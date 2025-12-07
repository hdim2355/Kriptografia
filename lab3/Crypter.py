import json
import time
from lab2.methods.ECB import ECB
from lab2.methods.CBC import CBC
from lab2.methods.CFB import CFB
from lab2.methods.OFB import OFB
from lab2.methods.CTR import CTR
from Padding import Padding
from AES import AESCipher
from OwnAlg import CustomCipher


class Crypter(Padding):
    def __init__(self, config):
        super().__init__()
        self.config = config
        # self.config = self.load_config(file)
        self.__block_size_bytes = self.config['block_size_bits'] // 8
        self.__mode = self.config['mode'].upper()
        self.__key = self.config.get('key', 0x55)
        self.__iv = self.config.get('iv', 0x00)
        self.__padding_mode = self.config.get('padding', 'zero')
        self.mode_processors = self._init_mode_processors()
        self.algorithm_processors = self._init_algorithm_processors()
        self.padding_functions = self._init_padding_functions()

    def _init_algorithm_processors(self):
        return {
            'AES': self._setup_aes,
            'CUSTOM': self._setup_custom,
            'XOR': self._init_mode_processors()
        }

    def _setup_aes(self, blocks, block_size):
        return AESCipher(blocks, block_size)

    def _setup_custom(self, blocks, block_size):
        return CustomCipher(blocks, block_size)

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

    def _setup_ecb(self, blocks, key, iv, algorithm='XOR'):
        if algorithm == 'CUSTOM':
            return ECB(blocks, self.config['block_size_bits'],
                       encrypt_func=self._custom_encrypt,
                       decrypt_func=self._custom_decrypt)
        elif algorithm == 'AES':
            return ECB(blocks, self.config['block_size_bits'],
                       encrypt_func=self._aes_encrypt,
                       decrypt_func=self._aes_decrypt)
        else:
            return ECB(blocks, self.config['block_size_bits'])

    def _setup_cbc(self, blocks, key, iv, algorithm='XOR'):
        if algorithm == 'CUSTOM':
            return CBC(blocks, self.config['block_size_bits'], iv, encrypt_func=self._custom_encrypt,
                       decrypt_func=self._custom_decrypt)
        elif algorithm == 'AES':
            return CBC(blocks, self.config['block_size_bits'], iv,
                       encrypt_func=self._aes_encrypt,
                       decrypt_func=self._aes_decrypt)
        elif algorithm == 'XOR':
            return CBC(blocks, self.config['block_size_bits'], iv)

    def _setup_cfb(self, blocks, key, iv, algorithm='XOR'):
        if algorithm == 'CUSTOM':
            return CFB(blocks, self.config['block_size_bits'], iv, encrypt_func=self._custom_encrypt,
                       decrypt_func=self._custom_decrypt)
        elif algorithm == 'AES':
            return CFB(blocks, self.config['block_size_bits'], iv, encrypt_func=self._aes_encrypt,
                       decrypt_func=self._aes_decrypt)
        else:
            return CFB(blocks, self.config['block_size_bits'], iv)

    def _setup_ofb(self, blocks, key, iv, algorithm='XOR'):
        if algorithm == 'CUSTOM':
            return OFB(blocks, self.config['block_size_bits'], iv,
                       encrypt_func=self._custom_encrypt,
                       decrypt_func=self._custom_decrypt)
        elif algorithm == 'AES':
            return OFB(blocks, self.config['block_size_bits'], iv,
                       encrypt_func=self._aes_encrypt,
                       decrypt_func=self._aes_decrypt)
        else:
            return OFB(blocks, self.config['block_size_bits'], iv)

    def _setup_ctr(self, blocks, key, iv, algorithm='XOR'):
        if algorithm == 'CUSTOM':
            return CTR(blocks, self.config['block_size_bits'], iv,
                       encrypt_func=self._custom_encrypt,
                       decrypt_func=self._custom_decrypt)
        elif algorithm == 'AES':
            return CTR(blocks, self.config['block_size_bits'], iv,
                       encrypt_func=self._aes_encrypt,
                       decrypt_func=self._aes_decrypt)
        else:
            return CTR(blocks, self.config['block_size_bits'], iv)

    def _init_padding_functions(self):
        return {
            'zero': (self.zero_padding, self.zero_unpadding),
            'des': (self.des_padding, self.des_unpadding),
            'schneier': (self.schneier_padding, self.schneier_unpadding)
        }

    def process_blocks(self, data, operation, algorithm='XOR'):
        pad_func, unpad_func = self.padding_functions[self.__padding_mode]

        if operation == 'encode':
            data = pad_func(data, self.__block_size_bytes)

        blocks = []
        for i in range(0, len(data), self.__block_size_bytes):
            blocks.append(data[i:i + self.__block_size_bytes])

        processor_func = self.mode_processors[self.__mode]
        # print(f'mode:{self.__mode},algo{algorithm}')
        processor = processor_func(blocks, self.__key, self.__iv, algorithm)

        if operation == 'encode':
            result_blocks = processor.encode(self.__key)
        else:
            result_blocks = processor.decode(self.__key)

        result_bytes = b''.join(result_blocks)
        if operation == 'decode':
            result_bytes = unpad_func(result_bytes)
        return result_bytes

    def _custom_encrypt(self, data, key):
        result = bytearray()
        key_str = str(key)
        for i, byte in enumerate(data):
            key_char = ord(key_str[i % len(key_str)])
            encrypted = (byte + key_char) % 256
            result.append(encrypted)

        return bytes(result)

    def _custom_decrypt(self, data, key):
        result = bytearray()
        key_str = str(key)
        for i, byte in enumerate(data):
            key_char = ord(key_str[i % len(key_str)])
            decrypted = (byte - key_char) % 256
            result.append(decrypted)

        return bytes(result)

    def _aes_encrypt(self, data, key):
        aes_cipher = AESCipher([data], self.__block_size_bytes, self.__mode, self.__iv)
        encrypted_blocks = aes_cipher.encode(key)
        return encrypted_blocks[0] if encrypted_blocks else b''

    def _aes_decrypt(self, data, key):
        aes_cipher = AESCipher([data], self.__block_size_bytes, self.__mode, self.__iv)
        decrypted_blocks = aes_cipher.decode(key)
        return decrypted_blocks[0] if decrypted_blocks else b''

    def performance_test(self, input_file, algorithms=['XOR', 'CUSTOM', 'AES']):
        with open(input_file, 'rb') as f:
            original_data = f.read()

        file_size_mb = len(original_data) / (1024 * 1024)
        print(f"Tesztfájl mérete: {file_size_mb:.2f} MB")
        print("=" * 60)
        print(self.__mode)

        results = []

        for algorithm in algorithms:
            if algorithm == 'AES':
                self.__key = 'AES_secure_key_123'
            print(f"\n{algorithm} algoritmus tesztelése:")
            # if algorithm == 'AES':
            #     print(f'Eredeti:{original_data.hex()}')
            start_time = time.time()
            encrypted_data = self.process_blocks(original_data, 'encode', algorithm)
            encrypt_time = time.time() - start_time
            # if algorithm == 'AES':
            #     print(f'Kodolt:{encrypted_data.hex()}')
            start_time = time.time()
            decrypted_data = self.process_blocks(encrypted_data, 'decode', algorithm)
            decrypt_time = time.time() - start_time
            # if algorithm == 'AES':
            #     print(f'Forditott:{decrypted_data.hex()}')
            success = original_data == decrypted_data

            print(f"  Titkosítás ideje: {encrypt_time:.4f} másodperc")
            print(f"  Visszafejtés ideje: {decrypt_time:.4f} másodperc")
            print(f"  Sikeres: {'IGEN' if success else 'NEM'}")
            print(f"  Titkosított méret: {len(encrypted_data)} bájt")

            results.append({
                'algorithm': algorithm,
                'encrypt_time': encrypt_time,
                'decrypt_time': decrypt_time,
                'success': success,
                'encrypted_size': len(encrypted_data)
            })

        return results

    def encrypt(self, plaintext,algorithm):
        """Adatok titkosítása"""
        return self.process_blocks(plaintext, 'encode', algorithm)

    def decrypt(self, ciphertext,algorithm):
        """Adatok visszafejtése"""
        return self.process_blocks(ciphertext, 'decode', algorithm)
