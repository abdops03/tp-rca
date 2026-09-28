"""Alice : génère les clés RSA, envoie sa clé publique à Bob, reçoit et
déchiffre le message chiffré avec sa clé privée."""

from rsa.keygen import generate_keypair
from rsa.cipher import decrypt_text


class Alice:
    def __init__(self, key_bit_size: int = 16):
        keys = generate_keypair(bit_size=key_bit_size)
        self._private_key = keys["private_key"]  # (n, d) -- jamais partagée
        self.public_key = keys["public_key"]      # (n, e) -- envoyée à Bob
        self._debug_keys = keys  # p, q, phi_n gardés pour affichage pédagogique

    def send_public_key(self) -> tuple[int, int]:
        """Étape 1 du schéma : Alice envoie sa clé publique."""
        return self.public_key

    def receive_and_decrypt(self, cipher_list: list[int]) -> str:
        """Étape 3 du schéma : Alice décode le message avec sa clé privée."""
        return decrypt_text(cipher_list, self._private_key)
