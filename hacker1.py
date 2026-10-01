  GNU nano 9.2                                  hacker1.py
import time

# ==========================================
# HACKER 1 - Factorisation de n
# ==========================================

# Pour commencer, on met ici un n connu.
# Plus tard, Vladimir récupérera n depuis Alice.
n = 1009 * 1013

print("=== HACKER 1 ===")
print("n =", n)

# Début de la mesure du temps
debut = time.perf_counter()

# Recherche des facteurs p et q
p = None
q = None

for i in range(2, int(n ** 0.5) + 1):
    if n % i == 0:
        p = i
        q = n // i
        break

# Fin de la mesure
fin = time.perf_counter()

if p is not None:
    print("Facteur p =", p)
    print("Facteur q =", q)
    print("Temps de factorisation =", fin - debut, "secondes")
else:
    print("Impossible de factoriser n")


