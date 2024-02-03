package main

import (
	"context"
	"io"

	pb "github.com/will-henderson/mumaxpy/protocol"
)

var ScalarFunctionRequest = make(chan int)
var VectorFunctionRequest = make(chan int)

var RevComRequests = make(chan int)

var ScalarFunctionResults [](chan float64)
var VectorFunctionResults [](chan [3]float64)

func RevComReceiver(stream pb.Mumax_ReverseCommunicationServer) {
	for {
		result, err := stream.Recv()
		if err == io.EOF {
			ScalarFunctionRequest <- -1
			VectorFunctionRequest <- -1
			return
		}
		func_no := <-RevComRequests

		switch value := result.Result.(type) {
		case *pb.RevComResult_Scalar:
			ScalarFunctionResults[func_no] <- value.Scalar
		default:
			vv := value.Vec
			VectorFunctionResults[func_no] <- [3]float64[value.X, value.Y, value.Z]
		}
	}

	_ = func_no

}

func (e *mumax) ScalarFuncHandler(stream pb.Mumax_ReverseCommunicationServer) {

	for {
		request := <-ScalarFunctionRequest
		if request == -1 {
			return nil
		}
		stream.Send(&pb.RevComRequest{Pyfunc: request})
		RevComRequest2 <- request
	}
}

func (e *mumax) ReverseCommunication(ctx context.Context, stream pb.Mumax_ReverseCommunicationServer) error {

	go ScalarFuncHandler(stream)

	for {
		result, err := stream.Recv()
		if err == io.EOF {
			RevComRequest <- -1
			return
		}
		pf := <-RevComRequest2
		pyfuncs[pf] <- result
	}
}
