package main

import (
	"flag"
	"net"
	"os"
	"os/signal"
	"syscall"

	en "github.com/mumax/3/engine"
	pb "github.com/will-henderson/mumaxpy/protocol"
	"google.golang.org/grpc"
)

var socket_address = "mumaxpy.sock"

type mumax struct {
	pb.UnimplementedMumaxServer
}

func main() {
	flag.Parse()

	go Run()

	os.Remove(socket_address)
	listener, err := net.Listen("unix", socket_address)
	if err != nil {
		panic(err)
	}

	sigs := make(chan os.Signal, 10)
	signal.Notify(sigs, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-sigs

		en.Close()
		listener.Close()
		os.Remove(socket_address)
		os.Exit(0)
	}()

	defer en.Close()
	defer listener.Close()
	defer os.Remove(socket_address)

	grpcServer := grpc.NewServer(grpc.UnaryInterceptor(RecoveryUnaryInterceptor), grpc.StreamInterceptor(RecoveryStreamInterceptor))
	server := &mumax{}
	print("server here?")
	pb.RegisterMumaxServer(grpcServer, server)
	grpcServer.Serve(listener)

}
