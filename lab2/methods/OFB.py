class OFB:
    def __init__(self, blocks, block_size, iv, encrypt_func=None, decrypt_func=None):
        self.__blocks = blocks
        self.__block_size = block_size
        self.__iv = iv
        self.custom_E_k = encrypt_func
        self.custom_D_k = decrypt_func

    def encode(self, key_byte=0x55):
        new_blocks = []
        O_sequence = self.generate_O(key_byte)
        for i in range(len(self.__blocks)):
            data = self.__blocks[i]
            O_block = O_sequence[i]
            cipher_bytes = bytearray()
            for j in range(len(data)):
                cipher_bytes.append(data[j] ^ O_block[j])
            new_blocks.append(bytes(cipher_bytes))

        self.__blocks = new_blocks
        return new_blocks

    def decode(self, key_byte=0x55):
        return self.encode(key_byte)

    def generate_O(self, key_byte=0x55):
        O_list = []
        O = bytes([self.__iv]) * self.__block_size
        for _ in range(len(self.__blocks)):
            # O = self.E_k(O, key_byte)
            if self.custom_E_k:
                O = self.custom_E_k(O, key_byte)
            else:
                O = self.E_k(O, key_byte)
            O_list.append(O)
        return O_list

    def E_k(self, data, key=0x55):
        return bytes([b ^ key for b in data])
