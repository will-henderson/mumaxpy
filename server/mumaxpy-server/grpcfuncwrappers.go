package main

import (
	"context"

	pb "github.com/will-henderson/mumaxpy/protocol"
	mmif "github.com/will-henderson/mumaxpy/server/interfacing"
)

func (e *mumax) Eval(ctx context.Context, cmd *pb.STRING) (res *pb.NULL, err error) {
	return mmif.Eval(cmd)
}

func (e *mumax) GetIdentifiers(in *pb.NULL, stream pb.Mumax_GetIdentifiersServer) error {
	ch := make(chan (*pb.Identifier))
	go mmif.GetIdentifiers(ch)

	for {
		tosend := <-ch
		if tosend == nil {
			return nil
		}
		err := stream.Send(tosend)
		if err != nil {
			return err
		}
	}
}

func (e *mumax) GetTypeInfo(in *pb.STRING, stream pb.Mumax_GetTypeInfoServer) error {

	ch := make(chan (*pb.Identifier))
	mmif.GetTypeInfo(in, ch)

	for {
		tosend := <-ch
		if tosend == nil {
			return nil
		}
		err := stream.Send(tosend)
		if err != nil {
			return err
		}
	}
}

func (e *mumax) Call(ctx context.Context, in *pb.FunctionCall) (*pb.CallResponse, error) {
	return mmif.Call(in)
}

func (e *mumax) CallMethod(ctx context.Context, in *pb.MethodCall) (*pb.CallResponse, error) {
	return mmif.CallMethod(in)
}

func (e *mumax) GetBool(ctx context.Context, in *pb.MumaxObject) (*pb.BOOL, error) {
	return mmif.GetBool(in)
}
func (e *mumax) GetInt(ctx context.Context, in *pb.MumaxObject) (*pb.INT, error) {
	return mmif.GetInt(in)
}
func (e *mumax) GetString(ctx context.Context, in *pb.MumaxObject) (*pb.STRING, error) {
	return mmif.GetString(in)
}
func (e *mumax) GetDouble(ctx context.Context, in *pb.MumaxObject) (*pb.DOUBLE, error) {
	return mmif.GetDouble(in)
}

func (e *mumax) SetBool(ctx context.Context, in *pb.BoolSet) (*pb.NULL, error) {
	return mmif.SetBool(in)
}
func (e *mumax) SetInt(ctx context.Context, in *pb.IntSet) (*pb.NULL, error) { return mmif.SetInt(in) }

func (e *mumax) SetDouble(ctx context.Context, in *pb.DoubleSet) (*pb.NULL, error) {
	return mmif.SetDouble(in)
}
func (e *mumax) SetString(ctx context.Context, in *pb.StringSet) (*pb.NULL, error) {
	return mmif.SetString(in)
}
func (e *mumax) SetVector(ctx context.Context, in *pb.VectorSet) (*pb.NULL, error) {
	return mmif.SetVector(in)
}
func (e *mumax) SetMumax(ctx context.Context, in *pb.MumaxSet) (*pb.NULL, error) {
	return mmif.SetMumax(in)
}
func (e *mumax) SetScalarFunction(ctx context.Context, in *pb.ScalarFunctionSet) (*pb.NULL, error) {
	return mmif.SetScalarFunction(in)
}
func (e *mumax) SetVectorFunction(ctx context.Context, in *pb.VectorFunctionSet) (*pb.NULL, error) {
	return mmif.SetVectorFunction(in)
}

func (e *mumax) GetFieldBool(ctx context.Context, in *pb.MumaxField) (*pb.BOOL, error) {
	return mmif.GetFieldBool(in)
}
func (e *mumax) GetFieldInt(ctx context.Context, in *pb.MumaxField) (*pb.INT, error) {
	return mmif.GetFieldInt(in)
}
func (e *mumax) GetFieldString(ctx context.Context, in *pb.MumaxField) (*pb.STRING, error) {
	return mmif.GetFieldString(in)
}
func (e *mumax) GetFieldDouble(ctx context.Context, in *pb.MumaxField) (*pb.DOUBLE, error) {
	return mmif.GetFieldDouble(in)
}
func (e *mumax) GetFieldMumax(ctx context.Context, in *pb.MumaxField) (*pb.MumaxObject, error) {
	return mmif.GetFieldMumax(in)
}

func (e *mumax) DestroyMumax(ctx context.Context, in *pb.MumaxObject) (*pb.NULL, error) {
	return mmif.DestroyMumax(in)
}

func (e *mumax) NewSlice(ctx context.Context, in *pb.Slice) (*pb.MumaxObject, error) {
	return mmif.NewSlice(in)
}

func (e *mumax) NewGPUSlice(ctx context.Context, in *pb.GPUSlice) (*pb.MumaxObject, error) {
	return mmif.NewGPUSlice(in)
}
