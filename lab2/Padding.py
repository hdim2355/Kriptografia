class Padding:
    def __init__(self):
        pass

    def zero_padding(self, data, block_size):
        pad = block_size - (len(data) % block_size)
        return data + bytes([0] * pad) if len(data) % block_size != 0 else data

    def des_padding(self, data, block_size):
        pad = block_size - (len(data) % block_size)
        return data + bytes([0x80]) + bytes([0x00] * (pad - 1)) if len(data) % block_size != 0 else data

    def schneier_padding(self, data, block_size):
        pad = block_size - (len(data) % block_size)
        return data + bytes([pad] * pad) if len(data) % block_size != 0 else data

    def zero_unpadding(self, data):
        return data.rstrip(b'\x00')

    def des_unpadding(self, data):
        if data and data[-1] == 0x00:
            pos = data.rfind(b'\x80')
            if pos != -1:
                return data[:pos]
        return data

    def schneier_unpadding(self, data):
        if data:
            padding_length = data[-1]
            if 0 < padding_length <= len(data):
                return data[:-padding_length]
        return data
