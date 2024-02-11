import mumaxpy 
import cupy as cp
import numpy as np

class SimpleField:
    def __init__(self):
        self.NComp = 3
    def __call__(self, Bx, By, Bz):
        m = cp.array(mm.SliceOf(mm.m, gpu=True))
        for i, B in [Bx, By, Bz]:
            cp.copyto(B, 3*m[i])


with mumaxpy.Mumax() as mm:

    def simple_field(Bx, By, Bz):
        m = cp.array(mm.SliceOf(mm.m, gpu=True))

        for i, B in [Bx, By, Bz]:
            cp.copyto(B, 3*m[i])

    mm.SetGridSize(64, 64, 2)
    mm.SetCellSize(1e-9, 1e-9, 1e-9)

    mm.m = mm.RandomMagSeed(0)
    field_internal = mm.SliceOf(SimpleField())
    field_external = 3 * mm.SliceOf(mm.m)

    diff = field_internal - field_external
    print("cupy v cpu:", np.sum(np.abs(diff) > 1e-5) / diff.size)
