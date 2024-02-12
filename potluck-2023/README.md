
# Upside-down Cake

flag formatは `"potluck{?}"` で全体の文字数が44文字であることがわかっている。

flagを半分で分けたそれぞれの文字列を $x,y$ 、
素数を $p$ としたとき、以下の式により暗号文 $ct$ が生成される。

$$
    x^{-1} + y^{-1} = ct \pmod p
$$

$p,ct$ が与えられるのでflagを求める問題。

上の式の両辺に $xy$ をかけると、

$$
    x + y = x\cdot y\cdot ct \pmod p
$$

flagの最初の8文字はわかっているので、既知部分を $k$ 、未知部分を $u$ とすると以下のように表せる。

$$
    (k + u) + y = (k + u)\cdot y\cdot ct \pmod p
$$

多変数の coppersmith method の[コード](https://github.com/defund/coppersmith)を用いて
 $u,y$ を求める。

$k,u,y$ からflagが得られる。