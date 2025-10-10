#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: <YOUR NAME>
SUNet: <SUNet ID>

Replace this with a description of the program.
"""
import random
import math
import utils
from lab1.assign1.utils import coprime


# Caesar Cipher

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    # raise NotImplementedError  # Your implementation here
    if not plaintext:
        return ""
    try:
        # plaintext = plaintext.upper()
        # letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letters = ''.join(chr(i) for i in range(256))
        key = 3
        output = ""
        for i in range(0, len(plaintext)):
            output += letters[(letters.find(plaintext[i]) + key) % len(letters)]
        return output
    except Exception as e:
        raise ValueError(f"Caesar encryption failed: {str(e)}")


def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    if not ciphertext:
        return ""
    try:
        # ciphertext = ciphertext.upper()
        # letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        letters = ''.join(chr(i) for i in range(256))
        KEY = 3
        output = ""
        for i in range(0, len(ciphertext)):
            output += letters[(letters.find(ciphertext[i]) - KEY) % len(letters)]
        return output
    except Exception as e:
        raise ValueError(f"Caesar decryption failed: {str(e)}")


# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if not plaintext:
        return ""
    try:
        output = ""
        while len(plaintext) > len(keyword):
            keyword += keyword
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(len(plaintext)):
            plval = letters.find(plaintext[i])
            keyval = letters.find(keyword[i])
            output += letters[(plval + keyval) % len(letters)]
        return output
    except Exception as e:
        raise ValueError(f"Railfence encryption failed: {str(e)}")

def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    if not ciphertext:
        return ""
    try:
        while len(ciphertext) > len(keyword):
            keyword += keyword
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        output = ""
        for i in range(len(ciphertext)):
            cival = letters.find(ciphertext[i])
            keyval = letters.find(keyword[i])
            output += letters[(cival - keyval) % len(letters)]
        return output
    except Exception as e:
        raise ValueError(f"Railfence decryption failed: {str(e)}")



# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    w = [1]
    for i in range(1, n):
        total = sum(w) + 1
        w.append(total)
    # print(f"{w}\n{utils.is_superincreasing(w)}")
    total = sum(w)
    q = random.randint(total + 1, total * 2)
    r = random.randint(2, q-1)
    print(w, q, r)
    while not math.gcd(r,q):
        r = random.randint(2, q - 1)
    return [tuple(w), int(q), int(r)]


def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    # print(f'ha:{private_key[0]}')
    w,q,r = private_key
    beta = [r*w_i % q for w_i in w]
    return tuple(beta)
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here


def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here


def encrypt_scytale(plaintext, circumference):
    if not plaintext:
        return ""
    try:
        # plaintext.upper()
        while len(plaintext) % circumference != 0:
            plaintext += "X"
        cols = len(plaintext) // circumference #4
        output = ""
        for i in range(circumference):
            for j in range(cols):
                output += plaintext[j * circumference + i]
        return output
    except Exception as e:
        raise ValueError(f"Scytale encryption failed: {str(e)}")

def decrypt_scytale(ciphertext, circumference):
    if not ciphertext:
        return ""
    try:
        while len(ciphertext) % circumference != 0:
            ciphertext += "X"
        cols = len(ciphertext) // circumference
        output = ""
        for i in range(circumference-1,0,-1):
            for j in range(cols,-1,-1):
                output += ciphertext[j * cols + i-1]
        return output[::-1]
    except Exception as e:
        raise ValueError(f"Scytale decryption failed: {str(e)}")

def encrypt_railfence(plaintext,rails):
    if not plaintext:
        return ""
    try:
        lists = [[] for _ in range(rails)]
        listIndex = 0
        direction = 1
        for char in plaintext:
            lists[listIndex].append(char)
            if listIndex == 0:
                direction = 1
            elif listIndex == rails - 1:
                direction = -1
            listIndex += direction
        output = ""
        for list in lists:
            for char in list:
                output += char
        return output
    except Exception as e:
        raise ValueError(f"Railfence encryption failed: {str(e)}")

def decrypt_railfence(ciphertext, rails):
    if not ciphertext:
        return ""
    try:
        rail_lengths = [0] * rails
        listIndex = 0
        direction = 1

        for _ in range(len(ciphertext)):
            rail_lengths[listIndex] += 1
            if listIndex == 0:
                direction = 1
            elif listIndex == rails - 1:
                direction = -1
            listIndex += direction
        lists = [[] for _ in range(rails)]

        index = len(ciphertext) - 1
        for rail in range(rails - 1, -1, -1):
            for _ in range(rail_lengths[rail]):
                lists[rail].append(ciphertext[index])
                index -= 1

        output = ""
        listIndex = 0
        direction = 1

        for _ in range(len(ciphertext)):
            output += lists[listIndex].pop()
            if listIndex == 0:
                direction = 1
            elif listIndex == rails - 1:
                direction = -1
            listIndex += direction

        return output
    except Exception as e:
        raise ValueError(f"Railfence decryption failed: {str(e)}")