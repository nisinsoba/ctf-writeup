from z3 import *

#nc = connect()

def LFSR(state):
	while 1:
		yield state & 0xf  
		for _ in range(4):
			bit = (state ^ (LShR(state, 1)) ^ (LShR(state, 3)) ^ (LShR(state, 4))) & 1
			state = (LShR(state, 1)) | (bit << 63)

def new_LFSR(state):
	while 1:
		yield state & 0xf  
		for _ in range(4):
			bit = (state ^ (state >> 1) ^ (state >> 3) ^ (state >> 4)) & 1  
			state = (state >> 1) | (bit << 63)

n = 56
rps = ["rock", "paper", "scissors", "rock"]

v = []
for i in range(n):
    nc.readuntil(': ')
    nc.send("rock")
    t = nc.readline()
    if "Tie!" in t: v.append(0)
    elif "You win!" in t: v.append(2)
    else: v.append(1)

s = Solver()
key = BitVec("k", 64)
rng = LFSR(key)
for i in range(n):
    val = next(rng)
    s.add(val%3 == v[i])

if s.check() == sat:
    m = s.model()
    res = 0
    init_val = m[key].as_long()
else:
    exit(1)

new_rng = new_LFSR(init_val)
for _ in range(56): next(new_rng)

for i in range(50):
    r = next(new_rng) % 3
    sendm = rps[r+1]
    print(rps[r])
    print(sendm)
    nc.send(sendm)
    t = nc.readline()
    print(t)

print(nc.readline())

# dice{wow_u_must_be_extremely_lucky_91ff5a34}
