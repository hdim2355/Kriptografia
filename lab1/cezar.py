ascii_256 = ''.join(chr(i) for i in range(256))
print(ascii_256)
print(f"Hossz: {len(ascii_256)}")  # 256
print(f"Első 32 karakter (vezérlőkarakterek): {ascii_256[:32]!r}")
print(f"Nyomtatható karakterek: {ascii_256[32:127]}")