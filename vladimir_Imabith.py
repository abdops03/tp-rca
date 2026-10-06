from math import isqrt, gcd


# ==========================================================
# AFFICHAGE
# ==========================================================

def afficher_titre(titre):
    print("\n" + "=" * 60)
    print(titre)
    print("=" * 60)


# ==========================================================
# FACTORISATION DE n
# ==========================================================

def factoriser_n(n):
    """
    Recherche p et q tels que :

        n = p * q

    Fonction adaptée aux petites clés RSA utilisées en TP.
    """

    print(f"\n[+] Recherche des facteurs de n = {n}...")

    if n % 2 == 0:
        return 2, n // 2

    limite = isqrt(n)

    for p in range(3, limite + 1, 2):

        if n % p == 0:

            q = n // p

            return p, q

    return None, None


# ==========================================================
# RECONSTRUCTION DE LA CLE PRIVEE
# ==========================================================

def reconstruire_cle_privee(n, e):

    afficher_titre("RECONSTRUCTION DE LA CLE PRIVEE")

    print(f"Clé publique reçue : ({n}, {e})")

    # ------------------------------------------------------
    # 1. Factoriser n
    # ------------------------------------------------------

    p, q = factoriser_n(n)

    if p is None or q is None:
        raise ValueError(
            "Impossible de factoriser n avec cette méthode."
        )

    print("\n[+] Factorisation réussie")

    print(f"p = {p}")
    print(f"q = {q}")

    print(f"\nVérification :")
    print(f"{p} × {q} = {p * q}")

    # ------------------------------------------------------
    # 2. Calcul de phi(n)
    # ------------------------------------------------------

    phi = (p - 1) * (q - 1)

    print("\n[+] Calcul de phi(n)")

    print(
        f"phi(n) = ({p} - 1) × ({q} - 1)"
    )

    print(f"phi(n) = {phi}")

    # ------------------------------------------------------
    # 3. Vérification
    # ------------------------------------------------------

    if gcd(e, phi) != 1:

        raise ValueError(
            "e n'est pas premier avec phi(n)."
        )

    # ------------------------------------------------------
    # 4. Calcul de d
    # ------------------------------------------------------

    d = pow(e, -1, phi)

    print("\n[+] Calcul de d")

    print(
        f"d = inverse de {e} modulo {phi}"
    )

    print(f"d = {d}")

    afficher_titre("CLE PRIVEE RETROUVEE")

    print(f"Clé publique : ({n}, {e})")
    print(f"Clé privée   : ({n}, {d})")

    return d


# ==========================================================
# DECHIFFREMENT
# ==========================================================

def dechiffrer_message(message_chiffre, d, n):

    afficher_titre("DECHIFFREMENT")

    texte = ""

    for numero, bloc in enumerate(message_chiffre, start=1):

        # Formule RSA :
        # m = c^d mod n

        m = pow(bloc, d, n)

        try:
            caractere = chr(m)

        except ValueError:
            caractere = "?"

        texte += caractere

        print(
            f"Bloc {numero:02d} : "
            f"{bloc} -> {m} -> {repr(caractere)}"
        )

    return texte


# ==========================================================
# LECTURE DU MESSAGE CHIFFRE
# ==========================================================

def lire_message_chiffre():

    print("""
Entre les nombres du message chiffré séparés par des espaces.

Exemple :

2790 1307 1859 1859 2185
""")

    entree = input("Message chiffré : ")

    # Autorise aussi les virgules
    entree = entree.replace(",", " ")

    nombres = entree.split()

    message = []

    for nombre in nombres:
        message.append(int(nombre))

    return message


# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================

def main():

    afficher_titre("VLADIMIR - ATTAQUE RSA DU TP")

    print("""
Alice doit me fournir :

    1. n
    2. e
    3. le message chiffré

Je ne connais pas :

    p
    q
    d

Le programme va tenter de les retrouver.
""")

    # ------------------------------------------------------
    # CLE PUBLIQUE DONNEE PAR ALICE
    # ------------------------------------------------------

    n = int(
        input("Alice - valeur de n : ")
    )

    e = int(
        input("Alice - valeur de e : ")
    )

    # ------------------------------------------------------
    # MESSAGE CHIFFRE DONNE PAR ALICE
    # ------------------------------------------------------

    message_chiffre = lire_message_chiffre()

    afficher_titre("INFORMATIONS RECUES D'ALICE")

    print(f"Clé publique : ({n}, {e})")

    print("\nMessage chiffré :")

    print(message_chiffre)

    # ------------------------------------------------------
    # RECONSTRUCTION CLE PRIVEE
    # ------------------------------------------------------

    d = reconstruire_cle_privee(
        n,
        e
    )

    # ------------------------------------------------------
    # DECHIFFREMENT
    # ------------------------------------------------------

    message = dechiffrer_message(
        message_chiffre,
        d,
        n
    )

    afficher_titre("MESSAGE RETROUVE")

    print(message)


# ==========================================================
# LANCEMENT
# ==========================================================

if __name__ == "__main__":
    main()
