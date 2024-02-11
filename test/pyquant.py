import mumaxpy 
import cupy as cp
import numpy as np

class SimpleField:
    def __init__(self, mm):
        self.ncomp = 3
        self.mm = mm

    def __call__(self, Bx, By, Bz):

        m = self.mm.m 
        msl = self.mm.SliceOf(m, gpu=True)
        field = 3 * cp.asarray(msl)
        
        for i, B in enumerate([Bx, By, Bz]):
            B_cp = cp.asarray(B)
            cp.copyto(B_cp, field[i])


with mumaxpy.Mumax() as mm:

    mm.SetGridSize(64, 64, 2)
    mm.SetCellSize(1e-9, 1e-9, 1e-9)

    mm.m = mm.Uniform(1, 0, 0)
    print("external average:", mm.m.Average())
    field_external = 3 * mm.SliceOf(mm.m)

    fi = mm.ValueOf(SimpleField(mm))
    field_internal = mm.NewSlice(3, 64, 64, 2)
    mm.SliceCopy(field_internal, fi)
    mm.Recycle(fi)

    print("Resulting average:", np.mean(field_internal, axis=(1,2, 3)))

    diff = field_internal - field_external
    print("cupy v cpu:", np.sum(np.abs(diff) > 1e-5) / diff.size)

field_internal.close()
