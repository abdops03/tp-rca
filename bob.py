"""Bob : reçoit la clé publique d'Alice et chiffre un message."""

from rsa.cipher import encrypt_text


class Bob:
    def __init__(self, public_key: tuple[int, int]):
        self.public_key = public_key

    def encrypt_message(self, message: str) -> list[int]:
        """Bob chiffre le message avec la clé publique d'Alice."""
        return encrypt_text(message, self.public_key)