package interfacing

import (
	"reflect"

	pb "github.com/will-henderson/mumaxpy/protocol"
)

var dynamicCount uint32 = 0
var dynamicObjects = make(map[uint32]reflect.Value)

func AddDynamicObject(val reflect.Value) *pb.MumaxObject {
	dynamicObjects[dynamicCount] = val
	obj := &pb.MumaxObject{Identity: &pb.MumaxObject_Ptr{Ptr: dynamicCount}}

	dynamicCount++
	return obj
}

var documentation = NewDocumentation()
var typeMap = make(map[string]reflect.Type)

func AddType(t reflect.Type) {
	name := t.String()
	_, ok := typeMap[name]
	if !ok {
		typeMap[name] = t
	}
}

func DestroyMumax(in *pb.MumaxObject) (*pb.NULL, error) {

	switch id := in.Identity.(type) {
	case *pb.MumaxObject_Ptr:
		delete(dynamicObjects, id.Ptr)
	}

	return &pb.NULL{}, nil
}
