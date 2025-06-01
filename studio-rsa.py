import random
from math import gcd
#from fattori_primi import fattori_primi

# === Miller-Rabin per test di primalità ===
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

# === Generazione di numeri primi ===
def generate_large_prime(bits):
    print("generate_large_prime\n  bits: {}\n".format( bits ) )
    while True:
        candidate = random.getrandbits(bits) | (1 << bits - 1) | 1
        p = is_prime(candidate)
        print("  candidate: {}, is_prime: {}\n".format( candidate, p ) )
        if p:
            return candidate

# === Inverso moltiplicativo mod φ(n) ===
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

# === Test sicurezza chiavi ===

def validate_rsa_key_strength(e, d, p, q, n, phi, min_bits=512):
    errors = []

    if p == q:
        errors.append("❌ I due numeri primi p e q sono uguali.")

    if gcd(e, phi) != 1:
        errors.append("❌ e e φ(n) non sono coprimi.")

    if e == d:
        errors.append("⚠️ e e d sono uguali: crittografia e decrittografia diventano identiche.")

    if n.bit_length() < min_bits:
        errors.append(f"⚠️ n ha solo {n.bit_length()} bit: troppo piccolo per la sicurezza.")

    if not (1 < e < phi):
        errors.append("❌ e non è nell'intervallo valido (1 < e < φ(n)).")

    if not (1 < d < phi):
        errors.append("❌ d non è nell'intervallo valido (1 < d < φ(n)).")

    if not errors:
        print("✅ La chiave RSA supera i controlli di sicurezza base.")
    else:
        print("⚠️ La chiave presenta problemi di sicurezza:")
        for err in errors:
            print("  -", err)

# === Generazione chiavi RSA ===
def generate_rsa_keys(bits=512):
    print("Generazione dei numeri primi p e q...")
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    while p == q:
        q = generate_large_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    print("generate_rsa_keys\n  p:{0}, q:{1}\n  n=({0} * {1})={2}, phi=({0}-1) * ({1}-1)={3}\n".format( p, q, n, phi ) )

    # Scelta dinamica di e: 1 < e < phi e coprimo con phi
    print("  Cerco e a caso tra 3 e {}\n".format( phi ) )
    while True:
        e = random.randrange(3, phi)
        n_gcd = gcd(e, phi)
        print("    e:{}, gcd:{}\n".format( e, n_gcd ) )
        if n_gcd == 1:
            break
   
    #fp = fattori_primi( phi )
    #print( "Fattori primi di phi: {}".format( fp ) )
            
    d = modinv(e, phi)
    print("  Trovato  d = {} = modinv( e:{}, phi:{} )\n".format( d, e, phi ) )
    print("  e:{}, d:{}, n:{}\n".format( e, d, n ) )
    return (p, q, n, phi, e, d)

# === Crittografia / Decrittografia ===
def encrypt(m, e, n):
    print("encrypt\n  Cifro {} con chiave ( {}, {} )\n".format(m, e, n) )
    p = pow(m, e)
    print("  pow( m:{}, e:{} ) = {}\n".format( m, e, p ) )
    p = pow(m, e, n)
    print("  pow( m:{}, e:{} ) % n:{} = {}\n".format( m, e, n, p ) )
    return p

def decrypt(c, d, n):
    print("decrypt\n  Decifro {} con chiave ( {}, {} )\n".format(c, d, n) )
    p = pow(c, d)
    print("  pow( c:{}, d:{} ) = {}\n".format( c, d, p ) )
    p = pow(c, d, n)
    print("  pow( c:{}, d:{} ) % n:{} = {}\n".format( c, d, n, p ) )
    return p

# === Esecuzione esempio ===
if __name__ == "__main__":
    p, q, n, phi, e, d = generate_rsa_keys( bits=3 )  # 256 bit = veloce per test, ma poco sicuro
    validate_rsa_key_strength(e, d, p, q, n, phi, min_bits=8)
    print(f"Chiave pubblica: (e={e}, n={n})")
    print(f"Chiave privata: (d={d}, n={n})")

    # Messaggio da cifrare
    message = 2
    print(f"Messaggio originale: {message}")

    # Crittografia
    ciphertext = encrypt(message, e, n)
    print(f"Messaggio cifrato: {ciphertext}")

    # Decrittografia
    decrypted = decrypt(ciphertext, d, n)
    print(f"Messaggio decrittato: {decrypted}")

