import math

def fattori_primi(n, fattori=None, divisori=None):
    if fattori is None:
        fattori = []
    if divisori is None:
        divisori = [2]

    if n < 2:
        return tuple(fattori)

    radice = math.isqrt(n)

    # Prova a dividere per i divisori noti
    for d in divisori:
        if d > radice:
            break
        if n % d == 0:
            fattori.append(d)
            return fattori_primi(n // d, fattori, divisori)

    # Trova un nuovo divisore (dispari)
    d = divisori[-1] + 1 if divisori[-1] == 2 else divisori[-1] + 2
    while d <= radice and n % d != 0:
        d += 2

    if d > radice:
        # n è primo, aggiungilo e termina
        fattori.append(n)
        return tuple(fattori)

    fattori.append(d)
    divisori.append(d)
    return fattori_primi(n // d, fattori, divisori)

if __name__ == "__main__":
    # Esempio d'uso
    numero = 987654321987654321
    print(f"Fattori primi di {numero}:", fattori_primi(numero))

