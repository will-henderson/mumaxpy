package main

import (
	"context"
	"reflect"
	"unsafe"

	"github.com/mumax/3/cuda"
	"github.com/mumax/3/data"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

//#cgo LDFLAGS: -L –lcudart -lcuda
//#cgo LDFLAGS:-L/usr/local/cuda/lib64/stubs/
//#cgo CFLAGS: -I/u
//#cgo LDFLAGS:-L/usr/lib/x86_64-linux-gnu/
//#cgo CFLAGS: -I/usr/include
//#include <cuda.h>
//#include <cuda_runtime_api.h>
import "C"

func (e *mumax) GPUSlice(ctx context.Context, in *pb.GPUSliceRequest) (*pb.GPUSlice, error) {
	sl := cuda.NewSlice(int(in.Ncomp), [3]int{int(in.Nx), int(in.Ny), int(in.Nz)})
	handle := getHandles(sl)
	mmobj := AddDynamicObject(reflect.ValueOf(sl))

	return &pb.GPUSlice{Mmobj: mmobj, Handle: handle}, nil
}

func getHandles(sl *data.Slice) [][]byte {
	//probably want to check that he lives on the GPU
	handle_bytes := make([][]byte, sl.NComp())
	if sl.GPUAccess() {
		for comp := 0; comp < sl.NComp(); comp++ {
			ptr := sl.DevPtr(comp)
			var handle C.cudaIpcMemHandle_t
			C.cudaIpcGetMemHandle(&handle, ptr)
			handle_bytes[comp] = C.GoBytes(unsafe.Pointer(&handle), C.CUDA_IPC_HANDLE_SIZE)
			// we would then like to process this into a byte string that we can send to python

		}
	}

	return handle_bytes
}
