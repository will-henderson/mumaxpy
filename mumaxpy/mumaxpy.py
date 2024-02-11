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
from inspect import signature
from numba import cuda

from . import funcstrings
from . import revcom
#from . import jupyterhack
from . import slices
from . import quantity

import nest_asyncio
nest_asyncio.apply()


socket_address = "mumaxpy.sock"

##This is THE class

class Mumax:

    _initialised_methods = False

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
                raise e

        self.roc = self.loop.run_until_complete
        #this is an issue if things are called from outside the main loop. 

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

        if not Mumax._initialised_methods:
            self.roc(self._populate_functions(asynchronous))
            Mumax._initialised_methods = True

        self.scalarpyfuncs = []
        self.vectorpyfuncs = []
        self.pyquants = []

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
            
        def _newslice(self, ncomp, Nx, Ny, Nz, gpu):
            if not gpu:
                return slices.Slice(self, ncomp, Nx, Ny, Nz)
            else:
                return slices.GPUSlice(self, ncomp, Nx, Ny, Nz)

            
        if not asynchronous:    
            def NewSlice(self, ncomp, Nx, Ny, Nz, gpu=False):
                return _newslice(self, ncomp, Nx, Ny, Nz, gpu)
            
            def DiscretisedField(self, quantity):
                return slices.DiscretisedFieldMM(self, quantity, asynchronous=False)
            
            def SliceOf(self, quantity, gpu=False):
                #slice of gets the same info as discretised field, but by avoiding discretisedfields wrapping we keep the shared me alive.
                dim = quantity.NComp()
                if hasattr(quantity, "Mesh"):
                    mesh = quantity.Mesh()
                else:
                    mesh = self.m.Mesh()

                nx, ny, nz = mesh.Size()

                if not gpu:
                    arr = self.NewSlice(dim, nx, ny, nz, gpu)
                    gpusl = self.ValueOf(quantity)
                    self.SliceCopy(arr, gpusl)
                    self.Recycle(gpusl)
                else:
                    arr = self.NewSlice(dim, nx, ny, nz, gpu)
                    quantity.EvalTo(arr)

                return arr
                
        else:
            async def NewSlice(self, ncomp, Nx, Ny, Nz, gpu=False):
                #nothing async about this at all. but the numpy routines themselves aren't so can't improve this obviously. 
                # Just for consistency with every other routine using async syntax.
                return _newslice(self, ncomp, Nx, Ny, Nz, gpu)

            async def SliceOf(self, quantity, gpu=False):
                dim = await quantity.NComp()
                if hasattr(quantity, "Mesh"):
                    mesh = await quantity.Mesh()
                else:
                    mesh = await self.m.Mesh()

                nx, ny, nz = await mesh.Size()

                if not gpu:
                    arr = await self.NewSlice(dim, nx, ny, nz, gpu)
                    gpusl = await self.ValueOf(quantity)
                    await self.SliceCopy(arr, gpusl)
                    await self.Recycle(gpusl)
                else:
                    arr = self.NewSlice(dim, nx, ny, nz, gpu)
                    quantity.EvalTo(arr)

                return arr

            async def DiscretisedField(self, quantity): 
                return slices.DiscretisedFieldMM(self, quantity, asynchronous=True)
        
        self.NewSlice = NewSlice.__get__(self)
        self.DiscretisedField = DiscretisedField.__get__(self)
        self.SliceOf = SliceOf.__get__(self)

    def __enter__(self):
        return self

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self, sig=None, frame=None):
        
        self.server.send_signal(signal.SIGINT)
        self.roc(self.channel.close())
        #os.remove(socket_address)

    def eval(self, cmd):
        if not isinstance(cmd, str):
            pass #this is an error
        
        self.roc(self.stub.Eval(mumax_pb2.STRING(s=cmd)))

async def toObj(identifier, vtype, master):
    if vtype not in master.typelist:
        await makeType(master, vtype)
    return master.typelist[vtype](identifier) 

async def makeType(master, vtype):

    def constructor(self, identifier):
        self.identifier = identifier

    def destructor(self):
        try:
            self.master.roc(self.master.stub.DestroyMumax(self.identifier))
        except grpc._cython.cygrpc.UsageError:
            pass #this is fine, mumax is dead so don't need to destroy anything inside


    classdict = {"__init__": constructor,
                 "__del__": destructor, 
                 "__exit__": destructor, 
                  "master": master}

    await addMethods(master, vtype, classdict)
    master.typelist[vtype] = type(vtype, (object, ), classdict)
    return 

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
    return

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
    

def _makeQuantity(value, master):
    if isinstance(value, str):
        return mumax_pb2.Quantity(gocode=value)
    elif hasattr(value, "identifier"):
        return mumax_pb2.Quantity(mmobj=_pam(value))
    elif quantity.isquantity(value):
        master.pyquants.append(value)
        return mumax_pb2.Quantity(py=mumax_pb2.PyQuant(ncomp=value.ncomp, funcno=len(master.pyquants)-1))
        
    elif callable(value):
        raise TypeError("it appears you have tried to pass a python function, \
                        however, to pass a quantity in this way it must be as an object which is callable, \
                        and has the ncomp attribute. you can use the mumaxpy.Quantity class for this.")
    

    
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

