package main

import (
	"C"

	en "github.com/mumax/3/engine"
	mmif "github.com/will-henderson/mumaxpy/server/interfacing"
)

// really want to pas in something that would be the equiv of flags here.
//
//export InitialiseMumax
func InitialiseMumax() {
	go mmif.Run()
}

//export CloseMumax
func CloseMumax() {
	en.Close()
}
