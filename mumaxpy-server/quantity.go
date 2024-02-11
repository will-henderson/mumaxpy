package main

import (
	"reflect"

	"github.com/mumax/3/data"
	en "github.com/mumax/3/engine"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

func processQuantity(s *pb.Quantity) (reflect.Value, error) {

	switch value := s.Q.(type) {
	case *pb.Quantity_Mmobj:
		obj := getObj(value.Mmobj)
		return obj, nil

	case *pb.Quantity_Gocode:
		expr, err := en.World.CompileExpr(value.Gocode)
		if err != nil {
			return reflect.ValueOf(nil), err
		}
		quantity, ok := expr.Eval().(en.Quantity)
		if !ok {
			panic("couldn't cast to quantity")
		}
		return reflect.ValueOf(quantity), nil

	case *pb.Quantity_Py:
		PyQuantDone = append(PyQuantDone, make(chan struct{}))
		quantity := &py_quant{int(value.Py.Funcno), int(value.Py.Ncomp)}
		return reflect.ValueOf(quantity), nil
	}
	return reflect.ValueOf(nil), nil //never get here
}

type py_quant struct {
	funcno int
	ncomp  int
}

func (c *py_quant) EvalTo(dst *data.Slice) {
	gpu_msg := getHandles(dst)
	PyQuantRequest <- &pb.RevComQuantRequest{Funcno: int64(c.funcno), Sl: gpu_msg}

	//when this is called we are in the main goroutine.
	//we would really like to free up the main goroutine here to allow other function calls in the meantime.
	// what we could do is handle Execution in here

	go returnwatcher(c.funcno)
	HandleOtherCalls()
}

func returnwatcher(funcno int) {
	<-PyQuantDone[funcno]
	Inject <- InjectType{nil, -1}
}

func (c *py_quant) NComp() int { return c.ncomp }
