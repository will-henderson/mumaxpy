import mumaxpy

with mumaxpy.Mumax() as mm:
    
    mm.SetGridSize(1, 1, 1)
    mm.SetCellSize(1e-9, 1e-9, 1e-9)

    mm.Msat = 1000e3
    mm.alpha = 1e-6
    mm.Kc1 = 1e3
    mm.MaxDt = 1e-13 
    mm.Ku1 = 1e5
    mm.EnableDemag = False
    mm.anisC1 = (1, 0, 0)
    mm.anisC2 = (0, 1, 0)
    mm.anisU = (1, 1, 0)
    mm.m = mm.Uniform(.3, .7, .1)

    E0 = mm.E_total.Get()
    TOL = 1e-5

    for i in range(10):
        mm.Run(10e-12)
        E = mm.E_total.Get()
        mm.Expect("deltaE", (E0 - E) / E0, 0, TOL)