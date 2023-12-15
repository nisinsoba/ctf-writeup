
# SLCG

```python
from __future__ import annotations
import os

FLAG = b"gctf{??????????}"

class LCG:
    def __init__(self, mod: int, mult: int, add: int, seed: int):
        self.mod = mod
        self.mult = mult
        self.add = add
        self.value = seed

    def __next__(self) -> int:
        self.value = (self.value * self.mult + self.add) % self.mod
        return self.value

    def __iter__(self) -> LCG:
        return self

    @classmethod
    def random_values(cls):
        return LCG(
            int.from_bytes(os.urandom(16), "big"), # mod
            int.from_bytes(os.urandom(16), "big"), # mult
            int.from_bytes(os.urandom(16), "big"), # add
            int.from_bytes(os.urandom(16), "big")  # value
        )

class Encryptor:
    def __init__(self):
        self.lcgs: tuple[LCG] = (LCG.random_values(), LCG.random_values())

    def encrypt(self, message: str) -> list[int]:
        result = []
        for ascii_char in message:
            bin_char = list(map(int, list(f"{ascii_char:07b}")))

            for bit in bin_char:
                result.append(next(self.lcgs[bit]))
                print(bit)

            self.lcgs = (
                LCG(
                    next(self.lcgs[0]), next(self.lcgs[0]),
                    next(self.lcgs[0]), next(self.lcgs[0])
                ),
                LCG(
                    next(self.lcgs[1]), next(self.lcgs[1]),
                    next(self.lcgs[1]), next(self.lcgs[1])
                )
            )
        return result

def main() -> int:
    encryption = Encryptor()
    print(f"ct = {encryption.encrypt(FLAG)}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

これは、線形合同法 (Linear congruential generators) の問題。

暗号化した値のリストが与えられる。

問題プログラムでは、はじめにランダムな初期値(mod, mult, add, value)を設定した2つのLCGを生成した後、encryptoメソッドでFLAGの暗号化を行っている。

encryptoメソッド内の処理内容は以下のようになっている。

```
FLAGの文字を一文字ずつ取り出し、for文を回す

    1文字を7ビットで表し、リストにする
    ビットが 0 or 1 の場合で以下の処理を行う
        
        0のとき、1個目のLCGを使用してvalueの値を更新し、valueを暗号文リストに追加
        1のとき、2個目のLCGを使用してvalueの値を更新し、valueを暗号文リストに追加

    1文字の処理が終わると、2つのLCGのmod, mult, add, valueの値を更新

