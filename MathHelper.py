import random


def bin_to_dec(bin):
    number = 0
    length = len(bin)
    for i in range(0, length):
        number += int(bin[i]) * (2 ** (length - i - 1))
    return number


def fast_exponentiation_mod(a, n, m):
    x = 1
    while n:
        if n & 0x01:
            x = (x * a) % m
        a = pow(a, 2, m)
        n >>= 1
    return x


def miller_rabin(n):
    if n < 5 or n % 2 == 0:
        raise ValueError('Неправильное число')
    l = n - 1
    r = 1
    s = 0
    while l != 1:
        if l % 2 == 0:
            l = l // 2
            s = s + 1
        else:
            r = l
            break
    a = random.randint(2, n - 2)
    y = fast_exponentiation_mod(a, r, n)
    if y != 1 and y != n - 1:
        j = 1
        if j <= s - 1 and y != n - 1:
            y = (y * y) % n
            if y == 1:
                return 0
            j = j + 1
        if y != n - 1:
            return 0
    return 1


def gen_k(k, t):
    while True:
        j = k - 1
        arr = []
        arr.append(1)
        while j > 1:
            b = random.randint(0, 1)
            arr.append(b)
            j = j - 1
        arr.append(1)
        string = ''
        for i in range(0, len(arr)):
            string = string + str(arr[i])
        p = bin_to_dec(string)
        i = 1
        while i < t:
            if int(p) % 2 == 0:
                break
            x = miller_rabin(int(p))
            if x == 1:
                i = i + 1
            elif x == 0:
                break
        if i == t:
            return p
