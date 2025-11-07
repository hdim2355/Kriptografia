import os
from ECB import ECB
from lab2.CBC import CBC
from CFB import CFB
from OFB import OFB
from CTR import CTR

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

print("ECB:")
blocks = process_block(data,8)
ecb = ECB(blocks,8)
print(blocks)
print(ecb.encode())
print(ecb.decode())

print("CBC:")
cbc = CBC(blocks,8,0x11)
print(blocks)
print(cbc.encode())
print(cbc.decode())

print("CFB:")
cbc = CFB(blocks,8,0x11)
print(blocks)
print(cbc.encode())
print(cbc.decode())

print("OFB:")
ofb = OFB(blocks,8,0x11)
print(blocks)
print(ofb.encode())
print(ofb.decode())

print("CTR:")
ctr = CTR(blocks,8,0x11)
print(blocks)
print(ctr.encode())
print(ctr.decode())