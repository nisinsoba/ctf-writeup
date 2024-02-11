import ast
from pwn import *
from sage.all import *

#r = remote("", "")

r.recvuntil("option:\t".encode())
r.sendline('{"option":"1"}'.encode())

Ns = ast.literal_eval(r.recvline().decode().split('=')[1])
es = ast.literal_eval(r.recvline().decode().split('=')[1])

M = int(sqrt(Ns[-1]))
vec1 = vector([M , es[0], es[1], es[2]])
vec2 = vector([0, -Ns[0], 0, 0])
vec3 = vector([0, 0, -Ns[1], 0])
vec4 = vector([0, 0, 0, -Ns[2]])
mat = Matrix([vec1, vec2, vec3, vec4])

mat = mat.LLL()
d_evil = abs(mat[0][0] // M)

r.recvuntil("option:\t".encode())
r.sendline('{"option":"2"}'.encode())
r.recvuntil("Enter your payload:".encode())
s = 2**333 - 1
r.sendline(str(s).encode())

rand = ast.literal_eval(r.recvline().decode().split('=')[1])
d_good=rand[0]//s

d = pow(2,333)*d_evil + d_good
print("d = ", d)

def updatect(iv:bytes, str1:bytes, str2:bytes, blocksize=16):
    iv = list(iv)
    for i in range(0, blocksize):
        iv[i] = iv[i] ^ str1[i] ^ str2[i]
    return bytes(iv)

r.recvuntil("option:\t".encode())
s = '{"option":"3", "d":' + str(d) + '}'
r.sendline(s.encode())
r.recvuntil("2.sign in".encode())
r.sendline('{"option":"1", "user":""}'.encode())
pt = ast.literal_eval(r.recvline().strip().decode())
id = pt['id']
ct = r.recvline().strip().decode()

pt = b'{"id": ' + str(id).encode() + b', "isadmin'
new_pt = b'{"isadmin":1}\x03\x03\x03'

iv = bytes.fromhex(ct[:32])
print("pt = ", pt[:16])
print("new pt = ", new_pt)
new_iv = updatect(iv, pt[:16], new_pt)
new_ct = new_iv.hex() + ct[32:64]

r.recvuntil("option:\t".encode())
tmp = '{"option":"3", "d":' + str(d) + '}'
r.sendline(tmp.encode())
r.recvuntil("2.sign in".encode())
sendm = '{"option":"2", "token":"' + new_ct + '"}'
r.sendline(sendm.encode())
r.sendline('{"option":"1"}'.encode())
print(r.recvuntil("0xL4ugh".encode()).decode(), end="")
print(r.recvline().decode())

# 0xL4ugh{cryptocats_B3b0_4nd_M1ndfl4y3r}