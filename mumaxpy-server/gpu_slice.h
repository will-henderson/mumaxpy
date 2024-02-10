#include <cuda_runtime_api.h>
#include <cuda.h>
#include <string.h>

 void* open_mem_handle(char* handlebytes, int* err){
    void* ptr = NULL;
    cudaIpcMemHandle_t handle;

    memcpy(handle.reserved, handlebytes, CUDA_IPC_HANDLE_SIZE * sizeof(char));

    *err = (int)cudaIpcOpenMemHandle(&ptr, handle, cudaIpcMemLazyEnablePeerAccess);
    return ptr;

}

void* get_mem_handle(char* handlebytes, void* ptr, int* err){
    cudaIpcMemHandle_t handle;

    *err = (int)cudaIpcGetMemHandle(&handle, ptr);

    memcpy(handlebytes, handle.reserved, CUDA_IPC_HANDLE_SIZE * sizeof(char));

}
