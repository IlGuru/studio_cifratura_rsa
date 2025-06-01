def fattori_primi(n, fattori=None, divisori=None):
    if fattori is None:
        fattori = []
    if divisori is None:
        divisori = [2]

    if n < 2:
        return tuple(fattori)

    # Prova a dividere per i divisori già trovati
    for d in divisori:
        if n % d == 0:
            fattori.append(d)
            return fattori_primi(n // d, fattori, divisori)

    # Trova un nuovo divisore dispari
    d = divisori[-1] + 1 if divisori[-1] == 2 else divisori[-1] + 2
    while n % d != 0:
        d += 2  # salta i pari

    fattori.append(d)
    divisori.append(d)
    return fattori_primi(n // d, fattori, divisori)

# Esempio d'uso
numero = 360
print(f"Fattori primi di {numero}:", fattori_primi(numero))

