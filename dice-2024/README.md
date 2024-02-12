
# rps-casino

以下で定義されているLFSRが初期値stateから値を生成する。

```python
def LFSR():
    state = bytes_to_long(os.urandom(8))
    while 1:
        print(state & 0xf, end=" ")
        yield state & 0xf  
        for i in range(4):
            bit = (state ^ (state >> 1) ^ (state >> 3) ^ (state >> 4)) & 1  
            state = (state >> 1) | (bit << 63)
```

LFSRが生成する値をmod 3した値に対して、0ならばrock, 1ならばpaper, 2ならばscissorsが選択される。

最初に50回ジャンケンを行った結果が得られる。そして次の56回のジャンケンに勝てばflagが出る。

z3を使って最初の50回の結果からLFSRの初期値を求める。初期値が分かればその後の値を再現できる。

LFSRから生成される値を $r$ 、最初の50回のジャンケンの結果を $t\in\{0,1,2\}$ とし、以下の制約を加える。

$$
    r_i\ \mod 3\ =\ t_i\quad (i=1,\ldots,50)
$$

これで解を探せば条件を満たす初期値が得られてflagが得られる。
