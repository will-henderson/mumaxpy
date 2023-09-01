package main

import (
	"context"

	en "github.com/mumax/3/engine"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

func (e *mumax) Eval(ctx context.Context, cmd *pb.STRING) (res *pb.NULL, err error) {

	tree, err := en.World.Compile(cmd.S)
	if err != nil {
		return &pb.NULL{}, err
	} else {
		Execute(func() interface{} { return tree.Eval() })
		return &pb.NULL{}, nil
	}
}
