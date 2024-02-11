import mumaxpy 
import cupy as cp
import numpy as np

class SimpleField:
    def __init__(self, mm):
        self.ncomp = 3
        self.mm = mm

    def __call__(self, Bx, By, Bz):
        print("calling function")
        m = self.mm.m 
        print("got m")
        print("do getting things work", mm.t)

        print("do functions work?", mm.ceil(2.3))
        print(m.NComp())
        msl = self.mm.SliceOf(m, gpu=True)
        print("got a slice")
        m = cp.array(msl)
        print("about to copy")
        for i, B in [Bx, By, Bz]:
            cp.copyto(B, 3*m[i])


with mumaxpy.Mumax() as mm:

    mm.SetGridSize(64, 64, 2)
    mm.SetCellSize(1e-9, 1e-9, 1e-9)

    mm.m = mm.RandomMagSeed(0)
    field_external = 3 * mm.SliceOf(mm.m)

    fi = mm.ValueOf(SimpleField(mm))
    field_internal = mm.NewSlice(3, 64, 64, 2)
    mm.SliceCopy(fi, field_internal)
    mm.Recycle(fi)

    diff = field_internal - field_external
    print("cupy v cpu:", np.sum(np.abs(diff) > 1e-5) / diff.size)

field_internal.close()
