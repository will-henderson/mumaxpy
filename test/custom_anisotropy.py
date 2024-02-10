import mumaxpy 
import cupy as cp
import numpy as np
from numba import cuda
import typing

def normalise(x):
    norm = np.linalg.norm(x)
    return x / norm

class CustomAnisField:

    def __init__(self, mm, k, u):
        self.ncomp = 3
        self.mm = mm
        self.prefactor = 2 * k / mm.Msat.Average()
        self.u = cp.array(u, dtype=np.float32)
        self.u = cp.expand_dims(self.u, 1)
        self.u = cp.expand_dims(self.u, 1)
        self.u = cp.expand_dims(self.u, 1)


    def field(self):
        m = cp.array(self.mm.SliceOf(self.mm.m, gpu=True))
        res = cp.sum(self.u * m, axis=0)
        res = cp.expand_dims(res, 0)
        res = res * self.u 
        return res, m

    def __call__(self, Bx, By, Bz):
        B, m = self.field()
        for i, Bi in enumerate([Bx, By, Bz]):
            Bi = cp.array(Bi)
            cp.copyto(Bi, B[i, :, :, :])

class CustomAnisEnergy(CustomAnisField):

    def __init__(self, mm, k, u):
        super().__init__(mm, k, u)
        self.ncomp = 1

    def __call__(self, E):
        B = self.field()
        m_full = mm.SliceOf(mm.m_full, gpu=True)
        cp.sum(-.5 * B, m_full, axis=0, out=E)




with mumaxpy.Mumax() as mm:
    
    mm.SetGridSize(64, 64, 1)
    mm.SetCellSize(4e-9, 4e-9, 2e-9)
    
    mm.Aex = 13e-12
    mm.alpha = 1
    mm.m = mm.Uniform(1, 1, 0)

    mm.Msat = 1100e3
        

    K = .5e6
    u = normalise([1000, 0, 0])

    anis_field = CustomAnisField(mm, K, u)
    anis_energy = CustomAnisEnergy(mm, K, u)


    test_cases = [
        {"B": [0, 0.00, 0], "m": 0.000, "E": -6.553505382400001e-17},
        {"B": [0, 0.01, 0], "m": 0.011, "E": -6.552704614400001e-17},
        {"B": [0, 0.03, 0], "m": 0.033, "E": -6.546302566400002e-17},
        {"B": [0, 0.10, 0], "m": 0.110, "E": -6.473485516800002e-17},
        {"B": [0, 0.30, 0], "m": 0.331, "E": -5.833683353600001e-17},
    ]

    for case in test_cases:
        mm.B_ext = case["B"]
        mm.Relax()
        mm.Expect("my", mm.m.Average()[1], case["m"], 1e-3)
        print(mm.E_custom)
        mm.Expect("E_custom", mm.E_custom, case["E"], 1e-22)