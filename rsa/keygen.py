"""Génération des clés RSA."""

import math
import secrets


def is_prime(n: int) -> bool:
    """Teste si n est un nombre premier."""
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    divisor = 3

    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2

    return True


def generate_prime(bit_size: int) -> int:
    """Génère un nombre premier de la taille demandée."""
    while True:
        candidate = secrets.randbits(bit_size)

        # Force le nombre à avoir la taille demandée
        candidate |= (1 << (bit_size - 1))

        # Force le nombre à être impair
        candidate |= 1

        if is_prime(candidate):
            return candidate


def extended_gcd(a: int, b: int):
    """Algorithme d'Euclide étendu."""
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y


def mod_inverse(e: int, phi_n: int) -> int:
    """Calcule l'inverse de e modulo phi(n)."""
    gcd, x, _ = extended_gcd(e, phi_n)

    if gcd != 1:
        raise ValueError("e et phi(n) ne sont pas premiers entre eux.")

    return x % phi_n


def choose_e(phi_n: int) -> int:
    """Choisit e premier avec phi(n)."""

    candidates = [65537, 257, 17, 5, 3]

    for e in candidates:
        if e < phi_n and math.gcd(e, phi_n) == 1:
            return e

    e = 3

    while e < phi_n:
        if math.gcd(e, phi_n) == 1:
            return e

        e += 2

    raise ValueError("Impossible de trouver e.")


def generate_keypair(bit_size: int = 16):
    """
    Génère une paire de clés RSA.

    Clé publique  : (n, e)
    Clé privée    : (n, d)
    """

    # Génération de p et q
    p = generate_prime(bit_size)
    q = generate_prime(bit_size)

    # Évite p = q
    while q == p:
        q = generate_prime(bit_size)

    # n = p × q
    n = p * q

    # phi(n) = (p - 1)(q - 1)
    phi_n = (p - 1) * (q - 1)

    # Choix de e
    e = choose_e(phi_n)

    # d = inverse de e modulo phi(n)
    d = mod_inverse(e, phi_n)

    return {
        "public_key": (n, e),
        "private_key": (n, d),
        "p": p,
        "q": q,
        "phi_n": phi_n,
        "e": e,
        "d": d,
    }