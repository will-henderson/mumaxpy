import numpy as np
import multiprocessing.shared_memory as shm
from . import mumax_pb2
import torch
        
class GPUSlice:
    def __init__(self, master, ncomp, nx, ny, nz, gpu):
        self._t = torch.zeros(size=(ncomp, nz, ny, nx), dtype=torch.float32, device=torch.device('cuda', gpu))
        self.handle = self._t.untyped_storage()._share_cuda_()[1]
        self.master = master
        self.identifier = master.roc(master.stub.NewGPUSlice(
            mumax_pb2.GPUSlice(ncomp = ncomp, 
                               nx = nx, 
                               ny = ny, 
                               nz = nz,
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