import socket
import subprocess
import signal
import atexit
import grpc
from . import mumax_pb2
from . import mumax_pb2_grpc
import os 
import asyncio
import time
import numpy as np
import multiprocessing.shared_memory as shm
import discretisedfield as df
from inspect import signature
from numba import cuda

from . import funcstrings
from . import revcom
from . import jupyterhack
from . import slices

socket_address = "mumaxpy.sock"

##This is THE class

class Mumax:

    def __init__(self, o=None, gpu=0, asynchronous=False, **kwargs):

        #serverpath = os.path.join('/root', 'go', 'bin', 'mumaxpy-server')
        serverpath = os.path.join(os.path.expanduser('~'), 'go', 'bin', 'mumaxpy-server')
        args = [serverpath]
        if o is None:
            o = os.path.join(os.getcwd(), "mumax.out")

        self._output_directory = o
        args.append("-o")
        args.append(o)
        
        self._gpu = gpu
        cuda.select_device(gpu)
        args.append("-gpu")
        args.append(str(gpu))

        for k, v in kwargs.items():
            args.append("-" + k)
            args.append(str(v))
        self.server = subprocess.Popen(args)

        ##if running in ipython terminal, we need to start the event loop manually. 

        #ok nevertheless ipython will continue to give an error if we communicate
        #with the client in run_until_complete. 
        #we can instead use create_task, and await inside run until complete

        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError as e:
            if str(e).startswith('There is no current event loop in thread'):
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
            else:
                raise 

        self.roc = self.loop.run_until_complete

        socketpath = "unix:" + socket_address
        self.channel = grpc.aio.insecure_channel(socketpath, options=[
            ('grpc.max_send_message_length', 1024**3),
            ('grpc.max_receive_message_length', 1024**3)])
        self.stub = mumax_pb2_grpc.mumaxStub(self.channel)

        self._asynchronous = asynchronous

        signal.signal(signal.SIGINT, self.close)
        signal.signal(signal.SIGTERM, self.close)
        atexit.register(self.close)

        #we just wait a while and hope that the server starts in this time
        time.sleep(1)

        self.typelist = dict()
        self.roc(self._populate_functions(asynchronous))

        self.scalarpyfuncs = []
        self.vectorpyfuncs = []

    async def _populate_functions(self, asynchronous):

        identifiers = self.stub.GetIdentifiers(mumax_pb2.NULL())

        self.types = dict()

        async for identifier in identifiers:
            match identifier.WhichOneof("props"):
                case "f":
                    s = funcstrings.functionString(identifier.name, identifier.f.argnames, identifier.f.argtypes, identifier.f.outtypes, identifier.doc, asynchronous)
                case "l":
                    s = funcstrings.lValueString(identifier.name, identifier.l.type, identifier.l.inputtype, identifier.doc)
                case "r":
                    s = funcstrings.rOnlyString(identifier.name, identifier.r.type, identifier.doc)
            exec(s)

        #however, we now modify the new slice function to work in shared memory. 
        # we do these here so that the previous population doesn't overwrite. 
        # also, for consistency I guess we should define these asyncly. 

        if not asynchronous:    
            def NewSlice(self, ncomp, Nx, Ny, Nz):
                return Slice(self, ncomp, Nx, Ny, Nz)
            
            def DiscretisedField(self, quantity):
                return DiscretisedFieldMM(self, quantity, asynchronous=False)
            
            def SliceOf(self, quantity):
                #slice of gets the same info as discretised field, but by avoiding discretisedfields wrapping we keep the shared me alive.
                dim = quantity.NComp()
                if hasattr(quantity, "Mesh"):
                    mesh = quantity.Mesh()
                else:
                    mesh = self.m.Mesh()

                nx, ny, nz = mesh.Size()

                arr = self.NewSlice(dim, nx, ny, nz)
                gpusl = self.ValueOf(quantity)
                self.SliceCopy(arr, gpusl)
                self.Recycle(gpusl)

                return arr
            
            def NewGPUSlice(self, ncomp, Nx, Ny, Nz):
                return slices.GPUSlice(self, ncomp, Nx, Ny, Nz)
                
        else:
            async def NewSlice(self, ncomp, Nx, Ny, Nz, cpu=True):
                #nothing async about this at all. but the numpy routines themselves aren't so can't improve this obviously. 
                # Just for consistency with every other routine using async syntax.
                if cpu:
                    return Slice(self, ncomp, Nx, Ny, Nz)
                else:
                    return slices.GPUSlice(self, ncomp, Nx, Ny, Nz, self._gpu)

            async def SliceOf(self, quantity):
                dim = await quantity.NComp()
                if hasattr(quantity, "Mesh"):
                    mesh = await quantity.Mesh()
                else:
                    mesh = await self.m.Mesh()

                nx, ny, nz = await mesh.Size()

                arr = await self.NewSlice(dim, nx, ny, nz)
                gpusl = await self.ValueOf(quantity)
                await self.SliceCopy(arr, gpusl)
                await self.Recycle(gpusl)

                return arr

            async def DiscretisedField(self, quantity): 
                return DiscretisedFieldMM(self, quantity, asynchronous=True)
        
        self.NewSlice = NewSlice.__get__(self)
        self.DiscretisedField = DiscretisedField.__get__(self)
        self.SliceOf = SliceOf.__get__(self)
        self.NewGPUSlice = NewGPUSlice.__get__(self)

    def __enter__(self):
        return self

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self, sig=None, frame=None):
        
        self.server.send_signal(signal.SIGINT)
        self.roc(self.channel.close())

    def eval(self, cmd):
        if not isinstance(cmd, str):
            pass #this is an error 
        
        self.roc(self.stub.Eval(mumax_pb2.STRING(s=cmd)))

