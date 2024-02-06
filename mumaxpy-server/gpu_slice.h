#include <cuda_runtime_api.h>
#include <cuda.h>

 void* open_mem_handle(char* handlebytes, int* err){
    void* ptr = NULL;
    cudaIpcMemHandle_t handle;

    for (int i = 0; i < 64; i++){
        handle.reserved[i] = handlebytes[i];
    }

    *err = (int)cudaIpcOpenMemHandle(&ptr, handle, cudaIpcMemLazyEnablePeerAccess);
    return ptr;

}
