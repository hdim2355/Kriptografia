class CFB:
    def __init__(self, blocks, block_size, iv):
        self.__blocks = blocks
        self.__block_size = block_size
        self.__iv = iv

    def encode(self, key_byte=0x55):
        new_blocks = []
        C = bytes([self.__iv]) * self.__block_size if self.__block_size > 0 else len(self.__blocks[0])
        for data in self.__blocks:
            E = self.E_k(C, key_byte)
            C = bytearray()
            for i in range(len(data)):
                C.append(data[i] ^ E[i])
            new_blocks.append(bytes(C))
        self.__blocks = new_blocks
        return new_blocks

    def decode(self, key_byte=0x55):
        new_blocks = []
        prev_cipher = bytes([self.__iv]) * self.__block_size if self.__block_size > 0 else len(self.__blocks[0])
        for cipher_block in self.__blocks:
            E = self.E_k(prev_cipher, key_byte)
            plain_bytes = bytearray()
            for i in range(len(cipher_block)):
                plain_bytes.append(cipher_block[i] ^ E[i])
            plain_block = bytes(plain_bytes)
            new_blocks.append(plain_block)
            prev_cipher = cipher_block
        self.__blocks = new_blocks
        return new_blocks


    def E_k(self, data, key=0x55):
        return bytes([b ^ key for b in data])

    def D_k(self, data, key=0x55):
        return self.E_k(data, key)