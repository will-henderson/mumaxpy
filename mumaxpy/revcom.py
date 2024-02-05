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

async def Operation(operation, initialsend, master):

    async def op():
        return await operation(initialsend)

    op_task = asyncio.create_task(op())

    if master.scalarpyfuncs or master.vectorpyfuncs:
        revcomhandler = RevComHandler(master.scalarpyfuncs, master.vectorpyfuncs, master.stub)
        revcom_task = asyncio.create_task(revcomhandler.start())
        result = await op_task
        revcom_task.cancel()
    else:
        result = await op_task

    return result 