import numpy as np
import multiprocessing.shared_memory as shm
from . import mumax_pb2
from numba import cuda
import discretisedfield as df
        
class GPUSlice(cuda.cudadrv.devicearray.DeviceNDArray):
    def __init__(self, master, ncomp, nx, ny, nz):
        
        dtype = np.dtype(np.float32)
        strides = (dtype.itemsize * nx * ny * nz,
                   dtype.itemsize, 
                   dtype.itemsize * nx, 
                   dtype.itemsize * nx * ny)

        super().__init__((ncomp, nx, ny, nz), dtype=dtype, strides=strides)
        self.handle = bytes(self.get_ipc_handle()._ipc_handle.handle)
        self.master = master
        self.identifier = master.roc(master.stub.NewGPUSlice(mumax_pb2.GPUSlice(ncomp=ncomp, nx=nx, ny=ny, nz=nz, handle=self.handle)))

    def attach(self, master):
        self.master = master
        self.identifier = master.roc(master.stub.NewGPUSlice(
            mumax_pb2.GPUSlice(
                ncomp=self.shape[0],
                nx=self.shape[1],
                ny=self.shape[2], 
                nz=self.shape[3], handle=self.handle)))

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
        arr.identifier = master.roc(master.stub.NewSlice(mumax_pb2.Slice(ncomp=ncomp, nx=nx, ny=ny, nz=nz, file=name)))
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


    def close(self):
        #it is a niche edge case where mumax will still want access to a slice that python doesn't want.
        #so just ignore it.
        self.shm.unlink()
        self.shm.close()
        try:
            self.master.roc(self.master.stub.DestroyMumax(self.identifier))
        except:
            pass


    def __del__(self):
        if not isinstance(self.base, self.__class__) and self.maydestroy:
            try:
                self.close()
            except FileNotFoundError:
                pass #this find, probably have already closed.

    def attach(self, master):
        self.master = master
        self.identifier = master.roc(master.stub.NewSlice(
            mumax_pb2.Slice(ncomp=self.mumax_shape[0], 
                            nx=self.mumax_shape[1],
                            ny=self.mumax_shape[2],
                            nz=self.mumax_shape[3],
                              file=self.shm._name)))

class DiscretisedFieldMM(df.Field):
    __class__ = df.Field #little trick to make ubermag work
    def __init__(self, master, quantity, asynchronous=False):

        if asynchronous:
            def r(f):
                return master.roc(f)
            def r(f):
                return f

        dim = r(quantity.NComp())

        if hasattr(quantity, "Mesh"):
            mesh = r(quantity.Mesh())
        else:
            mesh = r(master.m.Mesh())

        nx, ny, nz = r(mesh.Size())

        ubermesh = df.Mesh(p1=[0,0,0], p2=mesh.WorldSize(), n=[nx, ny, nz])
        
        if hasattr(quantity, "Unit"):
            unit = r(quantity.Unit())
        else:
            unit = "?"

        arr = r(self.NewSlice(dim, nx, ny, nz))
        gpusl = r(self.ValueOf(quantity))
        r(self.SliceCopy(arr, gpusl))
        r(self.Recycle(gpusl))

        super().__init__(ubermesh, dim, value=np.moveaxis(arr, 0, 3) , dtype=np.float32, units=unit)