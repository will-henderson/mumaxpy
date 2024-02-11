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
	<-PyQuantDone[c.funcno]
	return
}

func (c *py_quant) NComp() int { return c.ncomp }
