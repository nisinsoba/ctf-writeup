a = 104932596701958568145159429432079350581741243925294416012169671604384908382893445168447905864839450402111868722373005467040643335329799448356719960809485814400987619457043584576651627652936429829564657705560266433066823589229257859375942917575729874731586891094997845427952093627170472382405528285663530612106
b = 146908709759837063143862302770110984437045635655026319928249954800644806528614554086681623417268963974691959251767647958752898163761641238519061717835899588252518767306816402052353874469376243689011218283173950163484015487529897260943257598915903245695362042234335492571429369281809958738989439275152307290506
n = 68915438454431862553872087841423255330382510660515857448975005472053459609178709434028465492773792706094321524334359097372292237742328589766664933832084854448986045922250239618283612819975877218019020936022572963433202427817150998352120028655478359887600473211365524707624162292808256010583620102295206287739
e = 65537

m1 = b"The quick brown fox jumps over the lazy dog"
m3 = b"https://translate.google.com/?sl=it&tl=en&text=ricerca"

# encrypted data
enc = ["05d7913ff5cd9b6a706249ac05779f2501013ecc05caec697d9270a8a1d3bdaabf898d73410aa0ffbd361a6032adbbfa35386b2e19ec812e9f6bd52e6a2ca1b3760b3076a86ffc94dd6007d74a272e0e3d5326d9e5b01b9211a803338f5899ad6cc29877cc02ca2ff923db79e3ad477bf3820e73596088f54a8cfb187f812201", "1913ba387e6f847dce455dc47092bf83571c34914b7df5875da536f11e68c8a39c78dfe69517ef4b389ea51434e071ce033854fd27c831996aa214cdc02225747a517d44408fbd0232672679bc189f26f6e9b6852a1e68e93ac14e2ce5afc1e050a44733094fe68b0477d4c4b609043e4da4e58390c4f9cf372005653c7f2529",  "45054a08d594bd8af1d0fac759ccc799214d0ccce8ae9c5183ef4fba296819bcdf6306f72ee34dcd5d85967fae314d6d3d65a7693b4187adce1d5375dd00c472c0310393cd5bb114602e24d481e276a4926e8886bdcfed96bb8bf9c5812d594f66e46b1737849e8e2f2c3f7b6a45e284c754cf6caf71df34efe143636b5e9079"]

C1 = bytes.fromhex(enc[0])
C2 = bytes.fromhex(enc[1])
C3 = bytes.fromhex(enc[2])
c1 = int.from_bytes(C1, 'big') ^^ int.from_bytes(m1, 'big')
c3 = int.from_bytes(C3, 'big') ^^ int.from_bytes(m3, 'big')

# Half GCD code from https://scrapbox.io/crypto-writeup-public/half-GCD
def pdivmod(u, v):
    """
    polynomial version of divmod
    """
    q = u // v
    r = u - q*v
    return (q, r)

def hgcd(u, v, min_degree=10):
    """
    Calculate Half-GCD of (u, v)
    f and g are univariate polynomial
    <http://web.cs.iastate.edu/~cs577/handouts/polydivide.pdf>
    """
    x = u.parent().gen()

    if u.degree() < v.degree():
        u, v = v, u

    if 2*v.degree() < u.degree() or u.degree() < min_degree:
        q = u // v
        return matrix([[1, -q], [0, 1]])

    m = u.degree() // 2
    b0, c0 = pdivmod(u, x^m)
    b1, c1 = pdivmod(v, x^m)

    R = hgcd(b0, b1)
    DE = R * matrix([[u], [v]])
    d, e = DE[0,0], DE[1,0]
    q, f = pdivmod(d, e)

    g0 = e // x^(m//2)
    g1 = f // x^(m//2)

    S = hgcd(g0, g1)
    return S * matrix([[0, 1], [1, -q]]) * R

def pgcd(u, v):
    """
    fast implementation of polynomial GCD
    using hgcd
    """
    if u.degree() < v.degree():
        u, v = v, u

    if v == 0:
        return u

    if u % v == 0:
        return v

    if u.degree() < 10:
        while v != 0:
            u, v = v, u % v
        return u

    R = hgcd(u, v)
    B = R * matrix([[u], [v]])
    b0, b1 = B[0,0], B[1,0]
    r = b0 % b1
    if r == 0:
        return b1

    return pgcd(b1, r)

# Franklin-Reiter Related Message Attack
# f1(x) = x^e - c1
# f2(x) = (a*x + b)^e - c3
# (x - s) = gcd(f1, f2).monic()

PR.<x> = PolynomialRing(Zmod(n))
f1 = (a*x+b)^e - c1
f2 = (a^3*x+a^2*b+a*b+b)^e - c3

# Half GCD
g = pgcd(f1, f2)
s = Zmod(n)(-g.monic()[0])

r2 = (a^2*s + a*b + b) % n
key = pow(r2, e, n)
m = int(key) ^^ int.from_bytes(C2, 'big')

print(int.to_bytes(m, 128, 'big').lstrip(b'\x00'))

# RicSec{1_7h1nk_y0u_uNd3r5t4nd_ev3ry7h1ng_4b0ut_Franklin-Reiter's_a7t4ck}

