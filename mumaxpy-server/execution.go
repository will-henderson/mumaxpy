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

var current_n int

type InjectType struct {
	f func() interface{}
	n int
}

var Inject = make(chan InjectType)

type InjectResponseType struct {
	result interface{}
	err    interface{}
}

var InjectResponse [](chan InjectResponseType)

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
			InjectResponse[current_n] <- InjectResponseType{nil, r}
		}
		loop()
	}()

	loop()
}

func loop() {
	for {
		inj := <-Inject
		InjectResponse[inj.n] <- InjectResponseType{inj.f(), nil}
	}
}

func Execute(f func() interface{}) interface{} {
	n := inject_channel()
	defer decrement_inject_channel()

	Inject <- InjectType{f, n}
	resp := <-InjectResponse[n]
	if resp.err != nil {
		panic(resp.err)
	}
	return resp.result
}

func inject_channel() int {

	n := current_n
	if len(InjectResponse) <= n {
		InjectResponse = append(InjectResponse, make(chan InjectResponseType))
	}

	current_n = current_n + 1

	return n
}

func decrement_inject_channel() {
	current_n = current_n - 1
}

func HandleOtherCalls() {
	for {
		inj := <-Inject
		if inj.n == -1 { //to break off this routine on a response
			return
		} else {
			InjectResponse[inj.n] <- InjectResponseType{inj.f(), nil}
		}
	}
}

func extraDeclarations() {
	en.DeclFunc("SliceCopy", data.Copy, "copies data from one slice into another")
	en.DeclFunc("Recycle", cuda.Recycle, "returns a buffer obtained from GetBuffer to the pool")
	en.DeclFunc("ValueOf", en.ValueOf, "returns the GPU slice representation of a quantity")
	en.DeclFunc("SetLLTorque", en.SetLLTorque, "sets dst to the current Landau-Lifshitz Torque")
	//and probably want to expose all the other things one would need to implement evolver python side.
}
