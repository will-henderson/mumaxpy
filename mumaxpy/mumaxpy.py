import socket
import subprocess
import signal
import atexit
import grpc
from . import mumax_pb2
from . import mumax_pb2_grpc
import os 
import time
import numpy as np
import discretisedfield as df
import mmap
import multiprocessing.shared_memory as shm

from . import funcstrings


socket_address = "mumaxpy.sock"

class Mumax:

    def __init__(self, o=None, **kwargs):

        serverpath = os.path.join("installating_stuff", "mumaxpy-server")
        args = [serverpath]
        if o is None:
            o = os.path.join(os.getcwd(), "mumax.out")

        self._output_directory = o
        args.append("-o")
        args.append(o)
        for k, v in kwargs.items():
            args.append("-" + k)
            args.append(str(v))
        self.server = subprocess.Popen(args)

        socketpath = "unix:" + socket_address
        self.channel = grpc.insecure_channel(socketpath, options=[
            ('grpc.max_send_message_length', 1024**3),
            ('grpc.max_receive_message_length', 1024**3)])
        self.stub = mumax_pb2_grpc.mumaxStub(self.channel)

        signal.signal(signal.SIGINT, self.close)
        signal.signal(signal.SIGTERM, self.close)
        atexit.register(self.close)

        #we just wait a while and hope that the server starts in this time
        time.sleep(1)

        self.typelist = dict()
        self._populate_functions()

    def _populate_functions(self):

        identifiers = self.stub.GetIdentifiers(mumax_pb2.NULL())

        self.types = dict()

        for identifier in identifiers:
            match identifier.WhichOneof("props"):
                case "f":
                    s = funcstrings.functionString(identifier.name, identifier.f.argnames, identifier.f.argtypes, identifier.f.outtypes, identifier.doc)
                case "l":
                    s = funcstrings.lValueString(identifier.name, identifier.l.type, identifier.l.inputtype, identifier.doc)
                case "r":
                    s = funcstrings.rOnlyString(identifier.name, identifier.r.type, identifier.doc)
            exec(s)

        #however, we now modify the new slice function to work in shared memory. 
        def NewSlice(self, ncomp, Nx, Ny, Nz):
            return Slice(self, ncomp, Nx, Ny, Nz)
        self.NewSlice = NewSlice.__get__(self)

        def DiscretisedField(self, quantity):
            return DiscretisedFieldMM(self, quantity)
        self.DiscretisedField = DiscretisedField.__get__(self)


    def Directory():
        #this is a dictionary. The elements are the memory mapped files. I guess it could be writable. 
        pass

    @property
    def get_Table(self):
        #check if lines or columns have been added to table, if so update.
        pass

    def __del__(self):
        self.close()

    def __exit__(self):
        self.close()

    def close(self):
        
        self.server.send_signal(signal.SIGINT)
        self.channel.close()

    def eval(self, cmd):
        if not isinstance(cmd, str):
            pass #this is an error 
        
        self.stub.Eval(mumax_pb2.STRING(s=cmd))

def toObj(identifier, vtype, master):
    if vtype not in master.typelist:
        makeType(master, vtype)
    return master.typelist[vtype](identifier) 

def makeType(master, vtype):

    def constructor(self, identifier):
        self.identifier = identifier

    def destructor(self):
        self.master.stub.DestroyMumax(self.identifier)


    classdict = {"__init__": constructor,
                 "__del__": destructor, 
                 "__exit__": destructor, 
                  "master": master}

    addMethods(master, vtype, classdict)

    master.typelist[vtype] = type(vtype, (object, ), classdict)

def addMethods(master, vtype, classdict):
    req = mumax_pb2.STRING(s=vtype)
    identifiers = master.stub.GetTypeInfo(req)

    for identifier in identifiers:
        match identifier.WhichOneof("props"):
            case "f":
                s = funcstrings.methodString(identifier.name, identifier.f.argnames, identifier.f.argtypes, identifier.f.outtypes, identifier.doc)
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
        #then call make slice. 
        basearr = np.ndarray(shape=(ncomp, nz, ny, nx), dtype=np.float32, buffer=mem.buf)
        basearr = np.moveaxis(basearr, [0, 1, 2, 3], [0, 3, 2, 1])
        arr = basearr.view(cls)
        arr.master = master
        arr.identifier = master.stub.NewSlice(mumax_pb2.Slice(ncomp=ncomp, nx=nx, ny=ny, nz=nz, file=name))
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
        self.master.stub.DestroyMumax(self.identifier) 
        self.shm.unlink()
        self.shm.close()

    def __del__(self):
        if not isinstance(self.base, Slice) and self.maydestroy:
            self.destructor()
    
class DiscretisedFieldMM(df.Field):
    __class__ = df.Field #little trick to make ubermag work
    def __init__(self, master, quantity):

        dim = quantity.NComp()

        if hasattr(quantity, "Mesh"):
            mesh = quantity.Mesh()
        else:
            mesh = master.m.Mesh()

        nx, ny, nz = mesh.Size()

        ubermesh = df.Mesh(p1=[0,0,0], p2=mesh.WorldSize(), n=[nx, ny, nz])
        
        if hasattr(quantity, "Unit"):
            unit = quantity.Unit()
        else:
            unit = "?"

        arr = Slice(master, dim, nx, ny, nz)

        gpusl = master.ValueOf(quantity)
        master.SliceCopy(arr, gpusl)
        master.Recycle(gpusl)

        super().__init__(ubermesh, dim, value=np.moveaxis(arr, 0, 3) , dtype=np.float32, units=unit)

        
def _pam(mmobj):
    return mmobj.identifier

def _makeScalarFunction(value):
    try:
        value = float(value)
        return mumax_pb2.ScalarFunction(scalar=value)
    except:
        if isinstance(value, str):
            return mumax_pb2.ScalarFunction(gocode=value)
        elif hasattr(value, '__call__'): #this would be the python call
            raise NotImplementedError("Using python functions is not yet supported")
        else:
            raise TypeError("Scalar Function argument must either be a float or a string representing go code")
        
def _makeScalarFunction3(value):
    try:
        l = list(value)
        if len(l) != 3: raise TypeError("Gocode or list of length 3")
        return mumax_pb2.ScalarFunction3(x = _makeScalarFunction(l[0]),
                                         y = _makeScalarFunction(l[1]), 
                                         z = _makeScalarFunction(l[2]))
    except:
        raise TypeError("Gocode or list of length 3")
    
def _makeVectorFunction(value):
    if isinstance(value, str):
         return mumax_pb2.VectorFunction(gocode=value)
    else:
        return mumax_pb2.VectorFunction(components=_makeScalarFunction3(value))

def _processArray(arr):
    which = arr.WhichOneof('elements')

    if which != 'a':
        return list(getattr(arr, which).s)
    else:
        return [_processArray(a) for a in getattr(arr, 'a').s]

