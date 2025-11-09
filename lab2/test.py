from Crypter import Crypter
import os
import json

def create_test_files():
    test_files = {
        'binary_1mb.bin': 1,
        'binary_5mb.bin': 5,
        'binary_10mb.bin': 10
    }

    for filename, size_mb in test_files.items():
        if not os.path.exists(filename):
            size_bytes = size_mb * 1024 * 1024
            random_data = os.urandom(size_bytes)
            with open(filename, 'wb') as f:
                f.write(random_data)


def load_config_from_file(mode):
    resources_path = os.path.join('resources', f'config_{mode.lower()}.json')
    root_path = f'config_{mode.lower()}.json'
    if os.path.exists(resources_path):
        config_file = resources_path
    elif os.path.exists(root_path):
        config_file = root_path
    else:
        raise FileNotFoundError(f"Hiba, nincs ilyen file: {mode}")
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config, config_file

def run_comprehensive_tests():

    create_test_files()

    algorithms = ['XOR', 'CUSTOM', 'AES']
    test_file = 'binary_1mb.bin'

    print("🚀 KRIPTOGRÁFIAI RENDSZER TESZTELÉSE")
    print("=" * 70)

    all_results = {}

    for mode in ['ECB', 'CBC', 'CFB', 'OFB', 'CTR']:
        config, config_file = load_config_from_file(mode)
        crypter = Crypter(config_file)
        all_results[mode] = (crypter.performance_test(test_file, algorithms))

    for mode, results in all_results.items():
        print(f"\n{mode} mód:")
        for result in results:
            print(f"  {result['algorithm']:8} - "
                  f"Enc: {result['encrypt_time']:6.4f}s - "
                  f"Dec: {result['decrypt_time']:6.4f}s - "
                  f"{'✅' if result['success'] else '❌'}")

if __name__ == "__main__":
    run_comprehensive_tests()
