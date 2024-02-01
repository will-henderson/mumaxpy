package main

import (
	"context"
	"os"
	"reflect"
	"syscall"
	"unsafe"

	"github.com/mumax/3/data"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

const devShm = "/run/shm/"

func (e *mumax) NewSlice(ctx context.Context, in *pb.Slice) (*pb.MumaxObject, error) {
	compsize := in.Nx * in.Ny * in.Nz * 4
	totalsize := in.Ncomp * compsize

	f, err := os.OpenFile(devShm+in.File, os.O_RDWR, 0777)
	if err != nil {
		panic(err)
	}

	bytes, err := syscall.Mmap(int(f.Fd()), 0, int(totalsize), syscall.PROT_READ|syscall.PROT_WRITE, syscall.MAP_SHARED)
	if err != nil {
		panic(err)
	}

	originPtr := uintptr(unsafe.Pointer(unsafe.SliceData(bytes)))
	ptrs := make([]unsafe.Pointer, in.Ncomp)
	for c := int64(0); c < in.Ncomp; c++ {
		ptrs[c] = unsafe.Pointer(originPtr + uintptr(c*compsize))
	}

	sl := data.SliceFromPtrs([3]int{int(in.Nx), int(in.Ny), int(in.Nz)}, data.CPUMemory, ptrs)

	return AddDynamicObject(reflect.ValueOf(sl)), nil
}
