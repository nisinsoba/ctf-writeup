
# Share it (Part 1)

以下の平文をAESのCBCモードで16バイトごとに暗号化した暗号文が与えられる。

```
{'admin': false, 'username': username}
```

false の部分を true にして送ればflagが得られる。

falseの文字列は先頭ブロックにあるので、先頭ブロックについて考える。

復号時、先頭ブロックでは以下の式が成り立つ。
(暗号文 $c$ , 平文 $m$ , 復号関数 $D$ , 初期化ベクトル $\mathrm{IV}$ )

$$
m_1 = D(c_1)\ \oplus\ \mathrm{IV}
$$

よって、IV を変更すると平文の先頭ブロックを自由に操作できる。

先頭ブロックの一部分に注目すると、大雑把に次のように表せる。

$$
\mathrm{false} = D(c_1)\ \oplus\ \mathrm{IV}
$$

欲しいのは以下の式を満たす $\mathrm{\widehat{IV}}$ なので、

$$
\mathrm{true} = D(c_1)\ \oplus\ \mathrm{\widehat{IV}}
$$

次のように $\mathrm{\widehat{IV}}$ を設定すればよい。

$$
\mathrm{\widehat{IV}} = \mathrm{IV}\ \oplus\ \mathrm{false}\ \oplus\ \mathrm{true}
$$

元の暗号文と $\mathrm{\widehat{IV}}$ を送ると flag が得られる。
