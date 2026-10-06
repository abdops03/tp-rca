from alice import Alice
from bob import Bob
from hacker1 import Hacker1

# ==========================
# 1. ALICE
# ==========================

alice = Alice(key_bit_size=16)

# Alice donne uniquement sa clé publique
public_key = alice.send_public_key()

print("Clé publique :", public_key)


# ==========================
# 2. BOB
# ==========================

bob = Bob(public_key)

message = "Bonjour Alice !"

cipher_list = bob.encrypt_message(message)

print("Message original :", message)
print("Message chiffré  :", cipher_list)


# ==========================
# 3. ALICE
# ==========================

message_dechiffre = alice.receive_and_decrypt(cipher_list)

print("Message déchiffré :", message_dechiffre)


# ==========================
# 4. HACKER 1 - VLADIMIR
# ==========================

hacker = Hacker1(public_key, cipher_list)

hacker.attack()
