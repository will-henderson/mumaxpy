#include <cuda_runtime_api.h>
#include <cuda.h>

void* open_mem_handle(void* handlebytes){
    void* ptr;
    cudaIpcMemHandle_t handle = {*(char*)(handlebytes)};
    cudaIpcOpenMemHandle(&ptr, handle, 1);
    return ptr;
}
