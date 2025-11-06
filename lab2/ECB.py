class ECB:
    def __init__(self,blocks,block_size):
        self.__blocks = blocks
        self.__block_size = block_size

    def encode(self,key_byte=0x55):
        new_blocks = []
        for data in self.__blocks:
            block_byte_i = bytes([b ^ key_byte for b in data])
            new_blocks.append(block_byte_i)
        return new_blocks

    def decode(self):
        return
