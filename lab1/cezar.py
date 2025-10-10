# ascii_256 = ''.join(chr(i) for i in range(256))
# print(ascii_256)
# print(f"Hossz: {len(ascii_256)}")  # 256
# print(f"Első 32 karakter (vezérlőkarakterek): {ascii_256[:32]!r}")
# print(f"Nyomtatható karakterek: {ascii_256[32:127]}")


def encrypt_scytale(plaintext, circumference): #5
    # plaintext.upper()
    while len(plaintext) % circumference != 0:
        plaintext += "X"
    cols = len(plaintext) // circumference #4
    output = ""
    for i in range(circumference):
        for j in range(cols):
            output += plaintext[j * circumference + i]
    print(output)

plaintext = input()
encrypt_scytale(plaintext, 4) # eddig megy a decriptre is

def encrypt_railfence(val,n):
    m = n-2
    next = n + m
