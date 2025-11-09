class CTR:
    def __init__(self, blocks, block_size, iv, encrypt_func=None, decrypt_func=None):
        self.__blocks = blocks
        self.__block_size = block_size
        self.__iv = iv
        self.custom_E_k = encrypt_func
        self.custom_D_k = decrypt_func

    def generate_N(self):
        N_sequence = []
        for i in range(len(self.__blocks)):
            N = bytes([(self.__iv + i) % 256]) * self.__block_size
            N_sequence.append(N)
        return N_sequence

    def encode(self, key_byte=0x55):
        new_blocks = []
        N_sequence = self.generate_N()

        for i in range(len(self.__blocks)):
            data = self.__blocks[i]
            N_block = N_sequence[i]
            # encrypted_N = self.E_k(N_block, key_byte)
            if self.custom_E_k:
                encrypted_N = self.custom_E_k(N_block, key_byte)
            else:
                encrypted_N = self.E_k(N_block, key_byte)
            cipher_bytes = bytearray()
            for j in range(len(data)):
                cipher_bytes.append(data[j] ^ encrypted_N[j])
            new_blocks.append(bytes(cipher_bytes))

        self.__blocks = new_blocks
        return new_blocks

    def decode(self, key_byte=0x55):
        return self.encode(key_byte)

    def E_k(self, data, key=0x55):
        return bytes([b ^ key for b in data])
