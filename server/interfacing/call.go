package interfacing

import (
	"reflect"

	"github.com/mumax/3/data"
	en "github.com/mumax/3/engine"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

func Call(in *pb.FunctionCall) (*pb.CallResponse, error) {

	function := reflect.ValueOf(en.World.Identifiers[in.Name].Eval())
	fType := function.Type()

	argv := GetArgv(fType, in)

	outs := Execute(func() interface{} { return function.Call(argv) })

	return MakeOutput(fType, outs.([]reflect.Value)), nil
}

func CallMethod(in *pb.MethodCall) (*pb.CallResponse, error) {

	var item reflect.Value
	switch id := in.Mmobj.Identity.(type) {
	case *pb.MumaxObject_Name:
		item = reflect.ValueOf(en.World.Identifiers[id.Name].Eval())
	case *pb.MumaxObject_Ptr:
		item = dynamicObjects[id.Ptr]
	}

	fCall := in.Fc
	function := item.MethodByName(fCall.Name)
	fType := function.Type()

	argv := GetArgv(fType, fCall)
	outs := Execute(func() interface{} { return function.Call(argv) })
	return MakeOutput(fType, outs.([]reflect.Value)), nil
}

func GetArgv(fType reflect.Type, in *pb.FunctionCall) (argv []reflect.Value) {

	numArgs := fType.NumIn()
	argtypes := make([]string, numArgs)
	for i := 0; i < fType.NumIn(); i++ {
		argtypes[i] = fType.In(i).String()
	}

	argv = make([]reflect.Value, numArgs)
	for i := 0; i < numArgs; i++ {
		switch argtypes[i] {
		case "int":
			argv[i] = reflect.ValueOf(int(in.ArgInt[0]))
			in.ArgInt = in.ArgInt[1:]
		case "float64":
			argv[i] = reflect.ValueOf(in.ArgDouble[0])
			in.ArgDouble = in.ArgDouble[1:]
		case "string":
			argv[i] = reflect.ValueOf(in.ArgString[0])
			in.ArgString = in.ArgString[1:]
		case "bool":
			argv[i] = reflect.ValueOf(in.ArgBool[0])
			in.ArgBool = in.ArgBool[1:]
		case "script.ScalarFunction":
			sf, _ := processScalarFunction(in.ArgScalarFunction[0])
			argv[i] = reflect.ValueOf(sf)
			in.ArgScalarFunction = in.ArgScalarFunction[1:]
		case "script.VectorFunction":
			vf, _ := processVectorFunction(in.ArgVectorFunction[0])
			argv[i] = reflect.ValueOf(vf)
			in.ArgVectorFunction = in.ArgVectorFunction[1:]
		case "engine.Quantity":
			argv[i], _ = processQuantity(in.ArgQuantity[0])
			in.ArgQuantity = in.ArgQuantity[1:]
		case "data.Vector":
			argv[i] = reflect.ValueOf(data.Vector{in.ArgDouble[0], in.ArgDouble[1], in.ArgDouble[2]})
			in.ArgDouble = in.ArgDouble[3:]
		default:
			argv[i] = getObj(in.ArgMumax[0])
			in.ArgMumax = in.ArgMumax[1:]
		}
	}

	return argv
}

func MakeOutput(fType reflect.Type, outs []reflect.Value) *pb.CallResponse {

	ret := &pb.CallResponse{}

	for i := 0; i < len(outs); i++ {
		processOutput(outs[i], ret)
	}

	return ret
}

func processOutput(out reflect.Value, ret *pb.CallResponse) {

	if !(out.Kind() == reflect.Array || out.Kind() == reflect.Slice) {

		switch out.Type().String() {
		case "int":
			ret.OutInt = append(ret.OutInt, out.Int())
		case "float64", "float32":
			ret.OutDouble = append(ret.OutDouble, out.Float())
		case "string":
			ret.OutString = append(ret.OutString, out.String())
		case "bool":
			ret.OutBool = append(ret.OutBool, out.Bool())
		default:
			ret.OutMumax = append(ret.OutMumax, AddDynamicObject(out))
		}
	} else {
		ret.OutArray = append(ret.OutArray, processArray(out))
	}
}

func processArray(arr reflect.Value) *pb.Array {

	t := arr.Type().Elem()
	n := arr.Len()

	if !(t.Kind() == reflect.Array || t.Kind() == reflect.Slice) {

		switch t.String() {
		case "int":
			s := &pb.INTs{S: make([]int64, n)}
			for i := 0; i < n; i++ {
				s.S[i] = arr.Index(i).Int()
			}
			return &pb.Array{Elements: &pb.Array_I{I: s}}
		case "float64", "float32":
			s := &pb.DOUBLEs{S: make([]float64, n)}
			for i := 0; i < n; i++ {
				s.S[i] = arr.Index(i).Float()
			}
			return &pb.Array{Elements: &pb.Array_D{D: s}}
		case "string":
			s := &pb.STRINGs{S: make([]string, n)}
			for i := 0; i < n; i++ {
				s.S[i] = arr.Index(i).String()
			}
			return &pb.Array{Elements: &pb.Array_S{S: s}}
		case "bool":
			s := &pb.BOOLs{S: make([]bool, n)}
			for i := 0; i < n; i++ {
				s.S[i] = arr.Index(i).Bool()
			}
			return &pb.Array{Elements: &pb.Array_B{B: s}}
		default:
			s := &pb.MumaxObjects{S: make([]*pb.MumaxObject, n)}
			for i := 0; i < n; i++ {
				s.S[i] = AddDynamicObject(arr.Index(i))
			}
			return &pb.Array{Elements: &pb.Array_O{O: s}}
		}
	}

	s := &pb.Arrays{S: make([]*pb.Array, n)}
	for i := 0; i < n; i++ {
		s.S[i] = processArray(arr.Index(i))
	}
	return &pb.Array{Elements: &pb.Array_A{A: s}}

}