FLAGの全ての文字に対して処理を行い、暗号文のリストを返す
```

$value$ を $value'$ に更新するための式は以下である。

$$
value' = value\ *\ mult\ +\ add \pmod{mod}
$$

FLAGの1文字を処理する間は各LCGの $mult, add, mod$ の値は同じであり、
FLAGの先頭の数文字が既知で、かつ $value'$ のリストが与えられているため、 
$mult, add, mod$ の値が求められそう。

まずは $mod$ の値を求める。

"gctf{ }" の最初の文字のgを7ビットのリストに直すと[1,1,0,0,1,1,1]となる。

ビットが1の要素に注目し、暗号リストから最初の 1, 2, 5, 6, 7個目の
valueを取ってきてそれぞれ $v_1,v_2,v_3,v_4,v_5$ とする。そして未知の初期値を $v_0$ とする。

それぞれの値に対して以下の式が成り立つ。

$$
\begin{align}
v_1 = v_0\cdot mult + add \pmod{mod}\\
v_2 = v_1\cdot mult + add \pmod{mod}\\
v_3 = v_2\cdot mult + add \pmod{mod}\\
v_4 = v_3\cdot mult + add \pmod{mod}\\
v_5 = v_4\cdot mult + add \pmod{mod}\\
\end{align}
$$

次に式同士引き算する。

$$
\begin{align}
v_2 - v_1 = mult(v_1-v_0) \pmod{mod}\qquad (1)\\
v_3 - v_2 = mult(v_2-v_1) \pmod{mod}\qquad (2)\\
v_4 - v_3 = mult(v_3-v_2) \pmod{mod}\qquad (3)\\
v_5 - v_4 = mult(v_4-v_3) \pmod{mod}\qquad (4)\\
\end{align}
$$

そして次のように式変形する。

$$
\begin{align}
(3)\cdot (1)-(2)\cdot (2) &= mult(v_3-v_2)(v_2-v_1)-mult^2(v_2-v_1)(v_2-v_1)\\
                          &= mult^2(v_2-v_1)(v_2-v_1)-mult^2(v_2-v_1)(v_2-v_1)\\
                          &= 0 \pmod{mod}\\
(4)\cdot (2)-(3)\cdot (3) &= mult(v_4-v_3)(v_3-v_2)-mult^2(v_3-v_2)(v_3-v_2)\\
                          &= mult^2(v_3-v_2)(v_3-v_2)-mult^2(v_3-v_2)(v_3-v_2)\\
                          &= 0 \pmod{mod}\\
\end{align}
$$

よって、 $\mathrm{gcd}(\ (3)\cdot (1)-(2)\cdot (2),\ (4)\cdot (2)-(3)\cdot (3)\ )$ で $mod$ が求められる。

次に (2)式より $mult$ を求める。

$$
\begin{align}
v_3-v_2 &= mult(v_2-v_1) \pmod{mod}\\
\Longrightarrow mult &= (v_3-v_2)(v_2-v_1)^{-1} \pmod{mod}
\end{align}
$$

$add$ も求まる。

$$
\begin{align}
v_2 &= v_1\cdot mult + add \pmod{mod}\\
\Longrightarrow add &= v_2 - v_1\cdot mult \pmod{mod}
\end{align}
$$

これで、 ビットが1の場合に使用するLCGの文字gに対する $mod, mult, add, value$ が求まったので、 1の場合のLCGの全ての値は再現できる。

また、1の場合のLCGで計算したvalueの値と暗号文のvalueの値が一致しない場合は暗号文
のvalueが0の場合のLCGから生成されたことが分かるので、平文ビットの1 or 0を判定できる。

よってFLAGが得られる。

## 別解

$mod, mult, add$ の値はグレブナー基底でも求められる。

コードを以下に示す。

```python
import ast
with open("ciphertext.txt", "r") as f:
    ct = ast.literal_eval(f.read().split("=")[1].strip())

P.<x,y> = PolynomialRing(ZZ, order='lex')
I = ideal(ct[0]*x + y - ct[1], ct[1]*x + y - ct[4], ct[4]*x + y - ct[5], ct[5]*x + y - ct[6])
basis = I.groebner_basis()

xdash = ZZ(basis[0].coefficient({x:0}))
ydash = ZZ(basis[1].coefficient({y:0}))
mod = basis[2]

mult = -xdash % mod
add = -ydash % mod

print(f"mod = {mod}")
print(f"mult = {mult}")
print(f"add = {add}")
```

これは、次の合同連立方程式をグレブナー基底で解いている。
(辞書式順序で計算(order='lex'))

$$
\begin{align}
v_1\cdot mult + add - v_2 = 0 \pmod{mod}\\
v_2\cdot mult + add - v_3 = 0 \pmod{mod}\\
v_3\cdot mult + add - v_4 = 0 \pmod{mod}\\
v_4\cdot mult + add - v_5 = 0 \pmod{mod}\\
\end{align}
$$

左辺をsageに入れてグレブナー基底を計算した結果から以下の式が得られる。

$$
\begin{align*}
mult + xdash = 0 \pmod{mod}\\
add  + ydash = 0 \pmod{mod}\\
mod  = 0 \pmod{mod}
\end{align*}
$$

よって、

$$
\begin{align*}
mult &= -xdash \pmod{mod}\\
add  &= -ydash \pmod{mod}\\
mod  &= 0 \pmod{mod}\\
\end{align*}
$$

FLAGを得るまでの残りの流れは上と同じ。
