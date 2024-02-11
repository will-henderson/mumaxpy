import mumaxpy
import numpy as np
import cupy as cp

with mumaxpy.Mumax() as mm:
    mm.SetGridSize(64, 64, 2)
    mm.SetCellSize(1e-9, 1e-9, 1e-9)

    mm.m = mm.RandomMag()

    m_cpu = mm.SliceOf(mm.m)

    m_gpu = mm.SliceOf(mm.m, gpu=True)
    m_gpucpu = np.array(m_gpu)

    diff = m_gpucpu - m_cpu 
    print("cpu v gpu:", np.sum(np.abs(diff) > 1e-5) / diff.size)

    m_cp = cp.array(m_gpu)
    m_cpcpu = cp.asnumpy(m_cp)

    diff = m_cpcpu - m_cpu 
    print("cupy v cpu:", np.sum(np.abs(diff) > 1e-5) / diff.size)

m_cpu.close()