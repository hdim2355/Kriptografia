import json
from ECB import ECB
from CBC import CBC
from CFB import CFB
from OFB import OFB
from CTR import CTR
from Padding import Padding


class Crypter(Padding):
    def __init__(self, file):
        super().__init__()
        self.config = self.load_config(file)
        self.mode_processors = self._init_mode_processors()
        self.padding_functions = self._init_padding_functions()

    def load_config(self, file):
        with open(file, 'r') as f:
            return json.load(f)

    def _init_mode_processors(self):
        return {
            'ECB': self._setup_ecb,
            'CBC': self._setup_cbc,
            'CFB': self._setup_cfb,
            'OFB': self._setup_ofb,
            'CTR': self._setup_ctr
        }

    def _setup_ecb(self, blocks, key, iv):
        return ECB(blocks, self.config['block_size_bits'])

    def _setup_cbc(self, blocks, key, iv):
        return CBC(blocks, self.config['block_size_bits'], iv)

    def _setup_cfb(self, blocks, key, iv):
        return CFB(blocks, self.config['block_size_bits'], iv)

    def _setup_ofb(self, blocks, key, iv):
        return OFB(blocks, self.config['block_size_bits'], iv)

    def _setup_ctr(self, blocks, key, iv):
        return CTR(blocks, self.config['block_size_bits'], iv)

    def _init_padding_functions(self):
        return {
            'zero': (self.zero_padding, self.zero_unpadding),
            'des': (self.des_padding, self.des_unpadding),
            'schneier': (self.schneier_padding, self.schneier_unpadding)
        }

    def process_blocks(self, data, operation):
        block_size_bytes = self.config['block_size_bits'] // 8
        mode = self.config['mode'].upper()
        key = self.config.get('key', 0x55)
        iv = self.config.get('iv', 0x00)

        padding_mode = self.config.get('padding', 'zero')
        pad_func, unpad_func = self.padding_functions[padding_mode]

        if operation == 'encode':
            data = pad_func(data, block_size_bytes)

        blocks = []
        for i in range(0, len(data), block_size_bytes):
            blocks.append(data[i:i + block_size_bytes])

        processor = self.mode_processors[mode](blocks, key, iv)

        if operation == 'encode':
            result_blocks = processor.encode(key)
        else:
            result_blocks = processor.decode(key)

        result_bytes = b''.join(result_blocks)

        if operation == 'decode':
            result_bytes = unpad_func(result_bytes)

        return result_bytes

    def encrypt_file(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = f.read()
        print(data.hex())
        encrypted_data = self.process_blocks(data, 'encode')
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)
        print(encrypted_data.hex())

    def decrypt_file(self, input_file, output_file):
        with open(input_file, 'rb') as f:
            data = f.read()
        decrypted_data = self.process_blocks(data, 'decode')
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        print(decrypted_data.hex())
