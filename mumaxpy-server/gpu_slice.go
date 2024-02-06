package main

import (
	"context"
	"errors"
	"fmt"
	"reflect"
	"strconv"
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
//#include "gpu_slice.h"
import "C"

func (e *mumax) NewGPUSlice(ctx context.Context, in *pb.GPUSlice) (*pb.MumaxObject, error) {

	compsize := in.Nx * in.Ny * in.Nz * 4

	//write well firstly this probably needs to come from the right context

	if len(in.Handle) != C.CUDA_IPC_HANDLE_SIZE {
		return nil, errors.New("gpu memory handle is not the right length, got" + strconv.Itoa(len(in.Handle)))
	}

	//well, we need to call this from the right thread anyway

	var err C.int

	//try on stack?
	var b_handle [64]byte
	for i := 0; i < 64; i++ {
		b_handle[i] = in.Handle[i]
		fmt.Printf("%x", in.Handle[i])
		fmt.Printf(" ")
	}

	//ptr := Execute(func() interface{} { return C.open_mem_handle(unsafe.Pointer(&b_handle[0]), &err) })
	ptr := C.open_mem_handle(unsafe.Pointer(&b_handle[0]), &err)

	if err != 0 {
		print("there is an error:", err, ",     ")
	} else {
		print("no error apparently")
	}

	//originPtr := uintptr(ptr.(unsafe.Pointer))
	originPtr := uintptr(ptr)

	ptrs := make([]unsafe.Pointer, in.Ncomp)
	for c := int64(0); c < in.Ncomp; c++ {
		ptrs[c] = unsafe.Pointer(originPtr + uintptr(c*compsize))
	}

	sl := data.SliceFromPtrs([3]int{int(in.Nx), int(in.Ny), int(in.Nz)}, data.GPUMemory, ptrs)

	//lets do some tests here
	print(sl.NComp())
	print(sl.GPUAccess())
	print(cuda.GetCell(sl, 0, 0, 0, 0))

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
