import numpy as np
import multiprocessing.shared_memory as shm
from . import mumax_pb2
import torch

class Slice(np.ndarray):

    initialised = False

    def __new__(cls, master, ncomp, nx, ny, nz):
        nbytes = ncomp * nx * ny * nz * 4 # 4 bytes in float32
        mem = shm.SharedMemory(create=True, size=nbytes)
        name = mem._name
        #then make slice. 
        basearr = np.ndarray(shape=(ncomp, nz, ny, nx), dtype=np.float32, buffer=mem.buf)
        basearr = np.moveaxis(basearr, [0, 1, 2, 3], [0, 3, 2, 1])
        arr = basearr.view(cls)
        arr.mumax_shape=(ncomp, nz, ny, nx)
        arr.master = master
        arr.identifier = master.loop.run_until_complete(master.stub.NewSlice(mumax_pb2.Slice(ncomp=ncomp, nx=nx, ny=ny, nz=nz, file=name)))
        arr.shm = mem
        arr.maydestroy = True 

        if not cls.initialised:
            #addMethods(master, "*data.Slice", cls.__dict__) //this doesn't work, but don't really need it.
            cls.initialised = True
     
        return arr

    def __array_finalize__(self, arr):
        if arr is None: return
        self.master = getattr(arr, "master", None)
        self.identifier = getattr(arr, "identifier", None)
        self.shm = getattr(arr, "shm", None)
        self.maydestroy = getattr(arr, "maydestroy", False)

    def __array_wrap__(self, arr, context=None):
        arr = super().__array_wrap__(arr, context)
        arr.maydestroy=False

        if self is arr or type(self) is not Slice:
            return arr

        if arr.shape == ():
            return arr[()]
        
        return arr.view(np.ndarray)


    def destructor(self):
        #it is a niche edge case where mumax will still want access to a slice that python doesn't want.
        #so just ignore it.
        self.master.loop.run_until_complete(self.master.stub.DestroyMumax(self.identifier))
        self.shm.unlink()
        self.shm.close()

    def __del__(self):
        if not isinstance(self.base, Slice) and self.maydestroy:
            self.destructor()

    def attach(self, master):
        self.master = master
        self.identifier = master.roc(master.stub.NewSlice(
            mumax_pb2.Slice(ncomp=self.mumax_shape[0], 
                            nx=self.mumax_shape[1],
                            ny=self.mumax_shape[2],
                            nz=self.mumax_shape[3],
                              file=self.shm._name)))
        
class GPUSlice:
    def __init__(self, master, ncomp, nx, ny, nz):
        devno = master.roc(master.Device())
        self._t = torch.zeros(size=(ncomp, nz, ny, nx), dtype=torch.float32, device=torch.device('cuda', devno))
        self.handle = self._t.untyped_storage()._share_cuda_()[1]
        self.master = master
        self.identifier = master.roc(master.stub.NewGPUSlice(
            mumax_pb2.GPUSlice(ncomp=self.ncomp, 
                               nx = self.nx, 
                               ny = self.ny, 
                               nz = self.nz,
                               handle = self.handle)))
        
        self._t = torch.movedim(self._t, [0, 1, 2, 3], [0, 3, 2, 1])

    def __repr__(self):
        return self._t.__repr__()

    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        args = [getattr(a, '_t', a) for a in args]
        ret = func(*args, **kwargs)
        return ret #cast into GPUSlice in some cases?

    #also need a destructor to release shared cuda tensors