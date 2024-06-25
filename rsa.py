import math
import random
import sys
from sympy import randprime, mod_inverse


def getPrime():
    lower_bound = 2 ** (64 - 1)
    upper_bound = 2 ** 64 - 1

    prime = randprime(lower_bound, upper_bound)

    return prime


def encrypt(message, e, n):
    e = int(e)
    n = int(n)
    encrypted_message = []

    for m in message:
        ascii = "{:03d}".format(ord(m))
        cipher_text = pow(int(ascii), e, n) # C = M^e mod N
        encrypted_message.append(hex(cipher_text))

    print("Cyphertext = ", ''.join(map(str, encrypted_message)))


def decrypt(encrypted_message, d, n):
    d = int(d)
    n = int(n)
    decrypted_message = ""

    encrypted_message = [int(encrypted_message[i:i+34], 16) for i in range(0, len(encrypted_message), 34)]

    for cipher_text in encrypted_message:
        ascii = pow(cipher_text, d, n) # M = C^d mod N

        character = chr(int(str(ascii)[:3]))
        decrypted_message += character

    print("Plaintext = ", decrypted_message)


def genkeys():
    p = getPrime()
    q = getPrime()

    while p == q:
        q = getPrime()

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randrange(1, phi_n)

    while math.gcd(e, phi_n) != 1:
        e = random.randrange(1, phi_n)

    d = mod_inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    print("Public_key = " + str(public_key))
    print("Private_key = " + str(private_key))


try:
    match sys.argv[1]:
        case "encrypt":
            encrypt(sys.argv[2], sys.argv[3], sys.argv[4])  #sys.argv[2] = message, sys.argv[3] = e, n = sys.argv[4]
        case "decrypt":
            decrypt(sys.argv[2], sys.argv[3], sys.argv[4])  #sys.argv[2] = cypertext, sys.argv[3] = d, n = sys.argv[4]
        case "genkeys":
            genkeys()
        case _:
            print("Wrong argument, please try again.")
except IndexError:
    print("Usage: python rsa.py [encrypt/decrypt/genkeys] [message] [private_key/public_key]")
