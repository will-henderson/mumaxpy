import asyncio
import grpc
from . import mumax_pb2
from . import mumax_pb2_grpc

async def functionCall(fc, stub):
    return stub.Call(fc)

class RevComHandler():
    def __init__(self, pyfuncs, stub):
        self.pyfuncs = pyfuncs
        self.stub = stub
        self.requests = stub.ReverseCommunication(self.handler())
    
    def handler(self):
        for request in self.requests:
            match request.WhichOneof("pyfunc"):
                case "scalarpyfunc":
                    yield self.pyfuncs[request.scalarpyfunc]()
                case "vectorpyfunc":
                    yield self.pyfuncs[request.vectorpyfunc]()

async def revcomStreaming(pyfuncs, stub):
    revComHandler = RevComHandler(pyfuncs, stub)

async def Call(fc, master):
    call_task = asyncio.create_task(functionCall(fc, master.stub))

    if master.scalarpyfuncs or master.vectorpyfuncs:
        revcom_task = asyncio.create_task(revcomStreaming(master.pyfuncs, master.stub))
        result = await call_task
        revcom_task.cancel()
    else:
        result = await call_task

    return result