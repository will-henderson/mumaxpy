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

### Getting data from mumax 

```python
import mumaxpy

fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)
fig.tight_layout(h_pad=1, w_pad=3)

i = 0
def show(field, title):
    global i

    x = int(i/2)
    y = i%2
    field.sel('z').mpl(ax=ax[x, y])
    ax[x, y].set_title(title, size=10)
    ax[x, y].set_xlabel(ax[x, y].get_xlabel(), fontsize=10)
    ax[x, y].set_ylabel(ax[x, y].get_ylabel(), fontsize=10)
    cbar = ax[x, y].images[0].colorbar
    cbar.set_label("$m_z$", fontsize=10, labelpad=-1)
    cbar.ax.tick_params(labelsize=5)
    cbar.ax.yaxis.get_offset_text().set_fontsize(5)
    i += 1

with mumaxpy.Mumax() as mm:
    mm.SetGridSize(256, 128, 50)
    mm.SetCellSize(5e-9, 5e-9, 5e-9)

    mm.m = mm.Uniform(1, 1, 0)
    show(mm.DiscretisedField(mm.m),  "uniform")

    mm.m = mm.Vortex(1, -1)
    show(mm.DiscretisedField(mm.m), "vortex")
    ss
    mm.m = mm.TwoDomain(1,0,0,  0,1,0,  -1,0,0)
    show(mm.DiscretisedField(mm.m), "twodomain")
    
    mm.m = mm.RandomMag()
    show(mm.DiscretisedField(mm.m), "randommag")
```

`Mumax.DiscretisedField(quantity)` is a convenience function based on the function `Mumax.NewSlice(ncomp, Nx, Ny, Nz)`, which creates an ubermag discretised field object from a slice. `Mumax.NewSlice` itself creates a slice in shared memory, and hence changes to the slice from either the server or client side are reflected in the other. It should be noted that the discretisedfield object does not allow this, as the initialisation of a discretisedfield moves data away from the initialising array. To get a slice of the same quantity as an array which is still in shared memory, the `Mumax.SliceOf(quantity)` function can be used. 

An array slice created like this is still available after the mumax-server process is finished (e.g. after exiting the enclosing with statement). It can be attached to a new mumax-server with the `Slice.attach(Mumax)` function. A use case for this is an initial simulation to find the ground state, and then subsequent simulations in time. 

### Time-Varying Fields

Mumax supports time varying fields, e.g. `B_ext = vector(0.01, 1e-6*sin(2*pi*f*t), 0)`. These can be supported in a number of ways. 

```python
import mumaxpy
import numpy as np
with mumaxpy.Mumax() as mm:

    # directly passing mx3 script
    mm.B_ext = "vector(0.01, 1e-6*sin(2*pi*f*t), 0)"

    # passing an array/tuple/list with components, some of which can be scalars
    mm.B_ext = [0.01, "1e-6*sin(2*pi*f*t)", 0]

    #passing a python function which returns a array/tuple/list:
    def timevarying(t):
        return [0.01, 1e-6 * np.sin(2 * np.pi * f *t), 0]
    mm.B_ext = timevarying

    #passing a python function for a scalar component
    def timevarying(t):
        return 1e-6 * np.sin(2 * np.pi * f *t)
    mm.B_ext = [0.01, timevarying, 0]  

```

and with other mixtures of things like this, e.g. multiple python functions in an array, or a mixture of mx3 script and python functions.


