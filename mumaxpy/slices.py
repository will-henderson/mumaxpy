import numpy as np
import multiprocessing.shared_memory as shm
from . import mumax_pb2
from numba import cuda
        
class GPUSlice:
    def __init__(self, master, ncomp, nx, ny, nz):
        self._t = cuda.device_array((ncomp, nz, ny, nx), np.float32)
        self.handle = bytes(self._t.get_ipc_handle()._ipc_handle.handle)
        self.master = master
        self.identifier = master.roc(master.stub.NewGPUSlice(mumax_pb2.GPUSlice(ncomp=ncomp, nx=nx, ny=ny, nz=nz, handle=self.handle)))
