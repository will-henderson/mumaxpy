// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.3.0
// - protoc             (unknown)
// source: mumax.proto

package protocol

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

const (
	Mumax_Eval_FullMethodName                 = "/mumaxpy.mumax/Eval"
	Mumax_GetIdentifiers_FullMethodName       = "/mumaxpy.mumax/GetIdentifiers"
	Mumax_GetTypeInfo_FullMethodName          = "/mumaxpy.mumax/GetTypeInfo"
	Mumax_Call_FullMethodName                 = "/mumaxpy.mumax/Call"
	Mumax_CallMethod_FullMethodName           = "/mumaxpy.mumax/CallMethod"
	Mumax_ReverseCommunication_FullMethodName = "/mumaxpy.mumax/ReverseCommunication"
	Mumax_GetBool_FullMethodName              = "/mumaxpy.mumax/GetBool"
	Mumax_GetInt_FullMethodName               = "/mumaxpy.mumax/GetInt"
	Mumax_GetString_FullMethodName            = "/mumaxpy.mumax/GetString"
	Mumax_GetDouble_FullMethodName            = "/mumaxpy.mumax/GetDouble"
	Mumax_SetBool_FullMethodName              = "/mumaxpy.mumax/SetBool"
	Mumax_SetInt_FullMethodName               = "/mumaxpy.mumax/SetInt"
	Mumax_SetDouble_FullMethodName            = "/mumaxpy.mumax/SetDouble"
	Mumax_SetString_FullMethodName            = "/mumaxpy.mumax/SetString"
	Mumax_SetVector_FullMethodName            = "/mumaxpy.mumax/SetVector"
	Mumax_SetScalarFunction_FullMethodName    = "/mumaxpy.mumax/SetScalarFunction"
	Mumax_SetVectorFunction_FullMethodName    = "/mumaxpy.mumax/SetVectorFunction"
	Mumax_SetMumax_FullMethodName             = "/mumaxpy.mumax/SetMumax"
	Mumax_GetFieldBool_FullMethodName         = "/mumaxpy.mumax/GetFieldBool"
	Mumax_GetFieldInt_FullMethodName          = "/mumaxpy.mumax/GetFieldInt"
	Mumax_GetFieldString_FullMethodName       = "/mumaxpy.mumax/GetFieldString"
	Mumax_GetFieldDouble_FullMethodName       = "/mumaxpy.mumax/GetFieldDouble"
	Mumax_GetFieldMumax_FullMethodName        = "/mumaxpy.mumax/GetFieldMumax"
	Mumax_DestroyMumax_FullMethodName         = "/mumaxpy.mumax/DestroyMumax"
	Mumax_NewSlice_FullMethodName             = "/mumaxpy.mumax/NewSlice"
	Mumax_NewGPUSlice_FullMethodName          = "/mumaxpy.mumax/NewGPUSlice"
)

// MumaxClient is the client API for Mumax service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type MumaxClient interface {
	Eval(ctx context.Context, in *STRING, opts ...grpc.CallOption) (*NULL, error)
	GetIdentifiers(ctx context.Context, in *NULL, opts ...grpc.CallOption) (Mumax_GetIdentifiersClient, error)
	GetTypeInfo(ctx context.Context, in *STRING, opts ...grpc.CallOption) (Mumax_GetTypeInfoClient, error)
	Call(ctx context.Context, in *FunctionCall, opts ...grpc.CallOption) (*CallResponse, error)
	CallMethod(ctx context.Context, in *MethodCall, opts ...grpc.CallOption) (*CallResponse, error)
	ReverseCommunication(ctx context.Context, opts ...grpc.CallOption) (Mumax_ReverseCommunicationClient, error)
	GetBool(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*BOOL, error)
	GetInt(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*INT, error)
	GetString(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*STRING, error)
	GetDouble(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*DOUBLE, error)
	SetBool(ctx context.Context, in *BoolSet, opts ...grpc.CallOption) (*NULL, error)
	SetInt(ctx context.Context, in *IntSet, opts ...grpc.CallOption) (*NULL, error)
	SetDouble(ctx context.Context, in *DoubleSet, opts ...grpc.CallOption) (*NULL, error)
	SetString(ctx context.Context, in *StringSet, opts ...grpc.CallOption) (*NULL, error)
	SetVector(ctx context.Context, in *VectorSet, opts ...grpc.CallOption) (*NULL, error)
	SetScalarFunction(ctx context.Context, in *ScalarFunctionSet, opts ...grpc.CallOption) (*NULL, error)
	SetVectorFunction(ctx context.Context, in *VectorFunctionSet, opts ...grpc.CallOption) (*NULL, error)
	SetMumax(ctx context.Context, in *MumaxSet, opts ...grpc.CallOption) (*NULL, error)
	GetFieldBool(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*BOOL, error)
	GetFieldInt(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*INT, error)
	GetFieldString(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*STRING, error)
	GetFieldDouble(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*DOUBLE, error)
	GetFieldMumax(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*MumaxObject, error)
	DestroyMumax(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*NULL, error)
	NewSlice(ctx context.Context, in *Slice, opts ...grpc.CallOption) (*MumaxObject, error)
	NewGPUSlice(ctx context.Context, in *GPUSliceRequest, opts ...grpc.CallOption) (*GPUSlice, error)
}