def toObj(identifier, vtype, master):
    if vtype not in master.typelist:
        makeType(master, vtype)
    return master.typelist[vtype](identifier) 

def makeType(master, vtype):

    def constructor(self, identifier):
        self.identifier = identifier

    def destructor(self):
        self.master.roc(self.master.stub.DestroyMumax(self.identifier))


    classdict = {"__init__": constructor,
                 "__del__": destructor, 
                 "__exit__": destructor, 
                  "master": master}

    master.roc(addMethods(master, vtype, classdict))

    master.typelist[vtype] = type(vtype, (object, ), classdict)

async def addMethods(master, vtype, classdict):
    req = mumax_pb2.STRING(s=vtype)
    identifiers = master.stub.GetTypeInfo(req)

    async for identifier in identifiers:
        match identifier.WhichOneof("props"):
            case "f":
                s = funcstrings.methodString(identifier.name, identifier.f.argnames, identifier.f.argtypes, identifier.f.outtypes, identifier.doc, master._asynchronous)
            case "l":
                s = funcstrings.fieldString(identifier.name, identifier.l.type, identifier.doc)
            case "r":
                s = funcstrings.fieldString(identifier.name, identifier.r.type, identifier.doc)
        exec(s)

class Slice(np.ndarray):

    initialised = False

    def __new__(cls, master, ncomp, nx, ny, nz):
        nbytes = ncomp * nx * ny * nz * 4 # 4 bytes in float32
        mem = shm.SharedMemory(create=True, size=nbytes)
        name = mem._name
        #then make slice. 
        basearr = np.ndarray(shape=(ncomp, nz, ny, nx), dtype=np.float32, buffer=mem.buf)
        basearr = np.moveaxis(basearr, [0, 1, 2, 3], [0, 3, 2, 1])
        arr = basearr.view(cls)
        arr.mumax_shape=(ncomp, nz, ny, nx)
        arr.master = master
        arr.identifier = master.roc(master.stub.NewSlice(mumax_pb2.Slice(ncomp=ncomp, nx=nx, ny=ny, nz=nz, file=name)))
        arr.shm = mem
        arr.maydestroy = True 

        if not cls.initialised:
            #addMethods(master, "*data.Slice", cls.__dict__) //this doesn't work, but don't really need it.
            cls.initialised = True
     
        return arr

    def __array_finalize__(self, arr):
        if arr is None: return
        self.master = getattr(arr, "master", None)
        self.identifier = getattr(arr, "identifier", None)
        self.shm = getattr(arr, "shm", None)
        self.maydestroy = getattr(arr, "maydestroy", False)

    def __array_wrap__(self, arr, context=None):
        arr = super().__array_wrap__(arr, context)
        arr.maydestroy=False

        if self is arr or type(self) is not Slice:
            return arr

        if arr.shape == ():
            return arr[()]
        
        return arr.view(np.ndarray)


    def destructor(self):
        #it is a niche edge case where mumax will still want access to a slice that python doesn't want.
        #so just ignore it.
        self.shm.unlink()
        self.shm.close()
        try:
            self.master.roc(self.master.stub.DestroyMumax(self.identifier))
        except:
            pass


    def __del__(self):
        if not isinstance(self.base, Slice) and self.maydestroy:
            self.destructor()

    def attach(self, master):
        self.master = master
        self.identifier = master.roc(master.stub.NewSlice(
            mumax_pb2.Slice(ncomp=self.mumax_shape[0], 
                            nx=self.mumax_shape[1],
                            ny=self.mumax_shape[2],
                            nz=self.mumax_shape[3],
                              file=self.shm._name)))


