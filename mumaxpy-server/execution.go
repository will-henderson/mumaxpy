package main

import (
	"flag"
	"fmt"
	"os"
	"path"

	"github.com/mumax/3/cuda"
	"github.com/mumax/3/data"
	en "github.com/mumax/3/engine"
	"github.com/mumax/3/util"
)

//because cuda wants all communication from a single thread, but grpc uses
//one goroutine per method call, we need to route anything that might call
//cuda into a specific goroutine.

var Inject = make(chan func() interface{})

type InjectResponseType struct {
	result interface{}
	err    interface{}
}

var InjectResponse = make(chan InjectResponseType)

func Run() {
	flag.Parse()
	cuda.Init(*en.Flag_gpu)
	fmt.Println(cuda.GPUInfo)

	od := *en.Flag_od
	if od == "" {
		od = path.Base(os.Args[0]) + ".out"
	}

	en.InitIO(util.NoExt(od), od, *en.Flag_forceclean)
	extraDeclarations()

	defer func() {
		if r := recover(); r != nil {
			InjectResponse <- InjectResponseType{nil, r}
		}
		loop()
	}()

	loop()
}

func loop() {
	for {
		f := <-Inject
		InjectResponse <- InjectResponseType{f(), nil}
	}
}

func Execute(f func() interface{}) interface{} {
	Inject <- f
	resp := <-InjectResponse
	if resp.err != nil {
		panic(resp.err)
	}
	return resp.result
}

func device() int {
	return *en.Flag_gpu
}

func extraDeclarations() {
	en.DeclFunc("SliceCopy", data.Copy, "copies data from one slice into another")
	en.DeclFunc("Recycle", cuda.Recycle, "returns a buffer obtained from GetBuffer to the pool")
	en.DeclFunc("ValueOf", en.ValueOf, "returns the GPU slice representation of a quantity")
	en.DeclFunc("Device", device, "returns the cuda device number")
}