type mumaxClient struct {
	cc grpc.ClientConnInterface
}

func NewMumaxClient(cc grpc.ClientConnInterface) MumaxClient {
	return &mumaxClient{cc}
}

func (c *mumaxClient) Eval(ctx context.Context, in *STRING, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_Eval_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetIdentifiers(ctx context.Context, in *NULL, opts ...grpc.CallOption) (Mumax_GetIdentifiersClient, error) {
	stream, err := c.cc.NewStream(ctx, &Mumax_ServiceDesc.Streams[0], Mumax_GetIdentifiers_FullMethodName, opts...)
	if err != nil {
		return nil, err
	}
	x := &mumaxGetIdentifiersClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type Mumax_GetIdentifiersClient interface {
	Recv() (*Identifier, error)
	grpc.ClientStream
}

type mumaxGetIdentifiersClient struct {
	grpc.ClientStream
}

func (x *mumaxGetIdentifiersClient) Recv() (*Identifier, error) {
	m := new(Identifier)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *mumaxClient) GetTypeInfo(ctx context.Context, in *STRING, opts ...grpc.CallOption) (Mumax_GetTypeInfoClient, error) {
	stream, err := c.cc.NewStream(ctx, &Mumax_ServiceDesc.Streams[1], Mumax_GetTypeInfo_FullMethodName, opts...)
	if err != nil {
		return nil, err
	}
	x := &mumaxGetTypeInfoClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type Mumax_GetTypeInfoClient interface {
	Recv() (*Identifier, error)
	grpc.ClientStream
}

type mumaxGetTypeInfoClient struct {
	grpc.ClientStream
}

func (x *mumaxGetTypeInfoClient) Recv() (*Identifier, error) {
	m := new(Identifier)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *mumaxClient) Call(ctx context.Context, in *FunctionCall, opts ...grpc.CallOption) (*CallResponse, error) {
	out := new(CallResponse)
	err := c.cc.Invoke(ctx, Mumax_Call_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) CallMethod(ctx context.Context, in *MethodCall, opts ...grpc.CallOption) (*CallResponse, error) {
	out := new(CallResponse)
	err := c.cc.Invoke(ctx, Mumax_CallMethod_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) ReverseCommunication(ctx context.Context, opts ...grpc.CallOption) (Mumax_ReverseCommunicationClient, error) {
	stream, err := c.cc.NewStream(ctx, &Mumax_ServiceDesc.Streams[2], Mumax_ReverseCommunication_FullMethodName, opts...)
	if err != nil {
		return nil, err
	}
	x := &mumaxReverseCommunicationClient{stream}
	return x, nil
}

type Mumax_ReverseCommunicationClient interface {
	Send(*RevComResult) error
	Recv() (*RevComRequest, error)
	grpc.ClientStream
}

type mumaxReverseCommunicationClient struct {
	grpc.ClientStream
}

func (x *mumaxReverseCommunicationClient) Send(m *RevComResult) error {
	return x.ClientStream.SendMsg(m)
}

func (x *mumaxReverseCommunicationClient) Recv() (*RevComRequest, error) {
	m := new(RevComRequest)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *mumaxClient) GetBool(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*BOOL, error) {
	out := new(BOOL)
	err := c.cc.Invoke(ctx, Mumax_GetBool_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetInt(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*INT, error) {
	out := new(INT)
	err := c.cc.Invoke(ctx, Mumax_GetInt_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetString(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*STRING, error) {
	out := new(STRING)
	err := c.cc.Invoke(ctx, Mumax_GetString_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetDouble(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*DOUBLE, error) {
	out := new(DOUBLE)
	err := c.cc.Invoke(ctx, Mumax_GetDouble_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) SetBool(ctx context.Context, in *BoolSet, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_SetBool_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) SetInt(ctx context.Context, in *IntSet, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_SetInt_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) SetDouble(ctx context.Context, in *DoubleSet, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_SetDouble_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) SetString(ctx context.Context, in *StringSet, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_SetString_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) SetVector(ctx context.Context, in *VectorSet, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_SetVector_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) SetScalarFunction(ctx context.Context, in *ScalarFunctionSet, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_SetScalarFunction_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) SetVectorFunction(ctx context.Context, in *VectorFunctionSet, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_SetVectorFunction_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) SetMumax(ctx context.Context, in *MumaxSet, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_SetMumax_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetFieldBool(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*BOOL, error) {
	out := new(BOOL)
	err := c.cc.Invoke(ctx, Mumax_GetFieldBool_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetFieldInt(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*INT, error) {
	out := new(INT)
	err := c.cc.Invoke(ctx, Mumax_GetFieldInt_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetFieldString(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*STRING, error) {
	out := new(STRING)
	err := c.cc.Invoke(ctx, Mumax_GetFieldString_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetFieldDouble(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*DOUBLE, error) {
	out := new(DOUBLE)
	err := c.cc.Invoke(ctx, Mumax_GetFieldDouble_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) GetFieldMumax(ctx context.Context, in *MumaxField, opts ...grpc.CallOption) (*MumaxObject, error) {
	out := new(MumaxObject)
	err := c.cc.Invoke(ctx, Mumax_GetFieldMumax_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) DestroyMumax(ctx context.Context, in *MumaxObject, opts ...grpc.CallOption) (*NULL, error) {
	out := new(NULL)
	err := c.cc.Invoke(ctx, Mumax_DestroyMumax_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) NewSlice(ctx context.Context, in *Slice, opts ...grpc.CallOption) (*MumaxObject, error) {
	out := new(MumaxObject)
	err := c.cc.Invoke(ctx, Mumax_NewSlice_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *mumaxClient) NewGPUSlice(ctx context.Context, in *GPUSliceRequest, opts ...grpc.CallOption) (*GPUSlice, error) {
	out := new(GPUSlice)
	err := c.cc.Invoke(ctx, Mumax_NewGPUSlice_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// MumaxServer is the server API for Mumax service.
// All implementations must embed UnimplementedMumaxServer
// for forward compatibility
type MumaxServer interface {
	Eval(context.Context, *STRING) (*NULL, error)
	GetIdentifiers(*NULL, Mumax_GetIdentifiersServer) error
	GetTypeInfo(*STRING, Mumax_GetTypeInfoServer) error
	Call(context.Context, *FunctionCall) (*CallResponse, error)
	CallMethod(context.Context, *MethodCall) (*CallResponse, error)
	ReverseCommunication(Mumax_ReverseCommunicationServer) error
	GetBool(context.Context, *MumaxObject) (*BOOL, error)
	GetInt(context.Context, *MumaxObject) (*INT, error)
	GetString(context.Context, *MumaxObject) (*STRING, error)
	GetDouble(context.Context, *MumaxObject) (*DOUBLE, error)
	SetBool(context.Context, *BoolSet) (*NULL, error)
	SetInt(context.Context, *IntSet) (*NULL, error)
	SetDouble(context.Context, *DoubleSet) (*NULL, error)
	SetString(context.Context, *StringSet) (*NULL, error)
	SetVector(context.Context, *VectorSet) (*NULL, error)
	SetScalarFunction(context.Context, *ScalarFunctionSet) (*NULL, error)
	SetVectorFunction(context.Context, *VectorFunctionSet) (*NULL, error)
	SetMumax(context.Context, *MumaxSet) (*NULL, error)
	GetFieldBool(context.Context, *MumaxField) (*BOOL, error)
	GetFieldInt(context.Context, *MumaxField) (*INT, error)
	GetFieldString(context.Context, *MumaxField) (*STRING, error)
	GetFieldDouble(context.Context, *MumaxField) (*DOUBLE, error)
	GetFieldMumax(context.Context, *MumaxField) (*MumaxObject, error)
	DestroyMumax(context.Context, *MumaxObject) (*NULL, error)
	NewSlice(context.Context, *Slice) (*MumaxObject, error)
	NewGPUSlice(context.Context, *GPUSliceRequest) (*GPUSlice, error)
	mustEmbedUnimplementedMumaxServer()
}

// UnimplementedMumaxServer must be embedded to have forward compatible implementations.
type UnimplementedMumaxServer struct {
}

func (UnimplementedMumaxServer) Eval(context.Context, *STRING) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Eval not implemented")
}
func (UnimplementedMumaxServer) GetIdentifiers(*NULL, Mumax_GetIdentifiersServer) error {
	return status.Errorf(codes.Unimplemented, "method GetIdentifiers not implemented")
}
func (UnimplementedMumaxServer) GetTypeInfo(*STRING, Mumax_GetTypeInfoServer) error {
	return status.Errorf(codes.Unimplemented, "method GetTypeInfo not implemented")
}
func (UnimplementedMumaxServer) Call(context.Context, *FunctionCall) (*CallResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Call not implemented")
}
func (UnimplementedMumaxServer) CallMethod(context.Context, *MethodCall) (*CallResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CallMethod not implemented")
}
func (UnimplementedMumaxServer) ReverseCommunication(Mumax_ReverseCommunicationServer) error {
	return status.Errorf(codes.Unimplemented, "method ReverseCommunication not implemented")
}
func (UnimplementedMumaxServer) GetBool(context.Context, *MumaxObject) (*BOOL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetBool not implemented")
}
func (UnimplementedMumaxServer) GetInt(context.Context, *MumaxObject) (*INT, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetInt not implemented")
}
func (UnimplementedMumaxServer) GetString(context.Context, *MumaxObject) (*STRING, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetString not implemented")
}
func (UnimplementedMumaxServer) GetDouble(context.Context, *MumaxObject) (*DOUBLE, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetDouble not implemented")
}
func (UnimplementedMumaxServer) SetBool(context.Context, *BoolSet) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SetBool not implemented")
}
func (UnimplementedMumaxServer) SetInt(context.Context, *IntSet) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SetInt not implemented")
}
func (UnimplementedMumaxServer) SetDouble(context.Context, *DoubleSet) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SetDouble not implemented")
}
func (UnimplementedMumaxServer) SetString(context.Context, *StringSet) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SetString not implemented")
}
func (UnimplementedMumaxServer) SetVector(context.Context, *VectorSet) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SetVector not implemented")
}
func (UnimplementedMumaxServer) SetScalarFunction(context.Context, *ScalarFunctionSet) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SetScalarFunction not implemented")
}
func (UnimplementedMumaxServer) SetVectorFunction(context.Context, *VectorFunctionSet) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SetVectorFunction not implemented")
}
func (UnimplementedMumaxServer) SetMumax(context.Context, *MumaxSet) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SetMumax not implemented")
}
func (UnimplementedMumaxServer) GetFieldBool(context.Context, *MumaxField) (*BOOL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetFieldBool not implemented")
}
func (UnimplementedMumaxServer) GetFieldInt(context.Context, *MumaxField) (*INT, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetFieldInt not implemented")
}
func (UnimplementedMumaxServer) GetFieldString(context.Context, *MumaxField) (*STRING, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetFieldString not implemented")
}
func (UnimplementedMumaxServer) GetFieldDouble(context.Context, *MumaxField) (*DOUBLE, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetFieldDouble not implemented")
}
func (UnimplementedMumaxServer) GetFieldMumax(context.Context, *MumaxField) (*MumaxObject, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetFieldMumax not implemented")
}
func (UnimplementedMumaxServer) DestroyMumax(context.Context, *MumaxObject) (*NULL, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DestroyMumax not implemented")
}
func (UnimplementedMumaxServer) NewSlice(context.Context, *Slice) (*MumaxObject, error) {
	return nil, status.Errorf(codes.Unimplemented, "method NewSlice not implemented")
}
func (UnimplementedMumaxServer) NewGPUSlice(context.Context, *GPUSliceRequest) (*GPUSlice, error) {
	return nil, status.Errorf(codes.Unimplemented, "method NewGPUSlice not implemented")
}
func (UnimplementedMumaxServer) mustEmbedUnimplementedMumaxServer() {}

// UnsafeMumaxServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to MumaxServer will
// result in compilation errors.
type UnsafeMumaxServer interface {
	mustEmbedUnimplementedMumaxServer()
}

func RegisterMumaxServer(s grpc.ServiceRegistrar, srv MumaxServer) {
	s.RegisterService(&Mumax_ServiceDesc, srv)
}

func _Mumax_Eval_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(STRING)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).Eval(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_Eval_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).Eval(ctx, req.(*STRING))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetIdentifiers_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(NULL)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(MumaxServer).GetIdentifiers(m, &mumaxGetIdentifiersServer{stream})
}

type Mumax_GetIdentifiersServer interface {
	Send(*Identifier) error
	grpc.ServerStream
}

type mumaxGetIdentifiersServer struct {
	grpc.ServerStream
}

func (x *mumaxGetIdentifiersServer) Send(m *Identifier) error {
	return x.ServerStream.SendMsg(m)
}

func _Mumax_GetTypeInfo_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(STRING)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(MumaxServer).GetTypeInfo(m, &mumaxGetTypeInfoServer{stream})
}

type Mumax_GetTypeInfoServer interface {
	Send(*Identifier) error
	grpc.ServerStream
}

type mumaxGetTypeInfoServer struct {
	grpc.ServerStream
}

func (x *mumaxGetTypeInfoServer) Send(m *Identifier) error {
	return x.ServerStream.SendMsg(m)
}

func _Mumax_Call_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FunctionCall)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).Call(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_Call_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).Call(ctx, req.(*FunctionCall))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_CallMethod_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MethodCall)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).CallMethod(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_CallMethod_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).CallMethod(ctx, req.(*MethodCall))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_ReverseCommunication_Handler(srv interface{}, stream grpc.ServerStream) error {
	return srv.(MumaxServer).ReverseCommunication(&mumaxReverseCommunicationServer{stream})
}

type Mumax_ReverseCommunicationServer interface {
	Send(*RevComRequest) error
	Recv() (*RevComResult, error)
	grpc.ServerStream
}

type mumaxReverseCommunicationServer struct {
	grpc.ServerStream
}

func (x *mumaxReverseCommunicationServer) Send(m *RevComRequest) error {
	return x.ServerStream.SendMsg(m)
}

func (x *mumaxReverseCommunicationServer) Recv() (*RevComResult, error) {
	m := new(RevComResult)
	if err := x.ServerStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func _Mumax_GetBool_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxObject)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetBool(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetBool_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetBool(ctx, req.(*MumaxObject))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetInt_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxObject)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetInt(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetInt_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetInt(ctx, req.(*MumaxObject))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetString_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxObject)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetString(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetString_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetString(ctx, req.(*MumaxObject))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetDouble_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxObject)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetDouble(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetDouble_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetDouble(ctx, req.(*MumaxObject))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_SetBool_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BoolSet)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).SetBool(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_SetBool_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).SetBool(ctx, req.(*BoolSet))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_SetInt_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(IntSet)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).SetInt(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_SetInt_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).SetInt(ctx, req.(*IntSet))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_SetDouble_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(DoubleSet)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).SetDouble(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_SetDouble_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).SetDouble(ctx, req.(*DoubleSet))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_SetString_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(StringSet)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).SetString(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_SetString_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).SetString(ctx, req.(*StringSet))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_SetVector_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(VectorSet)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).SetVector(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_SetVector_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).SetVector(ctx, req.(*VectorSet))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_SetScalarFunction_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ScalarFunctionSet)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).SetScalarFunction(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_SetScalarFunction_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).SetScalarFunction(ctx, req.(*ScalarFunctionSet))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_SetVectorFunction_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(VectorFunctionSet)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).SetVectorFunction(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_SetVectorFunction_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).SetVectorFunction(ctx, req.(*VectorFunctionSet))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_SetMumax_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxSet)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).SetMumax(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_SetMumax_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).SetMumax(ctx, req.(*MumaxSet))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetFieldBool_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxField)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetFieldBool(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetFieldBool_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetFieldBool(ctx, req.(*MumaxField))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetFieldInt_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxField)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetFieldInt(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetFieldInt_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetFieldInt(ctx, req.(*MumaxField))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetFieldString_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxField)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetFieldString(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetFieldString_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetFieldString(ctx, req.(*MumaxField))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetFieldDouble_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxField)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetFieldDouble(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetFieldDouble_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetFieldDouble(ctx, req.(*MumaxField))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_GetFieldMumax_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxField)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).GetFieldMumax(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_GetFieldMumax_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).GetFieldMumax(ctx, req.(*MumaxField))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_DestroyMumax_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MumaxObject)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).DestroyMumax(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_DestroyMumax_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).DestroyMumax(ctx, req.(*MumaxObject))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_NewSlice_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Slice)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).NewSlice(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_NewSlice_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).NewSlice(ctx, req.(*Slice))
	}
	return interceptor(ctx, in, info, handler)
}