class DiscretisedFieldMM(df.Field):
    __class__ = df.Field #little trick to make ubermag work
    def __init__(self, master, quantity, asynchronous=False):

        if asynchronous:
            def r(f):
                return master.roc(f)
            def r(f):
                return f

        dim = r(quantity.NComp())

        if hasattr(quantity, "Mesh"):
            mesh = r(quantity.Mesh())
        else:
            mesh = r(master.m.Mesh())

        nx, ny, nz = r(mesh.Size())

        ubermesh = df.Mesh(p1=[0,0,0], p2=mesh.WorldSize(), n=[nx, ny, nz])
        
        if hasattr(quantity, "Unit"):
            unit = r(quantity.Unit())
        else:
            unit = "?"

        arr = r(self.NewSlice(dim, nx, ny, nz))
        gpusl = r(self.ValueOf(quantity))
        r(self.SliceCopy(arr, gpusl))
        r(self.Recycle(gpusl))

        super().__init__(ubermesh, dim, value=np.moveaxis(arr, 0, 3) , dtype=np.float32, units=unit)

def _pam(mmobj):
    return mmobj.identifier

def _makeScalarFunction(value, master):
    try:
        value = float(value)
        return mumax_pb2.ScalarFunction(scalar=value)
    except:
        if isinstance(value, str):
            return mumax_pb2.ScalarFunction(gocode=value)
        
        elif callable(value): #this would be the python call
            _pyfunc_setup(master.scalarpyfuncs, value, master)
            return mumax_pb2.ScalarFunction(pyfunc=len(master.scalarpyfuncs) - 1)
        
        else:
            raise TypeError("Scalar Function argument must either be a float, a string representing go code or a python function")
        
def _makeScalarFunction3(value, master):
    try:
        l = list(value)
        if len(l) != 3: raise TypeError("Gocode, Python Function or list of length 3 of these things")
        return mumax_pb2.ScalarFunction3(x = _makeScalarFunction(l[0], master),
                                         y = _makeScalarFunction(l[1], master), 
                                         z = _makeScalarFunction(l[2], master))
    except:
        raise TypeError("Gocode, Python Function or list of length 3 of these things")
    
def _makeVectorFunction(value, master):
    if isinstance(value, str):
         return mumax_pb2.VectorFunction(gocode=value)
    elif callable(value):
        _pyfunc_setup(master.vectorpyfuncs, value, master)
        return mumax_pb2.VectorFunction(pyfunc=len(master.vectorpyfuncs) - 1)
    else:
        return mumax_pb2.VectorFunction(components=_makeScalarFunction3(value, master))
    
def _pyfunc_setup(pyfunc_list, value, master):
    try:
        signat = signature(value)
        if len(signat.parameters) == 0:
            pyfunc_list.append(value)
        elif len(signat.parameters) == 1:
            pyfunc_list.append(lambda: value(master.t))
        else:
            raise TypeError("Python function must have either one or no arguments")
    except ValueError:
        #signature didn't work. Just assume this is a one argument function then.
        pyfunc_list.append(value)

def _processArray(arr):
    which = arr.WhichOneof('elements') 

    if which != 'a':
        return list(getattr(arr, which).s)
    else:
        return [_processArray(a) for a in getattr(arr, 'a').s]

