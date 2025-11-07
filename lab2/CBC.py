class CBC:
    def __init__(self, blocks, block_size, iv):
        self.__blocks = blocks
        self.__block_size = block_size
        self.__iv = iv

    def encode(self, key_byte=0x55):
        new_blocks = []
        C = bytes([self.__iv]) * len(self.__blocks[0]) if self.__blocks else b''
        for data in self.__blocks:
            xor_bytes = bytearray()
            for i in range(len(data)):
                xor_bytes.append(data[i] ^ C[i])
            xor_res = bytes(xor_bytes)
            Ci = self.E_k(xor_res, key_byte)
            new_blocks.append(Ci)
            C = Ci
        self.__blocks = new_blocks
        return new_blocks

    def decode(self, key_byte=0x55):
        new_blocks = []
        prev_cipher = bytes([self.__iv]) * len(self.__blocks[0]) if self.__blocks else b''
        for cipher_block in self.__blocks:
            decrypted = self.D_k(cipher_block, key_byte)
            plain_bytes = bytearray()
            for i in range(len(decrypted)):
                plain_bytes.append(decrypted[i] ^ prev_cipher[i])
            plain_block = bytes(plain_bytes)
            new_blocks.append(plain_block)
            prev_cipher = cipher_block
        self.__blocks = new_blocks
        return new_blocks

    def E_k(self, data, key=0x55):
        return bytes([b ^ key for b in data])

    def D_k(self, data, key=0x55):
        return self.E_k(data, key)