func _Mumax_NewGPUSlice_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GPUSliceRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MumaxServer).NewGPUSlice(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Mumax_NewGPUSlice_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MumaxServer).NewGPUSlice(ctx, req.(*GPUSliceRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Mumax_ServiceDesc is the grpc.ServiceDesc for Mumax service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Mumax_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "mumaxpy.mumax",
	HandlerType: (*MumaxServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Eval",
			Handler:    _Mumax_Eval_Handler,
		},
		{
			MethodName: "Call",
			Handler:    _Mumax_Call_Handler,
		},
		{
			MethodName: "CallMethod",
			Handler:    _Mumax_CallMethod_Handler,
		},
		{
			MethodName: "GetBool",
			Handler:    _Mumax_GetBool_Handler,
		},
		{
			MethodName: "GetInt",
			Handler:    _Mumax_GetInt_Handler,
		},
		{
			MethodName: "GetString",
			Handler:    _Mumax_GetString_Handler,
		},
		{
			MethodName: "GetDouble",
			Handler:    _Mumax_GetDouble_Handler,
		},
		{
			MethodName: "SetBool",
			Handler:    _Mumax_SetBool_Handler,
		},
		{
			MethodName: "SetInt",
			Handler:    _Mumax_SetInt_Handler,
		},
		{
			MethodName: "SetDouble",
			Handler:    _Mumax_SetDouble_Handler,
		},
		{
			MethodName: "SetString",
			Handler:    _Mumax_SetString_Handler,
		},
		{
			MethodName: "SetVector",
			Handler:    _Mumax_SetVector_Handler,
		},
		{
			MethodName: "SetScalarFunction",
			Handler:    _Mumax_SetScalarFunction_Handler,
		},
		{
			MethodName: "SetVectorFunction",
			Handler:    _Mumax_SetVectorFunction_Handler,
		},
		{
			MethodName: "SetMumax",
			Handler:    _Mumax_SetMumax_Handler,
		},
		{
			MethodName: "GetFieldBool",
			Handler:    _Mumax_GetFieldBool_Handler,
		},
		{
			MethodName: "GetFieldInt",
			Handler:    _Mumax_GetFieldInt_Handler,
		},
		{
			MethodName: "GetFieldString",
			Handler:    _Mumax_GetFieldString_Handler,
		},
		{
			MethodName: "GetFieldDouble",
			Handler:    _Mumax_GetFieldDouble_Handler,
		},
		{
			MethodName: "GetFieldMumax",
			Handler:    _Mumax_GetFieldMumax_Handler,
		},
		{
			MethodName: "DestroyMumax",
			Handler:    _Mumax_DestroyMumax_Handler,
		},
		{
			MethodName: "NewSlice",
			Handler:    _Mumax_NewSlice_Handler,
		},
		{
			MethodName: "NewGPUSlice",
			Handler:    _Mumax_NewGPUSlice_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "GetIdentifiers",
			Handler:       _Mumax_GetIdentifiers_Handler,
			ServerStreams: true,
		},
		{
			StreamName:    "GetTypeInfo",
			Handler:       _Mumax_GetTypeInfo_Handler,
			ServerStreams: true,
		},
		{
			StreamName:    "ReverseCommunication",
			Handler:       _Mumax_ReverseCommunication_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
	},
	Metadata: "mumax.proto",
}
