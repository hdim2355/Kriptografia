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
        plaintext = plaintext.upper()
        keyword = keyword.upper()
        for i in range(len(plaintext)):
            if plaintext[i] != " ":
                plval = letters.find(plaintext[i])
                keyval = letters.find(keyword[i])
                output += letters[(plval + keyval) % len(letters)]
            else:
                output += plaintext[i]
        return output
    except Exception as e:
        raise ValueError(f"Vigenere encryption failed: {str(e)}")

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
        ciphertext = ciphertext.upper()
        keyword = keyword.upper()
        output = ""
        for i in range(len(ciphertext)):
            if ciphertext[i] != " ":
                cival = letters.find(ciphertext[i])
                keyval = letters.find(keyword[i])
                output += letters[(cival - keyval) % len(letters)]
            else:
                output += ciphertext[i]
        return output
    except Exception as e:
        raise ValueError(f"Vigenere cypher decryption failed: {str(e)}")

def encrypt_scytale(plaintext, circumference): #5
    # plaintext.upper()
    while len(plaintext) % circumference != 0:
        plaintext += "X"
    cols = len(plaintext) // circumference #4
    output = ""
    for i in range(circumference):
        for j in range(cols):
            output += plaintext[j * circumference + i]
    return output

def decrypt_scytale(ciphertext, circumference):
    while len(ciphertext) % circumference != 0:
        ciphertext += "X"
    cols = len(ciphertext)//circumference
    lists = [[] for _ in range(len(ciphertext)//circumference)]
    for i in range(circumference):
        for j in range(len(ciphertext)//circumference):
            lists[j].append(ciphertext[i*cols + j])
    output = ""
    for list in lists:
        for char in list:
            output += char
    return output.replace("X","")

# print(encrypt_scytale("IAMHURTVERYBADLYHELP", 5))
# print(decrypt_scytale("IRYYATBHMVAEHEDLURLP",5))

def encrypt_railfence(plaintext,rails):
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

# print(encrypt_railfence("WEAREDISCOVEREDFLEEATONCE", 3))
def decrypt_railfence(ciphertext, rails):
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

# print(decrypt_railfence("WECRLTEERDSOEEFEAOCAIVDEN",3))
# print("\n\n")
#
# print(encrypt_scytale("HELLO", 3))
# print(encrypt_scytale("WEAREDISCOVERED", 4))
# print(encrypt_scytale("ATTACKATDAWN", 6))
#
# print("\n")
#
# print(decrypt_scytale("HLEOL", 3))
# print(decrypt_scytale("WECREDOEAIVDRSEX", 4))
# print(decrypt_scytale("AATTTDAACWKN", 6))



# print("\n\n\n")
#
print(f"WEAREDISCOVEREDFLEEATONCE={encrypt_railfence('WEAREDISCOVEREDFLEEATONCE', 3)}")
print(f"DEFENDTHEEASTWALLOFTHECASTLE={encrypt_railfence("DEFENDTHEEASTWALLOFTHECASTLE", 4)}")
print(f"HELLOWORLD={encrypt_railfence("HELLOWORLD", 4)}")

print("\n")

print(f"WECRLTEERDSOEEFEAOCAIVDEN={decrypt_railfence("WECRLTEERDSOEEFEAOCAIVDEN", 3)}")
print(f"DTTFSEDHSWOTATFNEAALHCLEELEE={decrypt_railfence("DTTFSEDHSWOTATFNEAALHCLEELEE", 4)}")
print(f"HOEWRLOLLD={decrypt_railfence("HOEWRLOLLD", 4)}")

print("\n")
# print("\n\n")

print(f"ATTACKATDAWN={encrypt_vigenere("ATTACKATDAWN", "LEMON")}")
print(f"LXFOPVEFRNHR={decrypt_vigenere("LXFOPVEFRNHR", "LEMON")}")

print(f"iagreewithyouthatsoundslikeagoodidea={encrypt_vigenere("iagreewithyouthatsoundslikeagoodidea", "LEMON")}")
print(f"tesfrpauhujsghulxechyhezvvimubzhurrl={decrypt_vigenere("tesfrpauhujsghulxechyhezvvimubzhurrl", "LEMON")}")

print(f"GEEKSFORGEEKS={encrypt_vigenere("GEEKSFORGEEKS", "AYUSH")}")
print(f"GCYCZFMLYLEIM={decrypt_vigenere("GCYCZFMLYLEIM", "AYUSH")}")


# Teszt fájlok létrehozása Pythonnal
def create_test_files():
    """Create test binary files for demonstration."""

    # 1. Egyszerű szöveges fájl
    with open('assign1/test.bin', 'wb') as f:
        f.write(b"Hello Binary World!\nThis is a test file.")

    # 2. Numerikus adatok
    with open('assign1/numbers.bin', 'wb') as f:
        f.write(b"0123456789\nABCDEF")

    # 3. Speciális karakterek
    with open('assign1/special.bin', 'wb') as f:
        f.write(b"!@#$%^&*()\nTEST{123}")

    # 4. Tiszta byte-ok
    with open('assign1/bytes.bin', 'wb') as f:
        f.write(bytes([65, 66, 67, 68, 69, 10, 97, 98, 99, 100, 101]))

    print("Test files created successfully!")


# if __name__ == '__main__':
#     create_test_files()