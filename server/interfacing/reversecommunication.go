package interfacing

import (
	"io"

	pb "github.com/will-henderson/mumaxpy/protocol"
)

/*
Reverse communication. When a python function is passed as a scalar/vector function
argument to mumax, it is set up such that when this scalar function is evaluated
by the calculator, an int, representing which particular scalar function has been passed,
is sent on the ScalarFunctionRequest channel. This forwards this int on to the python
side, which calculates the value of the scalar field (optionally calling other
mumax functions as part of this), and returns the result over the grpc stream.

This is then sent on the return channel to give the result of the Eval call
to the calculator.

*/

var ScalarFunctionRequest = make(chan int)
var VectorFunctionRequest = make(chan int)

var RevComRequests = make(chan int)

var ScalarFunctionResults [](chan float64)
var VectorFunctionResults [](chan [3]float64)

func RevComReceiver(stream pb.Mumax_ReverseCommunicationServer) error {
	for {
		result, err := stream.Recv()
		if err == io.EOF { //this kills all the go routines sending responses
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
		_ = func_no
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

// and we also have a separate stream for pyquants.
// since these are a little more complicated.

var PyQuantRequest = make(chan *pb.RevComQuantRequest)
var PyQuantDone [](chan struct{})
var RevComQuantRequests = make(chan int)

func PyQuantRequester(stream pb.Mumax_ReverseCommunicationQuantitiesServer) error {
	for {
		request := <-PyQuantRequest
		if request == nil {
			return nil
		}

		stream.Send(request)
		RevComQuantRequests <- int(request.Funcno)
	}
}

func RevComQuantReceiver(stream pb.Mumax_ReverseCommunicationQuantitiesServer) error {
	for {
		_, err := stream.Recv()
		if err == io.EOF { //this kills all the go routines sending responses
			PyQuantRequest <- nil
			return nil
		}
		func_no := <-RevComQuantRequests
		PyQuantDone[func_no] <- struct{}{}
	}
}

func (e *mumax) ReverseCommunicationQuantities(stream pb.Mumax_ReverseCommunicationQuantitiesServer) error {

	go PyQuantRequester(stream)
	err := RevComQuantReceiver(stream)
	return err
}
