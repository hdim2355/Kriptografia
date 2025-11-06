import os
from ECB import ECB

def create_random_binary_file(filename, size_in_mb=1):
    size_in_bytes = size_in_mb * 16
    random_data = os.urandom(size_in_bytes)
    with open(filename, 'wb') as file:
        file.write(random_data)

def read_file_to_bytes(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def process_block(data,block_size):
    blocks = []
    for i in range(0,len(data),block_size):
        blocks.append(data[i:i+block_size])
    return blocks


# create_random_binary_file('pelda.bin', 1)
data = read_file_to_bytes('pelda.bin')
print(f"Fájl mérete: {len(data)} bájt")
print(data)
print(data.hex())
print(process_block(data,8))

blocks = process_block(data,8)
ecb = ECB(blocks,8)
print(ecb.encode())