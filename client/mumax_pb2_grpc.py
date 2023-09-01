# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import mumax_pb2 as mumax__pb2


class mumaxStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Eval = channel.unary_unary(
                '/mumaxpy.mumax/Eval',
                request_serializer=mumax__pb2.STRING.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.GetIdentifiers = channel.unary_stream(
                '/mumaxpy.mumax/GetIdentifiers',
                request_serializer=mumax__pb2.NULL.SerializeToString,
                response_deserializer=mumax__pb2.Identifier.FromString,
                )
        self.GetTypeInfo = channel.unary_stream(
                '/mumaxpy.mumax/GetTypeInfo',
                request_serializer=mumax__pb2.STRING.SerializeToString,
                response_deserializer=mumax__pb2.Identifier.FromString,
                )
        self.Call = channel.unary_unary(
                '/mumaxpy.mumax/Call',
                request_serializer=mumax__pb2.FunctionCall.SerializeToString,
                response_deserializer=mumax__pb2.CallResponse.FromString,
                )
        self.CallMethod = channel.unary_unary(
                '/mumaxpy.mumax/CallMethod',
                request_serializer=mumax__pb2.MethodCall.SerializeToString,
                response_deserializer=mumax__pb2.CallResponse.FromString,
                )
        self.GetBool = channel.unary_unary(
                '/mumaxpy.mumax/GetBool',
                request_serializer=mumax__pb2.MumaxObject.SerializeToString,
                response_deserializer=mumax__pb2.BOOL.FromString,
                )
        self.GetInt = channel.unary_unary(
                '/mumaxpy.mumax/GetInt',
                request_serializer=mumax__pb2.MumaxObject.SerializeToString,
                response_deserializer=mumax__pb2.INT.FromString,
                )
        self.GetString = channel.unary_unary(
                '/mumaxpy.mumax/GetString',
                request_serializer=mumax__pb2.MumaxObject.SerializeToString,
                response_deserializer=mumax__pb2.STRING.FromString,
                )
        self.GetDouble = channel.unary_unary(
                '/mumaxpy.mumax/GetDouble',
                request_serializer=mumax__pb2.MumaxObject.SerializeToString,
                response_deserializer=mumax__pb2.DOUBLE.FromString,
                )
        self.SetBool = channel.unary_unary(
                '/mumaxpy.mumax/SetBool',
                request_serializer=mumax__pb2.BoolSet.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.SetInt = channel.unary_unary(
                '/mumaxpy.mumax/SetInt',
                request_serializer=mumax__pb2.IntSet.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.SetDouble = channel.unary_unary(
                '/mumaxpy.mumax/SetDouble',
                request_serializer=mumax__pb2.DoubleSet.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.SetString = channel.unary_unary(
                '/mumaxpy.mumax/SetString',
                request_serializer=mumax__pb2.StringSet.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.SetVector = channel.unary_unary(
                '/mumaxpy.mumax/SetVector',
                request_serializer=mumax__pb2.VectorSet.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.SetScalarFunction = channel.unary_unary(
                '/mumaxpy.mumax/SetScalarFunction',
                request_serializer=mumax__pb2.ScalarFunctionSet.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.SetVectorFunction = channel.unary_unary(
                '/mumaxpy.mumax/SetVectorFunction',
                request_serializer=mumax__pb2.VectorFunctionSet.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.SetMumax = channel.unary_unary(
                '/mumaxpy.mumax/SetMumax',
                request_serializer=mumax__pb2.MumaxSet.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.GetFieldBool = channel.unary_unary(
                '/mumaxpy.mumax/GetFieldBool',
                request_serializer=mumax__pb2.MumaxField.SerializeToString,
                response_deserializer=mumax__pb2.BOOL.FromString,
                )
        self.GetFieldInt = channel.unary_unary(
                '/mumaxpy.mumax/GetFieldInt',
                request_serializer=mumax__pb2.MumaxField.SerializeToString,
                response_deserializer=mumax__pb2.INT.FromString,
                )
        self.GetFieldString = channel.unary_unary(
                '/mumaxpy.mumax/GetFieldString',
                request_serializer=mumax__pb2.MumaxField.SerializeToString,
                response_deserializer=mumax__pb2.STRING.FromString,
                )
        self.GetFieldDouble = channel.unary_unary(
                '/mumaxpy.mumax/GetFieldDouble',
                request_serializer=mumax__pb2.MumaxField.SerializeToString,
                response_deserializer=mumax__pb2.DOUBLE.FromString,
                )
        self.GetFieldMumax = channel.unary_unary(
                '/mumaxpy.mumax/GetFieldMumax',
                request_serializer=mumax__pb2.MumaxField.SerializeToString,
                response_deserializer=mumax__pb2.MumaxObject.FromString,
                )
        self.DestroyMumax = channel.unary_unary(
                '/mumaxpy.mumax/DestroyMumax',
                request_serializer=mumax__pb2.MumaxObject.SerializeToString,
                response_deserializer=mumax__pb2.NULL.FromString,
                )
        self.NewSlice = channel.unary_unary(
                '/mumaxpy.mumax/NewSlice',
                request_serializer=mumax__pb2.Slice.SerializeToString,
                response_deserializer=mumax__pb2.MumaxObject.FromString,
                )


class mumaxServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Eval(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIdentifiers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTypeInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Call(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CallMethod(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBool(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetInt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetString(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDouble(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetBool(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetInt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetDouble(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetString(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetVector(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetScalarFunction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetVectorFunction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetMumax(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFieldBool(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFieldInt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFieldString(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFieldDouble(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFieldMumax(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DestroyMumax(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NewSlice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_mumaxServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Eval': grpc.unary_unary_rpc_method_handler(
                    servicer.Eval,
                    request_deserializer=mumax__pb2.STRING.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'GetIdentifiers': grpc.unary_stream_rpc_method_handler(
                    servicer.GetIdentifiers,
                    request_deserializer=mumax__pb2.NULL.FromString,
                    response_serializer=mumax__pb2.Identifier.SerializeToString,
            ),
            'GetTypeInfo': grpc.unary_stream_rpc_method_handler(
                    servicer.GetTypeInfo,
                    request_deserializer=mumax__pb2.STRING.FromString,
                    response_serializer=mumax__pb2.Identifier.SerializeToString,
            ),
            'Call': grpc.unary_unary_rpc_method_handler(
                    servicer.Call,
                    request_deserializer=mumax__pb2.FunctionCall.FromString,
                    response_serializer=mumax__pb2.CallResponse.SerializeToString,
            ),
            'CallMethod': grpc.unary_unary_rpc_method_handler(
                    servicer.CallMethod,
                    request_deserializer=mumax__pb2.MethodCall.FromString,
                    response_serializer=mumax__pb2.CallResponse.SerializeToString,
            ),
            'GetBool': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBool,
                    request_deserializer=mumax__pb2.MumaxObject.FromString,
                    response_serializer=mumax__pb2.BOOL.SerializeToString,
            ),
            'GetInt': grpc.unary_unary_rpc_method_handler(
                    servicer.GetInt,
                    request_deserializer=mumax__pb2.MumaxObject.FromString,
                    response_serializer=mumax__pb2.INT.SerializeToString,
            ),
            'GetString': grpc.unary_unary_rpc_method_handler(
                    servicer.GetString,
                    request_deserializer=mumax__pb2.MumaxObject.FromString,
                    response_serializer=mumax__pb2.STRING.SerializeToString,
            ),
            'GetDouble': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDouble,
                    request_deserializer=mumax__pb2.MumaxObject.FromString,
                    response_serializer=mumax__pb2.DOUBLE.SerializeToString,
            ),
            'SetBool': grpc.unary_unary_rpc_method_handler(
                    servicer.SetBool,
                    request_deserializer=mumax__pb2.BoolSet.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'SetInt': grpc.unary_unary_rpc_method_handler(
                    servicer.SetInt,
                    request_deserializer=mumax__pb2.IntSet.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'SetDouble': grpc.unary_unary_rpc_method_handler(
                    servicer.SetDouble,
                    request_deserializer=mumax__pb2.DoubleSet.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'SetString': grpc.unary_unary_rpc_method_handler(
                    servicer.SetString,
                    request_deserializer=mumax__pb2.StringSet.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'SetVector': grpc.unary_unary_rpc_method_handler(
                    servicer.SetVector,
                    request_deserializer=mumax__pb2.VectorSet.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'SetScalarFunction': grpc.unary_unary_rpc_method_handler(
                    servicer.SetScalarFunction,
                    request_deserializer=mumax__pb2.ScalarFunctionSet.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'SetVectorFunction': grpc.unary_unary_rpc_method_handler(
                    servicer.SetVectorFunction,
                    request_deserializer=mumax__pb2.VectorFunctionSet.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'SetMumax': grpc.unary_unary_rpc_method_handler(
                    servicer.SetMumax,
                    request_deserializer=mumax__pb2.MumaxSet.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'GetFieldBool': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFieldBool,
                    request_deserializer=mumax__pb2.MumaxField.FromString,
                    response_serializer=mumax__pb2.BOOL.SerializeToString,
            ),
            'GetFieldInt': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFieldInt,
                    request_deserializer=mumax__pb2.MumaxField.FromString,
                    response_serializer=mumax__pb2.INT.SerializeToString,
            ),
            'GetFieldString': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFieldString,
                    request_deserializer=mumax__pb2.MumaxField.FromString,
                    response_serializer=mumax__pb2.STRING.SerializeToString,
            ),
            'GetFieldDouble': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFieldDouble,
                    request_deserializer=mumax__pb2.MumaxField.FromString,
                    response_serializer=mumax__pb2.DOUBLE.SerializeToString,
            ),
            'GetFieldMumax': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFieldMumax,
                    request_deserializer=mumax__pb2.MumaxField.FromString,
                    response_serializer=mumax__pb2.MumaxObject.SerializeToString,
            ),
            'DestroyMumax': grpc.unary_unary_rpc_method_handler(
                    servicer.DestroyMumax,
                    request_deserializer=mumax__pb2.MumaxObject.FromString,
                    response_serializer=mumax__pb2.NULL.SerializeToString,
            ),
            'NewSlice': grpc.unary_unary_rpc_method_handler(
                    servicer.NewSlice,
                    request_deserializer=mumax__pb2.Slice.FromString,
                    response_serializer=mumax__pb2.MumaxObject.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mumaxpy.mumax', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class mumax(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Eval(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/Eval',
            mumax__pb2.STRING.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetIdentifiers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mumaxpy.mumax/GetIdentifiers',
            mumax__pb2.NULL.SerializeToString,
            mumax__pb2.Identifier.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTypeInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mumaxpy.mumax/GetTypeInfo',
            mumax__pb2.STRING.SerializeToString,
            mumax__pb2.Identifier.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Call(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/Call',
            mumax__pb2.FunctionCall.SerializeToString,
            mumax__pb2.CallResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CallMethod(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/CallMethod',
            mumax__pb2.MethodCall.SerializeToString,
            mumax__pb2.CallResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBool(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetBool',
            mumax__pb2.MumaxObject.SerializeToString,
            mumax__pb2.BOOL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetInt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetInt',
            mumax__pb2.MumaxObject.SerializeToString,
            mumax__pb2.INT.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetString(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetString',
            mumax__pb2.MumaxObject.SerializeToString,
            mumax__pb2.STRING.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDouble(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetDouble',
            mumax__pb2.MumaxObject.SerializeToString,
            mumax__pb2.DOUBLE.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetBool(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/SetBool',
            mumax__pb2.BoolSet.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetInt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/SetInt',
            mumax__pb2.IntSet.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetDouble(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/SetDouble',
            mumax__pb2.DoubleSet.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetString(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/SetString',
            mumax__pb2.StringSet.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetVector(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/SetVector',
            mumax__pb2.VectorSet.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetScalarFunction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/SetScalarFunction',
            mumax__pb2.ScalarFunctionSet.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetVectorFunction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/SetVectorFunction',
            mumax__pb2.VectorFunctionSet.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetMumax(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/SetMumax',
            mumax__pb2.MumaxSet.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFieldBool(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetFieldBool',
            mumax__pb2.MumaxField.SerializeToString,
            mumax__pb2.BOOL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFieldInt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetFieldInt',
            mumax__pb2.MumaxField.SerializeToString,
            mumax__pb2.INT.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFieldString(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetFieldString',
            mumax__pb2.MumaxField.SerializeToString,
            mumax__pb2.STRING.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFieldDouble(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetFieldDouble',
            mumax__pb2.MumaxField.SerializeToString,
            mumax__pb2.DOUBLE.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFieldMumax(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/GetFieldMumax',
            mumax__pb2.MumaxField.SerializeToString,
            mumax__pb2.MumaxObject.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DestroyMumax(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/DestroyMumax',
            mumax__pb2.MumaxObject.SerializeToString,
            mumax__pb2.NULL.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NewSlice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mumaxpy.mumax/NewSlice',
            mumax__pb2.Slice.SerializeToString,
            mumax__pb2.MumaxObject.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
