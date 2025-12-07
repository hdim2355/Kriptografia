from Crypto.Cipher import AES

class AESCipher:
    def __init__(self, blocks, block_size, mode, iv=None):
        self.__blocks = blocks
        self.__block_size = block_size
        self.__mode = mode
        self.__iv = iv

    def encode(self, key):
        if isinstance(key, int):
            key_bytes = key.to_bytes(16, byteorder='big')
        else:
            key_str = str(key)
            key_bytes = key_str.encode('utf-8').ljust(16, b'\0')[:16]

        iv_bytes = self._prepare_iv()

        if self.__mode == 'ECB':
            cipher = AES.new(key_bytes, AES.MODE_ECB)
        elif self.__mode == 'CBC':
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
        elif self.__mode == 'CFB':
            cipher = AES.new(key_bytes, AES.MODE_CFB, iv=iv_bytes)
        elif self.__mode == 'OFB':
            cipher = AES.new(key_bytes, AES.MODE_OFB, iv=iv_bytes)
        else:
            cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=iv_bytes[:8])

        full_data = b''.join(self.__blocks)

        if len(full_data) % 16 != 0:
            full_data = full_data.ljust(len(full_data) + (16 - len(full_data) % 16), b'\0')

        encrypted_data = cipher.encrypt(full_data)

        return [encrypted_data[i:i + self.__block_size] for i in range(0, len(encrypted_data), self.__block_size)]

    def decode(self, key):
        if isinstance(key, int):
            key_bytes = key.to_bytes(16, byteorder='big')
        else:
            key_str = str(key)
            key_bytes = key_str.encode('utf-8').ljust(16, b'\0')[:16]

        iv_bytes = self._prepare_iv()

        if self.__mode == 'ECB':
            cipher = AES.new(key_bytes, AES.MODE_ECB)
        elif self.__mode == 'CBC':
            cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
        elif self.__mode == 'CFB':
            cipher = AES.new(key_bytes, AES.MODE_CFB, iv=iv_bytes)
        elif self.__mode == 'OFB':
            cipher = AES.new(key_bytes, AES.MODE_OFB, iv=iv_bytes)
        else:
            cipher = AES.new(key_bytes, AES.MODE_CTR, nonce=iv_bytes[:8])

        full_data = b''.join(self.__blocks)
        decrypted_data = cipher.decrypt(full_data)

        return [decrypted_data[i:i + self.__block_size] for i in range(0, len(decrypted_data), self.__block_size)]

    def _prepare_iv(self):
        if self.__iv is None:
            return b'\0' * 16
        if isinstance(self.__iv, int):
            return self.__iv.to_bytes(16, byteorder='big')
        if isinstance(self.__iv, bytes):
            return self.__iv.ljust(16, b'\0')[:16]
        return str(self.__iv).encode('utf-8').ljust(16, b'\0')[:16]