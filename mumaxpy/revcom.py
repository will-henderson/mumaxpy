import asyncio
import grpc
from . import mumax_pb2
from . import mumax_pb2_grpc
from numba import cuda
from contextlib import ExitStack
import numpy as np

### General Reverse Communication Things ###

class RevComHandler():
    def __init__(self, scalarpyfuncs, vectorpyfuncs, stub):
        self.scalarpyfuncs = scalarpyfuncs
        self.vectorpyfuncs = vectorpyfuncs
        self.stub = stub

    async def start(self):
        self.requests = self.stub.ReverseCommunication(self.handler())
    
    async def handler(self):
        async for request in self.requests:
            match request.WhichOneof("pyfunc"):
                case "scalarpyfunc":
                    val = self.scalarpyfuncs[request.scalarpyfunc]()
                    yield mumax_pb2.RevComResult(scalar=val)
                case "vectorpyfunc":
                    val = self.vectorpyfuncs[request.vectorpyfunc]()
                    yield mumax_pb2.RevComResult(vector=mumax_pb2.Vector(x=val[0], y=val[1], z=val[2]))


class RevComQuantHandler():
    def __init__(self, pyquants, stub):
        self.pyquants = pyquants
        self.stub = stub

    async def start(self):
        self.requests = self.stub.ReverseCommunicationQuantities(self.handler())

    async def handler(self):
        async for request in self.requests:
            sl = request.sl
            shape = (sl.nx, sl.ny, sl.nz)
            dtype = dtype(np.float32)
            strides = (dtype.itemsize, 
                   dtype.itemsize * sl.nx, 
                   dtype.itemsize * sl.nx * sl.ny)
            
            with ExitStack() as stack:
                dstarrs = [stack.enter_context(cuda.open_ipc_array(handle, shape, dtype, strides)) 
                           for handle in sl.handles]
                
                self.pyquants[request.funcno](*dstarrs)



async def Operation(operation, initialsend, master):

    async def op():
        return await operation(initialsend)

    op_task = asyncio.create_task(op())

    revcom_tasks = []

    if master.scalarpyfuncs or master.vectorpyfuncs:
        revcomhandler = RevComHandler(master.scalarpyfuncs, master.vectorpyfuncs, master.stub)
        revcom_tasks.append(asyncio.create_task(revcomhandler.start()))
    
    if master.pyquants:
        revcomquanthandler = RevComQuantHandler(master.pyquants, master.stub)
        revcom_tasks.append(asyncio.create_task(revcomquanthandler.start()))
    
    result = await op_task
    for task in revcom_tasks:
        task.cancel()

    return result 
