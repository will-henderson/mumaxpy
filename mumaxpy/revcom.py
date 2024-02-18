import asyncio
import grpc
from . import mumax_pb2
from . import mumax_pb2_grpc
from numba import cuda
from contextlib import ExitStack
import numpy as np

### General Reverse Communication Things ###

class RCHBase:
    def __init__(self, stub, optask):
        self.stub = stub
        self.optask = optask
        self.exception = []

    def handle_exception(self, e):
        self.optask.cancel()
        self.exception.append(e)

class RevComHandler(RCHBase):
    def __init__(self, scalarpyfuncs, vectorpyfuncs, stub, optask):
        self.scalarpyfuncs = scalarpyfuncs
        self.vectorpyfuncs = vectorpyfuncs
        super().__init__(stub, optask)

    async def start(self):
        self.requests = self.stub.ReverseCommunication(self.handler())
    
    async def handler(self):
        async for request in self.requests:
            try:
                match request.WhichOneof("pyfunc"):
                    case "scalarpyfunc":
                        val = self.scalarpyfuncs[request.scalarpyfunc]()
                        yield mumax_pb2.RevComResult(scalar=val)
                    case "vectorpyfunc":
                        val = self.vectorpyfuncs[request.vectorpyfunc]()
                        yield mumax_pb2.RevComResult(vector=mumax_pb2.Vector(x=val[0], y=val[1], z=val[2]))

            except Exception as e:
                self.handle_exception(e)
                break


                
class RevComQuantHandler(RCHBase):
    def __init__(self, pyquants, stub, optask):
        self.pyquants = pyquants
        super().__init__(stub, optask)

    async def start(self):
        self.requests = self.stub.ReverseCommunicationQuantities(self.handler())

    async def handler(self):
        async for request in self.requests:
            sl = request.sl
            shape = (sl.nx, sl.ny, sl.nz)
            dtype = np.dtype(np.float32)
            strides = (dtype.itemsize, 
                   dtype.itemsize * sl.nx, 
                   dtype.itemsize * sl.nx * sl.ny)

            with ExitStack() as stack:
                dstarrs = [stack.enter_context(cuda.open_ipc_array(handle, shape, dtype, strides)) 
                        for handle in sl.handles]
                try:
                    self.pyquants[request.funcno](*dstarrs)
                except Exception as e:
                    self.handle_exception(e)
                    break

            yield mumax_pb2.NULL()



async def Operation(operation, initialsend, master):

    async def op():
        return await operation(initialsend)

    op_task = asyncio.create_task(op())

    handlers = []
    revcom_tasks = []

    if master.scalarpyfuncs or master.vectorpyfuncs:
        handlers.append(RevComHandler(master.scalarpyfuncs, master.vectorpyfuncs, master.stub, op_task))
    
    if master.pyquants:
        handlers.append(RevComQuantHandler(master.pyquants, master.stub, op_task))

    revcom_tasks = [asyncio.create_task(handler.start()) for handler in handlers]
    
    try:
        result = await op_task
    except asyncio.CancelledError:
        for handler in handlers:
            for e in handler.exception:
                raise e #TODO: recover on the mumax side as well.

    for task in revcom_tasks:
        task.cancel()
  
    return result 

##ok, on nested calls, e.g. when calling Mesh() or something, we don't want to start a reverse communication loop.

def sync_operate_manager(operation, initialsend, master):

    try:
        task = asyncio.current_task()
        if task is None:
            istask = False
        else:
            istask = True
    except RuntimeError:
        istask = False

    if not istask:
        return master.roc(Operation(operation, initialsend, master))
    else:
        op = operation(initialsend)
        return master.roc(operation(initialsend))
    

async def async_operate_manager(operation, initialsend, master):
    
    try:
        task = asyncio.current_task()
        if task is None:
            istask = False
        else:
            istask = True
    except RuntimeError:
        istask = False

    if not istask:
        return await Operation(operation, initialsend, master)
    else:
        return await operation(initialsend)