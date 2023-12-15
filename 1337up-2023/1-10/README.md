
# 1-10 Writeup 

```python
from random import randint
from re import search
from flag import FLAG

cs = [randint(0, 2**1000) for _ in range(10)]
xs = [randint(0, 2**64) for _ in range(10)]
xs = [ord(f) + i - (i%1000) for i, f in zip (xs, search("{(.*)}", FLAG).group(1))]

print(f"{cs = }")
print(f"s = {sum(c*x for c, x in zip(cs, xs))}")
```

$s$ に関する式は以下のように表せる。

$$
\begin{align*}
s = xs_1 * cs_1 + \cdots + xs_{10} * cs_{10}\\
\Rightarrow xs_1 * cs_1 + \cdots + xs_{10} * cs_{10} - s = 0
\end{align*}
$$

各 $cs_k$ と $s$ は既知であり、 各 $xs_k$ は整数なので、格子を用いて各 $xs_k$ が求められそう。

以下のように行列を作る。

$$
\begin{bmatrix}
1      & 0 & \cdots & & 0      & cs_1    \\
0      & 1 & \cdots & & 0      & cs_2    \\
\vdots &   & \ddots & & \vdots & \vdots  \\
0      &   & \cdots & & 0      & cs_{10} \\
0      &   & \cdots & & 1      & -s
\end{bmatrix}
$$

この行列をLLL基底簡約すると、次のようなベクトルが得られた。

$$
[\ xs_1,\ xs_2,\ \cdots,xs_{10},\ 1,\ 0\ ]
$$

これで、 $xs$ が求まった。

FLAGの中身を $f$ としたとき、 $f$ と $xs$ との関係は式変形すると以下のように表せる。

$$
f_k = xs_k \pmod {1000}
$$

FLAG が得られた。
