package main

import (
	"io"

	pb "github.com/will-henderson/mumaxpy/protocol"
)

var ScalarFunctionRequest = make(chan int)
var VectorFunctionRequest = make(chan int)

var RevComRequests = make(chan int)

var ScalarFunctionResults [](chan float64)
var VectorFunctionResults [](chan [3]float64)

func RevComReceiver(stream pb.Mumax_ReverseCommunicationServer) error {
	for {
		result, err := stream.Recv()
		if err == io.EOF {
			ScalarFunctionRequest <- -1
			VectorFunctionRequest <- -1
			return nil
		}
		func_no := <-RevComRequests

		switch value := result.Result.(type) {
		case *pb.RevComResult_Scalar:
			ScalarFunctionResults[func_no] <- value.Scalar
		case *pb.RevComResult_Vec:
			vv := value.Vec
			VectorFunctionResults[func_no] <- [3]float64{vv.X, vv.Y, vv.Z}
		}
	}
}

func ScalarRevComRequester(stream pb.Mumax_ReverseCommunicationServer) error {
	for {
		request := <-ScalarFunctionRequest
		if request == -1 {
			return nil
		}
		stream.Send(&pb.RevComRequest{Pyfunc: &pb.RevComRequest_Scalarpyfunc{Scalarpyfunc: int64(request)}})

		RevComRequests <- request
	}
}

func VectorRevComRequester(stream pb.Mumax_ReverseCommunicationServer) error {
	for {
		request := <-VectorFunctionRequest
		if request == -1 {
			return nil
		}
		stream.Send(&pb.RevComRequest{Pyfunc: &pb.RevComRequest_Vectorpyfunc{Vectorpyfunc: int64(request)}})
		RevComRequests <- request
	}
}

func (e *mumax) ReverseCommunication(stream pb.Mumax_ReverseCommunicationServer) error {

	go ScalarRevComRequester(stream)
	go VectorRevComRequester(stream)
	err := RevComReceiver(stream)
	return err
}
