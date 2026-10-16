import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def dechiffrer_aes192_cbc(message_b64: str, cle: bytes, iv: bytes) -> str:
    if len(cle) != 24:
        raise ValueError(f"La clé doit faire exactement 24 octets (reçu : {len(cle)})")
    if len(iv) != 16:
        raise ValueError(f"L'IV doit faire exactement 16 octets (reçu : {len(iv)})")

    donnees_chiffrees = base64.b64decode(message_b64)
    cipher = Cipher(algorithms.AES(cle), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    donnees_paddes = decryptor.update(donnees_chiffrees) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    donnees_claires = unpadder.update(donnees_paddes) + unpadder.finalize()

    return donnees_claires.decode('utf-8')

if __name__ == "__main__":
    # Remplace par tes vraies clés/messages du TP
    CLE_24_OCTETS = b"123456789012345678901234"
    IV_16_OCTETS  = b"1234567890123456"
    MESSAGE_CHIFFRE_B64 = "TON_MESSAGE_BASE64"

    try:
        print("Message déchiffré :", dechiffrer_aes192_cbc(MESSAGE_CHIFFRE_B64, CLE_24_OCTETS, IV_16_OCTETS))
    except Exception as e:
        print("Erreur :", e)
