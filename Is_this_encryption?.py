from Crypto.Util.number import bytes_to_long, long_to_bytes
from pycuda.compiler import SourceModule
import pycuda.autoinit
import pycuda.driver as drv
import numpy as np

# CUDA 커널 코드 정의
mod = SourceModule("""
__device__ unsigned int encrypt(unsigned int data) {
    data ^= (data >> 11);
    data ^= (data << 7) & 0x9d2c5680;
    data ^= (data << 15) & 0xefc60000;
    data ^= (data >> 18);
    return data & 0xffffffff;
}

__global__ void brute_force(unsigned int target, unsigned int *result, bool *found) {
    unsigned int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (*found) return;

    unsigned int encrypted = encrypt(tid);
    if (encrypted == target) {
        *result = tid;
        *found = true;
    }
}
""")

brute_force = mod.get_function("brute_force")

# 암호화된 플래그 블록 리스트
enc_flag_hex_blocks = [
    '62271224', '1be0b1e3', '7e2c3372', 'f8960560',
    '2b9e0f5f', '3520b1df', '65dc284a', '1ac8e76b'
]

decrypted_flag = b''

for block_hex in enc_flag_hex_blocks:
    target_int = int(block_hex, 16)
    result = np.zeros(1, dtype=np.uint32)
    found = np.zeros(1, dtype=np.bool_)

    block_size = 256
    grid_size = (2**32 + block_size - 1) // block_size

    brute_force(
        np.uint32(target_int), drv.Out(result), drv.Out(found),
        block=(block_size, 1, 1), grid=(grid_size, 1)
    )

    if found[0]:
        decrypted_flag += long_to_bytes(result[0], 4)
    else:
        print("복호화 실패")

print(f"Decrypted Flag: {decrypted_flag.decode(errors='ignore')}")
