import math
import random
import hashlib
from MathHelper import gen_k


def generate_params(k):
    p = gen_k(k, 10)
    t = math.floor(math.log2(p))
    s = math.floor((t - 1) / 160)
    v = t - 160 * s
    return p, t, s, v


def generate_elliptic_curve_params(s, v):
    seedE = ""
    g = random.randint(160, 1001)
    for i in range(g):
        seedE += str(random.randrange(0, 2))
    seedE = bytes(seedE, 'utf-8')
    z = int(seedE)

    H = hashlib.sha1(seedE)
    c0 = bin(int(H.hexdigest(), 16))[2:]
    c0 = list(c0[-v:])
    c0[0] = '0'
    W0 = c0
    for i in range(1, s + 1):
        s_i = bytes(bin((z + i) % pow(2, g))[2:], 'utf-8')
        Wi = hashlib.sha1(s_i)
        Wi = list(bin(int(Wi.hexdigest(), 16))[2:])
        W0 = W0 + Wi
    W0 = ''.join(W0)
    r = int(W0, 2)
    return r


def generate_elliptic_curve_params2(r, p):
    while True:
        a = random.randint(1, p)
        b2 = (pow(a, 3, p) * pow(r, -1, p)) % p
        b = tonelli_shneks(b2, p)
        if pow(a, 3, p) == ((r * pow(b, 2, p)) % p):
            return a, b


def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def tonelli_shneks(a, p):
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


k = int(input('Введите размерность числа p: '))
p, t, s, v = generate_params(k)
r = generate_elliptic_curve_params(s, v)

while True:
    if r == 0 or ((4 * r) + 27) % p == 0:
        r = generate_elliptic_curve_params(s, v)
    else:
        break

a, b = generate_elliptic_curve_params2(r, p)
print(f'E: y^2 = x^3 + {a} * x + {b}')
print(f"GF({p})")


