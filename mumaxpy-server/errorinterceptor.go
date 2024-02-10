package main

import (
	"context"
	"fmt"
	"runtime"

	"google.golang.org/grpc"
)

type RecoveryHandlerFuncContext func(ctx context.Context, p any) (err error)

func RecoveryUnaryInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (_ any, err error) {

	defer func() {
		if r := recover(); r != nil {
			err = recoverFrom(ctx, r)
		}
	}()

	return handler(ctx, req)
}

func RecoveryStreamInterceptor(srv any, stream grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) (err error) {
	defer func() {
		if r := recover(); r != nil {
			err = recoverFrom(stream.Context(), r)
		}
	}()

	return handler(srv, stream)
}

func recoverFrom(ctx context.Context, p any) error {
	stack := make([]byte, 64<<10)
	stack = stack[:runtime.Stack(stack, false)]
	return &PanicError{Panic: p, Stack: stack}
}

type PanicError struct {
	Panic any
	Stack []byte
}

func (e *PanicError) Error() string {
	return fmt.Sprintf("panic caught: %v\n\n%s", e.Panic, e.Stack) //useful in development but over-verbose
	//return fmt.Sprintf("panic caught: %v", e.Panic)
}
