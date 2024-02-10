package main

import (
	"context"
	"errors"
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

	sl, err := newGPUSlice(in)
	return AddDynamicObject(reflect.ValueOf(sl)), err
}

func newGPUSlice(in *pb.GPUSlice) (*data.Slice, error) {

	compsize := in.Nx * in.Ny * in.Nz * 4

	if len(in.Handle) != C.CUDA_IPC_HANDLE_SIZE {
		return nil, errors.New("gpu memory handle is not the right length, got" + strconv.Itoa(len(in.Handle)))
	}

	var err C.int
	ptr := C.open_mem_handle((*C.char)(unsafe.Pointer(&in.Handle[0])), &err)

	if err != 0 {
		//panic here!
		print("fuck")
	}

	//originPtr := uintptr(ptr.(unsafe.Pointer))
	originPtr := uintptr(ptr)

	ptrs := make([]unsafe.Pointer, in.Ncomp)
	for c := int64(0); c < in.Ncomp; c++ {
		ptrs[c] = unsafe.Pointer(originPtr + uintptr(c*compsize))
	}

	sl := data.SliceFromPtrs([3]int{int(in.Nx), int(in.Ny), int(in.Nz)}, data.GPUMemory, ptrs)
	return sl, nil
}

func getHandles(sl *data.Slice) *pb.GPUSliceMM {

	ncomp := sl.NComp()
	size := sl.Size()

	if !sl.GPUAccess() {
		panic("slice needs GPU access to eval")
	}

	sl = cuda.Buffer(ncomp, size)
	handles := make([][]byte, ncomp)

	var err C.int

	for c := 0; c < ncomp; c++ {
		handles[c] = make([]byte, C.CUDA_IPC_HANDLE_SIZE)
		C.get_mem_handle((*C.char)(unsafe.Pointer(&handles[c][0])), sl.DevPtr(c), &err)

		if err != 0 {
			panic("couldn't share memory")
		}
	}

	msg := &pb.GPUSliceMM{Ncomp: int64(ncomp),
		Nx:      int64(size[0]),
		Ny:      int64(size[1]),
		Nz:      int64(size[2]),
		Handles: handles}

	return msg

}
