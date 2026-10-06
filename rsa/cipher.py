"""Chiffrement et déchiffrement RSA."""


def encrypt(message: int, public_key: tuple[int, int]) -> int:
    """Chiffre un entier avec la clé publique (n, e)."""
    n, e = public_key

    if message >= n:
        raise ValueError(
            "Le message est trop grand pour cette clé RSA."
        )

    return pow(message, e, n)


def decrypt(cipher: int, private_key: tuple[int, int]) -> int:
    """Déchiffre un entier avec la clé privée (n, d)."""
    n, d = private_key

    return pow(cipher, d, n)


def encrypt_text(
    message: str,
    public_key: tuple[int, int]
) -> list[int]:
    """Chiffre chaque caractère du message."""
    return [
        encrypt(ord(character), public_key)
        for character in message
    ]


def decrypt_text(
    cipher_list: list[int],
    private_key: tuple[int, int]
) -> str:
    """Déchiffre une liste d'entiers RSA."""
    return "".join(
        chr(decrypt(cipher, private_key))
        for cipher in cipher_list
    )