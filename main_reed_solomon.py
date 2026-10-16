
from itertools import product as combinaisons
from reed_solomon import redond, syndromes


def texte_vers_bits(texte):
    """Convertit chaque caractère en une suite de 8 bits."""
    bits = []
    for caractere in texte:
        bits.extend(
            int(bit)
            for bit in format(ord(caractere), "08b")
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
    """Convertit le texte et encode les blocs de 3 symboles."""
    bits = texte_vers_bits(texte)

    # Un bloc utile contient 9 bits.
    while len(bits) % 9 != 0:
        bits.append(0)

    symboles = bits_vers_symboles(bits)
    blocs_codes = []

    for i in range(0, len(symboles), 3):
        bloc = symboles[i:i + 3]
        blocs_codes.append(encoder_bloc(bloc))

    return blocs_codes


def ajouter_bruit(symbole):
    """Inverse volontairement le premier bit d'un symbole."""
    symbole_errone = symbole.copy()
    symbole_errone[0] = 1 - int(symbole_errone[0])
    return symbole_errone


def calculer_syndromes(bloc):
    """Calcule les 4 syndromes d'un bloc de 7 symboles."""
    if len(bloc) != 7:
        raise ValueError(
            "Un bloc transmis doit contenir 7 symboles."
        )

    a2, a1, a0, r3, r2, r1, r0 = bloc
    return syndromes(a2, a1, a0, r3, r2, r1, r0)


def syndromes_nuls(bloc):
    """Vérifie si les quatre syndromes sont nuls."""
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
        # Les trois premiers symboles contiennent les données utiles.
        for symbole in bloc[:3]:
            bits.extend(int(bit) for bit in symbole)

    # Retire les bits de remplissage ajoutés pendant l'encodage.
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

        # Vérification du bloc sans erreur.
        resultat = calculer_syndromes(bloc)
        print("Syndromes sans erreur :", resultat)

        # Copie du bloc pour simuler une erreur.
        bloc_recu = [symbole.copy() for symbole in bloc]

        # Test : ajoute une erreur au premier symbole.
        bloc_recu[0] = ajouter_bruit(bloc_recu[0])

        print("Bloc reçu avec bruit :", bloc_recu)

        # Calcul des syndromes après l'erreur.
        resultat_erreur = calculer_syndromes(bloc_recu)
        print("Syndromes avec erreur :", resultat_erreur)

        # Recherche de la correction.
        bloc_corrige, position = corriger_une_erreur(bloc_recu)

        if bloc_corrige is not None:
            blocs_corriges.append(bloc_corrige)

            print("Bloc corrigé :", bloc_corrige)

            if position is not None:
                print("Symbole corrigé, position :", position)
            else:
                print("Aucune erreur détectée.")

            print(
                "Syndromes après correction :",
                calculer_syndromes(bloc_corrige)
            )
        else:
            print("Aucune correction trouvée.")

    # Reconstruit le texte seulement si tous les blocs ont été corrigés.
    if len(blocs_corriges) == len(blocs):
        texte_decode = decoder_texte(
            blocs_corriges,
            longueur_originale
        )

        print("\nTexte original :", texte)
        print("Texte décodé   :", texte_decode)
