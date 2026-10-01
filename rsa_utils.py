# rsa_utils.py

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
