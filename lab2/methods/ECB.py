class ECB:
    def __init__(self, blocks, block_size, encrypt_func=None, decrypt_func=None):
        self.__blocks = blocks
        self.__block_size = block_size
        self.custom_E_k = encrypt_func
        self.custom_D_k = decrypt_func

    def encode(self, key_byte=0x55):
        new_blocks = []
        for data in self.__blocks:
            if self.custom_E_k:
                block_byte_i = self.custom_E_k(data, key_byte)
            else:
                block_byte_i = self.E_k(data, key_byte)
            new_blocks.append(block_byte_i)
        self.__blocks = new_blocks
        return new_blocks

    def decode(self, key_byte=0x55):
        new_blocks = []
        for data in self.__blocks:
            if self.custom_E_k:
                block_byte_i = self.custom_D_k(data, key_byte)
            else:
                block_byte_i = self.E_k(data, key_byte)
            new_blocks.append(block_byte_i)
        self.__blocks = new_blocks
        return new_blocks

    def E_k(self, data, key=0x55):
        return bytes([b ^ key for b in data])
