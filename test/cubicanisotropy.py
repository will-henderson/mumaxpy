import mumaxpy 

with mumaxpy.Mumax() as mm:

    mm.SetGridSize(64, 64, 1)
    mm.SetCellSize(4e-9, 4e-9, 2e-9)
    mm.Aex = 13e-12
    mm.Msat = 1100e3
    mm.alpha = 1
    mm.m = mm.Uniform(1, 0, 0)

    mm.DefRegion(2, mm.Cylinder(100e-9, 100e-9))
    mm.DefRegion(3, mm.Rect(100e-9, 20e-9))
    mm.SetGeom(mm.Cylinder(64*4e-9, 64*4e-9))