# MUMAXPY

Hello, I am excited to introduce my first contribution to the micromagnetic community :blush:.

## How to Use

### Evaluating mx3 code

A famililar way to use this will be by simply running mumax commands from python, e.g. Standard Problem 4:

```python
import mumaxpy

s = """
SetGridsize(128, 32, 1)
SetCellsize(500e-9/128, 125e-9/32, 3e-9)

Msat  = 800e3
Aex   = 13e-12
alpha = 0.02

m = uniform(1, .1, 0)
relax()
save(m)    // relaxed state

autosave(m, 200e-12)
tableautosave(10e-12)

B_ext = vector(-24.6E-3, 4.3E-3, 0)
run(1e-9)
"""

with mumaxpy.Mumax() as mm:
    mm.eval(s)

```

One can take advantage of the python enviroment by carrying out some logic in python and then calling mm.eval again.

### Directly calling mumax functions from python

```python
import mumaxpy
import numpy as np

with mumaxpy.Mumax() as mm:

    mm.SetGridSize(128, 32, 1)
    mm.SetCellSize(4e-9, 4e-9, 30e-9)
    
    mm.Msat = 800e3
    mm.Aex = 13e-12
    
    mm.m = mm.RandomMag()
    mm.Relax()
    
    Bmax = 100e-3
    Bstep = 1e-3
    mm.MinimizerStop = 1e-6
    
    extra = .1 * Bstep #add extra bit to include last as well in np.arange
    B_x = np.hstack([np.arange(0, Bmax+extra, Bstep), 
                     np.arange(Bmax, -Bmax-extra, -Bstep), 
                     np.arange(-Bmax, Bmax+extra, Bstep)])
    m_x = np.zeros_like(B_x)
    
    for i, B in enumerate(B_x):
        mm.B_ext = [B, 0, 0]
        mm.Minimize()
        m_x[i] = mm.m.Average()[0]
```

In this case, the functions are case-sensitive, and follow that used in the mumax documentation. 
I find using ipython's autocompletion useful for getting this right.

