import sys
import os
import unittest
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'methods'))

try:
    from Crypter import Crypter
except ImportError as e:
    print(f"Import hiba: {e}")
    print("Elérhető fájlok a könyvtárban:")
    for file in os.listdir(current_dir):
        print(f"  - {file}")
    if os.path.exists(os.path.join(current_dir, 'methods')):
        print("Elérhető fájlok a methods mappában:")
        for file in os.listdir(os.path.join(current_dir, 'methods')):
            print(f"  - methods/{file}")
    if os.path.exists(os.path.join(current_dir, 'resources')):
        print("Elérhető fájlok a resources mappában:")
        for file in os.listdir(os.path.join(current_dir, 'resources')):
            print(f"  - resources/{file}")
    raise


class TestCrypter(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.resources_dir = os.path.join(self.current_dir, 'resources')
        self.test_file = 'binary_1mb.bin'
        self._create_test_file()

    def _create_test_file(self):
        if not os.path.exists(self.test_file):
            size_bytes = 1 * 1024 * 1024
            random_data = os.urandom(size_bytes)
            with open(self.test_file, 'wb') as f:
                f.write(random_data)

    def get_existing_config(self, mode):
        config_file_in_resources = os.path.join(self.resources_dir, f"config_{mode.lower()}.json")
        config_file_in_root = os.path.join(self.current_dir, f"config_{mode.lower()}.json")

        if os.path.exists(config_file_in_resources):
            return config_file_in_resources
        elif os.path.exists(config_file_in_root):
            return config_file_in_root
        else:
            raise FileNotFoundError(f"Konfigurációs fájl nem található: config_{mode.lower()}.json")

    def run_algorithm_test(self, mode, algorithm):
        config_file = self.get_existing_config(mode)
        crypter = Crypter(config_file)
        results = crypter.performance_test(self.test_file, [algorithm])
        return results[0]

    def test_ecb_custom(self):
        result = self.run_algorithm_test('ecb', 'CUSTOM')
        self.assertTrue(result['success'])

    def test_ecb_aes(self):
        result = self.run_algorithm_test('ecb', 'AES')
        self.assertTrue(result['success'])

    def test_cbc_custom(self):
        result = self.run_algorithm_test('cbc', 'CUSTOM')
        self.assertTrue(result['success'])

    def test_cbc_aes(self):
        result = self.run_algorithm_test('cbc', 'AES')
        self.assertTrue(result['success'])

    def test_cfb_custom(self):
        result = self.run_algorithm_test('cfb', 'CUSTOM')
        self.assertTrue(result['success'])

    def test_cfb_aes(self):
        result = self.run_algorithm_test('cfb', 'AES')
        self.assertTrue(result['success'])

    def test_ofb_custom(self):
        result = self.run_algorithm_test('ofb', 'CUSTOM')
        self.assertTrue(result['success'])

    def test_ofb_aes(self):
        result = self.run_algorithm_test('ofb', 'AES')
        self.assertTrue(result['success'])

    def test_ctr_custom(self):
        result = self.run_algorithm_test('ctr', 'CUSTOM')
        self.assertTrue(result['success'])

    def test_ctr_aes(self):
        result = self.run_algorithm_test('ctr', 'AES')
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()