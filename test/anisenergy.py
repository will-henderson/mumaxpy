import mumaxpy 

with mumaxpy.Mumax() as mm:

    mm.SetGridSize(32, 10, 2)
    c = 1e-9
    mm.SetCellSize(c, 2*c, 3*c)

    mm.EnableDemag = False
    mm.Aex = 10e-12

    mm.Msat = 1000e3
    mm.anisU = [0, 0, 1]
    mm.Ku1 = 1e6

    mm.m = mm.Uniform(1, 0, 0.1)

    mm.TableAdd(mm.E_total)
    mm.TableAutoSave(1e-12)

    E0 = mm.E_total.Get()
    mm.alpha = 1
    mm.Run(1e-9)
    E1 = mm.E_total.Get()
    Delta1 = E1 - E0
    print("DeltaE damped:", Delta1)

    mm.m = mm.Uniform(1, 0, 0.1)
    E0 = mm.E_total.Get()
    mm.alpha = 0
    mm.Run(1e-9)
    E1 = mm.E_total.Get()
    Delta2 = E1-E0
    print("DeltaE, undamped:", Delta2)
    
    ratio = abs(Delta2/Delta1)
    print("ratio:", ratio)

    mm.Expect("Relative energy non-conservation:", ratio, 0, 1e-6)