class CBC:
    def __init__(self, blocks, block_size, iv, encrypt_func=None, decrypt_func=None):
        self.__blocks = blocks
        self.__block_size = block_size
        self.__iv = iv
        self.custom_E_k = encrypt_func
        self.custom_D_k = decrypt_func

    def encode(self, key_byte=0x55):
        new_blocks = []
        C = bytes([self.__iv]) * self.__block_size if self.__block_size > 0 else len(self.__blocks[0])
        for data in self.__blocks:
            xor_bytes = bytearray()
            for i in range(len(data)):
                xor_bytes.append(data[i] ^ C[i])
            xor_res = bytes(xor_bytes)
            # Ci = self.E_k(xor_res, key_byte)
            if self.custom_E_k:
                Ci = self.custom_E_k(xor_res, key_byte)
            else:
                Ci = self.E_k(xor_res, key_byte)
            new_blocks.append(Ci)
            C = Ci
        self.__blocks = new_blocks
        return new_blocks

    def decode(self, key_byte=0x55):
        new_blocks = []
        D = bytes([self.__iv]) * len(self.__blocks[0]) if self.__blocks else b''
        for data in self.__blocks:
            if self.custom_D_k:
                Di = self.custom_D_k(data, key_byte)
            else:
                Di = self.D_k(data, key_byte)
            xor_bytes = bytearray()
            for i in range(len(Di)):
                xor_bytes.append(Di[i] ^ D[i])
            plain_block = bytes(xor_bytes)
            new_blocks.append(plain_block)
            D = data
        self.__blocks = new_blocks
        return new_blocks

    def E_k(self, data, key=0x55):
        return bytes([b ^ key for b in data])

    def D_k(self, data, key=0x55):
        return self.E_k(data, key)
