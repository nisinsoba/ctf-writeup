
# L4ugh


666ビット素数 $d$ を生成し以下の値を生成

```python
d_evil = d >> 333
d_good = d % 2**333
```

次のコードで与えられる情報から d_evil, d_good を求め、$d$ を求める。

```python
def RsaGen(d_evil):
    for _ in range(19):
        try:
            Ns, es = [], []
            for evilChar in '666':
                p = getPrime(512)
                q = getPrime(512)
                phi = (p - 1) * (q - 1)
                e = inverse(d_evil, phi)
                Ns.append(p * q)
                es.append(e)
            
            return Ns, es
        except ValueError as e:
            pass

def getrand(d_good):
    user_input = int(input("Enter your payload:\t"))
    if user_input.bit_length() > (666//2): 
        print("MEH")
        return 
    return [d_good*user_input + getPrime(666//2) for i in range(10)]
```

d_evil は common private exponent attack で求められる。

d_good は $2^{333}-1$ を入力して生成される値 $v$ に対して $v//(2^{333}-1)$ で求められる。

これで次の問題に進める。次の問題はAESの問題。
AESのcbcモードで暗号化された暗号文に対してbit flipping attack で先頭ブロックの値を書き換えることでflagを得られる。