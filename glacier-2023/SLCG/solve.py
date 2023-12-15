import ast
import math

with open("ciphertext.txt", "r") as f:
    ciphertext = ast.literal_eval(f.read().split("=")[1].strip())

split_list = []
for i in range(0, len(ciphertext), 7):
    split_list.append(ciphertext[i:i+7])

g_bin = list(bin(ord("g")))[2:]
v = []
for i in range(len(g_bin)):
    if g_bin[i] == "1":
        v.append(ciphertext[i])

t1 = v[1] - v[0]
t2 = v[2] - v[1]
t3 = v[3] - v[2]
t4 = v[4] - v[3]

d = math.gcd(t3*t1-t2*t2, t4*t2-t3*t3)
m = (v[2]-v[1])*pow(v[1]-v[0], -1, d) % d
a = (v[1] - m*v[0]) % d
v0 = (v[0] - a) * pow(m, -1, d) % d
mod, mult, add, value = d, m, a, v0

result = []
for list in split_list:
    str = ""
    for cval in list:
        tmp = (value * mult + add) % mod
        if tmp == cval:
            value = tmp
            str += "1"
        else:
            str += "0"
    result.append(str)

    mod2 = (value * mult + add) % mod
    mult2 = (mod2 * mult + add) % mod
    add2 = (mult2 * mult + add) % mod
    value = (add2 * mult + add) % mod
    mod, mult, add = mod2, mult2, add2

for i in result:
    print(chr(int(i, 2)), end="")

# gctf{th15_lcg_3ncryp710n_w4sn7_s0_5s3cur3_aft3r_4ll}

