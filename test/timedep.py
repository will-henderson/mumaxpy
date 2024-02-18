import mumaxpy
import numpy as np

with mumaxpy.Mumax() as mm:
    
    c = 4e-9
    mm.SetGridSize(32, 32, 1)
    mm.SetCellSize(c, c, c)

    mm.Msat = 860e3
    mm.Aex = 13e-12
    mm.alpha = 0.2
    mm.m = mm.Uniform(1, 1, 0)
    mm.anisU = (0, 1, 0)

    f = 1e9

    def timefunc(t):
        return 1e5 * np.sin(2 * np.pi * f * t)

    #mm.Ku1 = "1e5 * sin(2 * pi * 1e9 * t)"
    mm.Ku1 = timefunc


    mm.Run(.5e-9)

    TOL = 1e-5
    mm.ExpectV("m", mm.m.Average(), (0, 0.9909376502037048, 0), TOL)