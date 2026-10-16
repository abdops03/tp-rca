
import numpy as np
from itertools import product as combinaisons
from reed_solomon import redond, syndromes


def texte_vers_bits(texte):
    """Convertit chaque caractère en 8 bits."""
    bits = []
    for caractere in texte:
        bits.extend(
            int(bit) for bit in format(ord(caractere), "08b")
        )
    return bits


def bits_vers_symboles(bits):
    """Découpe les bits en symboles de 3 bits."""
    return [
        bits[i:i + 3]
        for i in range(0, len(bits), 3)
    ]


def encoder_bloc(symboles):
    """Calcule les 4 symboles de redondance."""
    if len(symboles) != 3:
        raise ValueError(
            "Un bloc doit contenir exactement 3 symboles utiles."
        )

    a2, a1, a0 = symboles
    redondance = redond(a2, a1, a0)
    redondance = [list(symbole) for symbole in redondance]

    return [symbole.copy() for symbole in symboles] + redondance


def encoder_texte(texte):
    """Encode le texte par blocs de 3 symboles utiles."""
    bits = texte_vers_bits(texte)

    # Complète jusqu'à obtenir un nombre de bits multiple de 9.
    while len(bits) % 9 != 0:
        bits.append(0)

    symboles = bits_vers_symboles(bits)
    blocs_codes = []

    for i in range(0, len(symboles), 3):
        bloc = symboles[i:i + 3]
        blocs_codes.append(encoder_bloc(bloc))

    return blocs_codes


def noise(a, p=0.01):
    """Ajoute du bruit aléatoire à un symbole de 3 bits."""
    c = []

    for bit in a:
        if np.random.uniform() < p:
            c.append(1 - int(bit))
        else:
            c.append(int(bit))

    return c


def calculer_syndromes(bloc):
    """Calcule les syndromes d'un bloc de 7 symboles."""
    if len(bloc) != 7:
        raise ValueError(
            "Un bloc transmis doit contenir 7 symboles."
        )

    a2, a1, a0, r3, r2, r1, r0 = bloc
    return syndromes(a2, a1, a0, r3, r2, r1, r0)


def syndromes_nuls(bloc):
    """Vérifie si tous les syndromes sont nuls."""
    resultats = calculer_syndromes(bloc)

    return all(
        list(syndrome) == [0, 0, 0]
        for syndrome in resultats
    )


def corriger_une_erreur(bloc):
    """Recherche une correction en modifiant un seul symbole."""
    if syndromes_nuls(bloc):
        return [s.copy() for s in bloc], None

    for position in range(len(bloc)):
        for valeur in combinaisons([0, 1], repeat=3):
            valeur = list(valeur)

            if valeur == [int(bit) for bit in bloc[position]]:
                continue

            candidat = [s.copy() for s in bloc]
            candidat[position] = valeur

            if syndromes_nuls(candidat):
                return candidat, position

    return None, None


def decoder_texte(blocs_corriges, longueur_originale):
    """Reconstruit le texte à partir des blocs corrigés."""
    bits = []

    for bloc in blocs_corriges:
        for symbole in bloc[:3]:
            bits.extend(int(bit) for bit in symbole)

    bits = bits[:longueur_originale * 8]
    texte = ""

    for i in range(0, len(bits), 8):
        octet = bits[i:i + 8]

        if len(octet) == 8:
            valeur = int("".join(map(str, octet)), 2)
            texte += chr(valeur)

    return texte


if __name__ == "__main__":
    texte = input("Texte à encoder : ")
    longueur_originale = len(texte)

    blocs = encoder_texte(texte)
    blocs_corriges = []

    for numero, bloc in enumerate(blocs, start=1):
        print(f"\n--- Bloc {numero} ---")
        print("Symboles utiles :", bloc[:3])
        print("Redondance      :", bloc[3:])
        print("Bloc transmis   :", bloc)

        print(
            "Syndromes sans erreur :",
            calculer_syndromes(bloc)
        )

        # Simule le bruit sur les 7 symboles transmis.
        bloc_recu = [
            noise(symbole, p=0.01)
            for symbole in bloc
        ]

        print("Bloc reçu avec bruit :", bloc_recu)

        print(
            "Syndromes avec erreur :",
            calculer_syndromes(bloc_recu)
        )

        bloc_corrige, position = corriger_une_erreur(bloc_recu)

        if bloc_corrige is not None:
            blocs_corriges.append(bloc_corrige)
            print("Bloc corrigé :", bloc_corrige)

            if position is not None:
                print("Position corrigée :", position)
            else:
                print("Aucune erreur détectée.")

            print(
                "Syndromes après correction :",
                calculer_syndromes(bloc_corrige)
            )
        else:
            print("Aucune correction trouvée.")

    if len(blocs_corriges) == len(blocs):
        texte_decode = decoder_texte(
            blocs_corriges,
            longueur_originale
        )

        print("\nTexte original :", texte)
        print("Texte décodé   :", texte_decode)
    else:
        print(
            "\nDécodage incomplet : au moins un bloc "
            "n'a pas pu être corrigé."
        )
