import asyncio
import grpc
from . import mumax_pb2
from . import mumax_pb2_grpc

### General Reverse Communication Things ###

class RevComHandler():
    def __init__(self, scalarpyfuncs, vectorpyfuncs, stub):
        self.scalarpyfuncs = scalarpyfuncs
        self.vectorpyfuncs = vectorpyfuncs
        self.stub = stub
        print('about to start revcom')
        self.requests = stub.ReverseCommunication(self.handler())
    
    def handler(self):
        for request in self.requests:
            print(request)
            match request.WhichOneof("pyfunc"):
                case "scalarpyfunc":
                    yield self.scalarpyfuncs[request.scalarpyfunc]()
                case "vectorpyfunc":
                    yield self.vectorpyfuncs[request.vectorpyfunc]()

async def revcomStreaming(scalarpyfuncs, vectorpyfuncs, stub):
    print('well did we get here?')
    revComHandler = RevComHandler(scalarpyfuncs, vectorpyfuncs, stub)

async def TESTY():
    print('did he start?')

async def revComOperation(initialsend, operation, master):
    op_task = asyncio.create_task(operation(initialsend, master.stub))

    if master.scalarpyfuncs or master.vectorpyfuncs:
        TESTYtask = asyncio.create_task(TESTY())
        revcom_task = asyncio.create_task(revcomStreaming(master.scalarpyfuncs, master.vectorpyfuncs, master.stub))
        result = await op_task
        revcom_task.cancel()
    else:
        result = await op_task

    return result 

### Function Calls ###

async def call(fc, stub):
    return stub.Call(fc)

def call_rc(fc, master):
    return asyncio.run(revComOperation(fc, call, master))

### Setting Scalar Functions ###

# we need to use this here because mumax will initally call this once
# when setting the first time

async def setScalarFunction(s, stub):
    return stub.SetScalarFunction(s)

async def setScalarFunction_rc(s, master):
    return asyncio.run(revComOperation(s, setScalarFunction, master))

### Setting Vector Functions ###

# we need to use this here because mumax will initally call this once
# when setting the first time

async def setVectorFunction(s, stub):
    return stub.SetVectorFunction(s)

def setVectorFunction_rc(s, master):
    return asyncio.run(revComOperation(s, setVectorFunction, master))