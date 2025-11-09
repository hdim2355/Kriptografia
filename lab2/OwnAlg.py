class CustomCipher:
    def __init__(self, blocks, block_size):
        self.__blocks = blocks
        self.__block_size = block_size

    def encode(self, key):
        new_blocks = []
        for block in self.__blocks:
            encrypted_block = self.E_k(block, key)
            new_blocks.append(encrypted_block)
        self.__blocks = new_blocks
        return new_blocks

    def decode(self, key):
        new_blocks = []
        for block in self.__blocks:
            decrypted_block = self.D_k(block, key)
            new_blocks.append(decrypted_block)
        self.__blocks = new_blocks
        return new_blocks

    def E_k(self, data, key):
        result = bytearray()
        key_str = str(key)
        for i, byte in enumerate(data):
            key_char = ord(key_str[i % len(key_str)])
            encrypted = (byte + key_char) % 256
            result.append(encrypted)
        return bytes(result)

    def D_k(self, data, key):
        result = bytearray()
        key_str = str(key)
        for i, byte in enumerate(data):
            key_char = ord(key_str[i % len(key_str)])
            decrypted = (byte - key_char) % 256
            result.append(decrypted)
        return bytes(result)