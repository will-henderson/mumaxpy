package main

import (
	"context"
	"reflect"

	"github.com/mumax/3/data"
	en "github.com/mumax/3/engine"
	"github.com/mumax/3/script"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

func (e *mumax) SetScalarFunction(ctx context.Context, in *pb.ScalarFunctionSet) (*pb.NULL, error) {
	lhs := en.World.Identifiers[in.Mmobj.Identity.(*pb.MumaxObject_Name).Name].(script.LValue)

	interf, err := processScalarFunction(in.S)
	if err != nil {
		return &pb.NULL{}, err
	}

	Execute(func() interface{} { lhs.SetValue(interf); return nil })
	return &pb.NULL{}, nil

}

func processScalarFunction(s *pb.ScalarFunction) (script.ScalarFunction, error) {

	switch value := s.Sf.(type) {
	case *pb.ScalarFunction_Scalar:
		return float_sf(value.Scalar), nil
	case *pb.ScalarFunction_Gocode:
		expr, err := en.World.CompileExpr(value.Gocode)
		if err != nil {
			return nil, err
		}
		return &go_sf{expr}, nil
	case *pb.ScalarFunction_Pyfunc:
		func_no := len(ScalarFunctionResults)
		ScalarFunctionResults = append(ScalarFunctionResults, make(chan float64))
		return &py_sf{func_no}, nil
	}
	return nil, nil //don't get to this line
}

func processVectorFunction(v *pb.VectorFunction) (script.VectorFunction, error) {
	switch value := v.Vf.(type) {
	case *pb.VectorFunction_Gocode:
		expr, err := en.World.CompileExpr(value.Gocode)
		if err != nil {
			return nil, err
		}
		return &go_vf{expr}, nil
	case *pb.VectorFunction_Pyfunc:
		func_no := len(VectorFunctionResults)
		VectorFunctionResults = append(VectorFunctionResults, make(chan [3]float64))
		return &py_vf{func_no}, nil
	case *pb.VectorFunction_Components:
		sf3 := value.Components
		var intercomp [3]script.ScalarFunction
		var err error
		for i, comp := range [3]*pb.ScalarFunction{sf3.X, sf3.Y, sf3.Z} {
			intercomp[i], err = processScalarFunction(comp)
			if err != nil {
				return nil, err
			}
		}
		return &comp_vf{intercomp}, nil
	}
	return nil, nil //don't get to this line.
}

func (e *mumax) SetVectorFunction(ctx context.Context, in *pb.VectorFunctionSet) (*pb.NULL, error) {
	lhs := en.World.Identifiers[in.Mmobj.Identity.(*pb.MumaxObject_Name).Name].(script.LValue)

	interf, err := processVectorFunction(in.S)
	if err != nil {
		return &pb.NULL{}, err
	}

	Execute(func() interface{} { lhs.SetValue(interf); return nil })
	return &pb.NULL{}, nil
}

type float_sf float64

func (l float_sf) Eval() interface{}    { return float64(l) }
func (l float_sf) Type() reflect.Type   { return reflect.TypeOf(float64(0)) }
func (l float_sf) Child() []script.Expr { return nil }
func (l float_sf) Fix() script.Expr     { return l }
func (l float_sf) Float() float64       { return float64(l) }

type go_sf struct {
	in script.Expr
}

func (c *go_sf) Eval() interface{}    { return c }
func (c *go_sf) Type() reflect.Type   { return script.ScalarFunction_t }
func (c *go_sf) Float() float64       { return c.in.Eval().(float64) }
func (c *go_sf) Child() []script.Expr { return []script.Expr{c.in} }
func (c *go_sf) Fix() script.Expr     { return &go_sf{in: c.in.Fix()} }

type py_sf struct {
	func_no int
}

func (c *py_sf) Eval() interface{} { return c }

func (c *py_sf) Type() reflect.Type { return script.ScalarFunction_t }
func (c *py_sf) Float() float64 {
	ScalarFunctionRequest <- c.func_no
	return <-ScalarFunctionResults[c.func_no]
}
func (c *py_sf) Child() []script.Expr { return []script.Expr{en.World.Resolve("t")} }
func (c *py_sf) Fix() script.Expr     { return c }

type py_vf struct {
	func_no int
}

func (c *py_vf) Eval() interface{}  { return c }
func (c *py_vf) Type() reflect.Type { return script.VectorFunction_t }
func (c *py_vf) Float3() data.Vector {
	VectorFunctionRequest <- c.func_no
	return <-VectorFunctionResults[c.func_no]
}
func (c *py_vf) Child() []script.Expr { return []script.Expr{en.World.Resolve("t")} }
func (c *py_vf) Fix() script.Expr     { return c }

type go_vf struct {
	in script.Expr
}

func (c *go_vf) Eval() interface{}    { return c }
func (c *go_vf) Type() reflect.Type   { return script.VectorFunction_t }
func (c *go_vf) Float3() data.Vector  { return c.in.Eval().(data.Vector) }
func (c *go_vf) Child() []script.Expr { return []script.Expr{c.in} }
func (c *go_vf) Fix() script.Expr     { return &go_vf{in: c.in.Fix()} }

type comp_vf struct {
	comps [3]script.ScalarFunction
}

func (c *comp_vf) Eval() interface{}  { return c }
func (c *comp_vf) Type() reflect.Type { return script.VectorFunction_t }

func (c *comp_vf) Child() []script.Expr {

	exprs := make([]script.Expr, 3)
	for i := 0; i < 3; i++ {
		exprs[i] = c.comps[i]
	}
	return exprs
}

func (c *comp_vf) Fix() script.Expr {
	var comps [3]script.ScalarFunction
	for i := 0; i < 3; i++ {
		comps[i] = &go_sf{c.comps[i].Fix()}
	}
	return &comp_vf{comps}
}

func (c *comp_vf) Float3() (vec data.Vector) {
	for i := 0; i < 3; i++ {
		vec[i] = c.comps[i].Eval().(float64)
	}
	return vec
}
