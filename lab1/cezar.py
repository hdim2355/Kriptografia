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
    cols = len(ciphertext) // circumference
    output = ""
    for i in range(circumference-1,0,-1):
        for j in range(cols,-1,-1):
            output += ciphertext[j * cols + i-1]
    return output[::-1]

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

print(decrypt_railfence("WECRLTEERDSOEEFEAOCAIVDEN",3))
