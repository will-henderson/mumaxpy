package main

/*
import "C"

func (e *mumax) GPUSlice(ctx context.Context, in *pb.GPUSlice) (*pb.MumaxObject, error) {

	compsize := in.Nx * in.Ny * in.Nz * 4

	if len(in.Handle) != C.CUDA_IPC_HANDLE_SIZE {
		return nil, errors.New("gpu memory handle is not the right length, got" + strconv.Itoa(len(in.Handle)))
	}

	ptr := C.open_mem_handle(unsafe.Pointer(&in.Handle[0]))

	fmt.Println("We apparently opened a memory handle")

	originPtr := uintptr(ptr)

	ptrs := make([]unsafe.Pointer, in.Ncomp)
	for c := int64(0); c < in.Ncomp; c++ {
		ptrs[c] = unsafe.Pointer(originPtr + uintptr(c*compsize))
	}

	sl := data.SliceFromPtrs([3]int{int(in.Nx), int(in.Ny), int(in.Nz)}, data.GPUMemory, ptrs)

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
*/
