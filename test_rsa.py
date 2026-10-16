from alice import Alice
from bob import Bob


# 1. Alice génère ses clés
alice = Alice()

# 2. Alice envoie sa clé publique à Bob
public_key = alice.send_public_key()

print("Clé publique d'Alice :", public_key)

# 3. Bob reçoit la clé publique
bob = Bob(public_key)

# 4. Bob prépare son message
message = "Bonjour Alice"

# 5. Bob chiffre le message
message_chiffre = bob.encrypt_message(message)

print("Message original :", message)
print("Message chiffré :", message_chiffre)

# 6. Alice reçoit et déchiffre
message_dechiffre = alice.receive_and_decrypt(message_chiffre)

print("Message déchiffré par Alice :", message_dechiffre)