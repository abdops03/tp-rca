import time
import math


class Hacker1:

    def __init__(self, public_key, cipher_list):
        # Le hacker intercepte uniquement ces informations
        self.n, self.e = public_key
        self.cipher_list = cipher_list

    def extended_gcd(self, a, b):
        if b == 0:
            return a, 1, 0

        gcd, x1, y1 = self.extended_gcd(b, a % b)

        x = y1
        y = x1 - (a // b) * y1

        return gcd, x, y

    def mod_inverse(self, e, phi_n):
        gcd, x, _ = self.extended_gcd(e, phi_n)

        if gcd != 1:
            raise ValueError("Impossible de calculer l'inverse")

        return x % phi_n

    def attack(self):
        print("\n=== HACKER 1 - VLADIMIR ===")
        print("n =", self.n)
        print("e =", self.e)

        # ==========================
        # 1. Factorisation
        # ==========================

        debut = time.perf_counter()

        p = None
        q = None

        for i in range(2, math.isqrt(self.n) + 1):
            if self.n % i == 0:
                p = i
                q = self.n // i
                break

        fin = time.perf_counter()

        if p is None:
            print("Impossible de factoriser n")
            return

        print("Facteur p =", p)
        print("Facteur q =", q)
        print("Temps de factorisation =", fin - debut, "secondes")

        # ==========================
        # 2. Calcul de phi(n)
        # ==========================

        phi_n = (p - 1) * (q - 1)

        print("phi(n) =", phi_n)

        # ==========================
        # 3. Retrouver d
        # ==========================

        d = self.mod_inverse(self.e, phi_n)

        print("d =", d)

        # ==========================
        # 4. Déchiffrement
        # ==========================

        message = ""

        for cipher in self.cipher_list:
            character = pow(cipher, d, self.n)
            message += chr(character)

        print("Message retrouvé :", message)
