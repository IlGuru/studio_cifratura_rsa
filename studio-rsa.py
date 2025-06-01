import random
from math import gcd

# === 1. Miller-Rabin per test di primalità ===
def is_prime(n, k=5):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False

    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# === 2. Generazione di numeri primi ===
def generate_large_prime(bits):
    print("generate_large_prime\n  bits: {}\n".format( bits ) )
    while True:
        candidate = random.getrandbits(bits) | (1 << bits - 1) | 1
        p = is_prime(candidate)
        print("  candidate: {}, is_prime: {}\n".format( candidate, p ) )
        if p:
            return candidate

# === 3. Inverso moltiplicativo mod φ(n) ===
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Inverso moltiplicativo non esistente")
    return x % m

# === 4. Generazione chiavi RSA ===
def generate_rsa_keys(bits=512):
    print("Generazione dei numeri primi p e q...")
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    while p == q:
        q = generate_large_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if gcd(e, phi) != 1:
        # Se 65537 non va bene, scegliamo un altro valore
        for cand in range(3, phi, 2):
            if gcd(cand, phi) == 1:
                e = cand
                break
    d = modinv(e, phi)
    return (e, d, n)

# === 5. Crittografia / Decrittografia ===
def encrypt(m, e, n):
    return pow(m, e, n)

def decrypt(c, d, n):
    return pow(c, d, n)

# === 6. Esecuzione esempio ===
if __name__ == "__main__":
    e, d, n = generate_rsa_keys(bits=3)  # 256 bit = veloce per test, ma poco sicuro
    print(f"Chiave pubblica: (\ne={e}, \nn={n}\n)")
    print(f"Chiave privata: (d={d}, n={n})")

    ## Messaggio da cifrare
    #message = 123456789
    #print(f"Messaggio originale: {message}")

    ## Crittografia
    #ciphertext = encrypt(message, e, n)
    #print(f"Messaggio cifrato: {ciphertext}")

    ## Decrittografia
    #decrypted = decrypt(ciphertext, d, n)
    #print(f"Messaggio decrittato: {decrypted}")

