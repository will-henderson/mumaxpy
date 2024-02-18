package interfacing

import (
	"reflect"

	en "github.com/mumax/3/engine"
	"github.com/mumax/3/script"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

func getObj(in *pb.MumaxObject) reflect.Value {

	var ret reflect.Value
	switch id := in.Identity.(type) {
	case *pb.MumaxObject_Name:
		ret = reflect.ValueOf(en.World.Identifiers[id.Name].Eval())
	case *pb.MumaxObject_Ptr:
		ret = dynamicObjects[id.Ptr]
	}

	return ret
}

func GetBool(in *pb.MumaxObject) (*pb.BOOL, error) {
	return &pb.BOOL{S: getObj(in).Bool()}, nil
}

func GetDouble(in *pb.MumaxObject) (*pb.DOUBLE, error) {
	return &pb.DOUBLE{S: getObj(in).Float()}, nil
}

func GetInt(in *pb.MumaxObject) (*pb.INT, error) {
	return &pb.INT{S: getObj(in).Int()}, nil
}

func GetString(in *pb.MumaxObject) (*pb.STRING, error) {
	return &pb.STRING{S: getObj(in).String()}, nil
}

func GetFieldBool(in *pb.MumaxField) (*pb.BOOL, error) {
	return &pb.BOOL{S: getObj(in.Mmobj).FieldByName(in.FieldName).Bool()}, nil
}

func GetFieldDouble(in *pb.MumaxField) (*pb.DOUBLE, error) {
	return &pb.DOUBLE{S: getObj(in.Mmobj).FieldByName(in.FieldName).Float()}, nil
}

func GetFieldInt(in *pb.MumaxField) (*pb.INT, error) {
	return &pb.INT{S: getObj(in.Mmobj).FieldByName(in.FieldName).Int()}, nil
}

func GetFieldString(in *pb.MumaxField) (*pb.STRING, error) {
	return &pb.STRING{S: getObj(in.Mmobj).FieldByName(in.FieldName).String()}, nil
}

func GetFieldMumax(in *pb.MumaxField) (*pb.MumaxObject, error) {
	dynamicObjects[dynamicCount] = getObj(in.Mmobj).FieldByName(in.FieldName)
	dynamicCount++
	return &pb.MumaxObject{Identity: &pb.MumaxObject_Ptr{Ptr: dynamicCount}}, nil
}

func SetBool(in *pb.BoolSet) (*pb.NULL, error) {
	//assume we are calling this for an identifier
	lhs := en.World.Identifiers[in.Mmobj.Identity.(*pb.MumaxObject_Name).Name].(script.LValue)
	Execute(func() interface{} { lhs.SetValue(in.S); return nil })
	return &pb.NULL{}, nil
}

func SetDouble(in *pb.DoubleSet) (*pb.NULL, error) {
	//assume we are calling this for an identifier
	lhs := en.World.Identifiers[in.Mmobj.Identity.(*pb.MumaxObject_Name).Name].(script.LValue)
	Execute(func() interface{} { lhs.SetValue(in.S); return nil }) //does actually matter whether float32 or float64
	return &pb.NULL{}, nil
}

func SetInt(in *pb.IntSet) (*pb.NULL, error) {
	//assume we are calling this for an identifier
	lhs := en.World.Identifiers[in.Mmobj.Identity.(*pb.MumaxObject_Name).Name].(script.LValue)
	Execute(func() interface{} { lhs.SetValue(int(in.S)); return nil })
	return &pb.NULL{}, nil
}

func SetString(in *pb.StringSet) (*pb.NULL, error) {
	//assume we are calling this for an identifier
	lhs := en.World.Identifiers[in.Mmobj.Identity.(*pb.MumaxObject_Name).Name].(script.LValue)
	Execute(func() interface{} { lhs.SetValue(in.S); return nil })
	return &pb.NULL{}, nil
}

func SetVector(in *pb.VectorSet) (*pb.NULL, error) {
	lhs := en.World.Identifiers[in.Mmobj.Identity.(*pb.MumaxObject_Name).Name].(script.LValue)
	Execute(func() interface{} { lhs.SetValue([3]float64{in.X, in.Y, in.Z}); return nil })
	return &pb.NULL{}, nil
}

func SetMumax(in *pb.MumaxSet) (*pb.NULL, error) {
	//again, assume that this is an indentifier!!!
	lhs := en.World.Identifiers[in.Mmobj.Identity.(*pb.MumaxObject_Name).Name].(script.LValue)

	var interf interface{}
	switch id := in.S.Identity.(type) {
	case *pb.MumaxObject_Name:
		interf = reflect.ValueOf(en.World.Identifiers[id.Name].Eval()).Interface()
	case *pb.MumaxObject_Ptr:
		interf = dynamicObjects[id.Ptr].Interface()
	}

	Execute(func() interface{} { lhs.SetValue(interf); return nil })
	return &pb.NULL{}, nil
}
