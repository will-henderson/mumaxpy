#include <cuda_runtime_api.h>
#include <cuda.h>
#include <stdio.h>

 void* open_mem_handle(void* handlebytes, int* err){
    void* ptr;
    cudaIpcMemHandle_t handle = {*(char*)(handlebytes)};

    *err = (int)cudaIpcOpenMemHandle(&ptr, handle, cudaIpcMemLazyEnablePeerAccess);
    return ptr;

}
