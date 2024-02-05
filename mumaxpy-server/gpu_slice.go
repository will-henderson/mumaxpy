package main

import (
	"context"
	"reflect"
	"unsafe"

	"github.com/mumax/3/cuda"
	"github.com/mumax/3/data"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

//#cgo CFLAGS: -I /usr/include
//#cgo LDFLAGS: -L/usr/lib/x86_64-linux-gnu -lcuda -lcudart
//// DOCKER IMAGE
//#cgo CFLAGS: -I /usr/local/cuda-11.7/targets/x86_64-linux/include/
//#cgo LDFLAGS:-L /usr/local/cuda-11.7/targets/x86_64-linux/lib/
//#include <cuda.h>
//#include <cuda_runtime_api.h>
import "C"

func (e *mumax) GPUSlice(ctx context.Context, in *pb.GPUSlice) (*pb.MumaxObject, error) {

	compsize = in.Nx * in.Ny * in.Nz * 4

	var pointer
	c_handle = C.cudaIpcMemHandle_t(in.handle)

	C.cudaIpcOpenMemHandle(&pointer, c_handle, C.uint(1))
	originPtr := uintptr(*pointer2pointer) 

	ptrs := make([]unsafe.Pointer, in.Ncomp)

	sl := cuda.NewSlice(int(in.Ncomp), [3]int{int(in.Nx), int(in.Ny), int(in.Nz)})

	return AddDynamicObject(reflect.ValueOf(sl)), nil
}

//probably want to check we free it correctly.

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
