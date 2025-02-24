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

var Flag_socket = flag.String("socket", "mumaxpy.sock", "socket address")

type mumax struct {
	pb.UnimplementedMumaxServer
}

func main() {
	flag.Parse()

	go Run()

	os.Remove(*Flag_socket)
	listener, err := net.Listen("unix", *Flag_socket)
	if err != nil {
		panic(err)
	}

	sigs := make(chan os.Signal, 10)
	signal.Notify(sigs, os.Interrupt, syscall.SIGTERM)
	go func() {
		sig := <-sigs
		switch sig {
		case os.Interrupt:
			println("Interrupted")
			en.Break()
		case syscall.SIGTERM:
			en.Close()
			listener.Close()
			os.Remove(*Flag_socket)
			os.Exit(0)
		}
	}()

	defer en.Close()
	defer listener.Close()
	defer os.Remove(*Flag_socket)

	grpcServer := grpc.NewServer(grpc.UnaryInterceptor(RecoveryUnaryInterceptor), grpc.StreamInterceptor(RecoveryStreamInterceptor))
	server := &mumax{}
	pb.RegisterMumaxServer(grpcServer, server)
	grpcServer.Serve(listener)

}
