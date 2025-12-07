import os
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

class MessageSender:
    def __init__(self, client_name, client_id, private_key):
        self.client_name = client_name
        self.client_id = client_id
        self.private_key = private_key
        self.peer_public_key = None
        self.key1 = None

    def set_peer_public_key(self, peer_public_key):
        self.peer_public_key = peer_public_key

    def send_hello(self, sock, ciphers, block_size_bits):
        print(f"[{datetime.now()}] {self.client_name}: [Sender] Hello kuldese")

        hello_data = {
            'type': 'hello',
            'sender_id': self.client_id,
            'ciphers': ciphers,
            'block_size_bits': block_size_bits
        }

        return self.create_and_send_encrypted_message(sock, hello_data, 'hello')

    def generate_random_secret(self):
        self.key1 = os.urandom(32)
        return self.key1

    def send_half_secret(self, sock, secret_key):
        secret_to_send = {
            'type': 'half_secret',
            'sender_id': self.client_id,
            'secret': base64.b64encode(secret_key).decode('utf-8')
        }
        return self.create_and_send_encrypted_message(sock, secret_to_send, 'half_secret')

    def send_ack(self, sock, selected_cipher, supported_ciphers):

        ack_data = {
            'type': 'ack',
            'sender_id': self.client_id,
            'ciphers': supported_ciphers,
            'selected_cipher': selected_cipher
        }

        return self.create_and_send_encrypted_message(sock, ack_data, 'ack')

    def send_encrypted_message(self, sock, message, crypter, algorithm):
        try:
            print(f"[{datetime.now()}] {self.client_name}: [Sender] Titkosított üzenet küldése")

            encrypted_bytes = crypter.encrypt(message.encode('utf-8'), algorithm)
            encrypted_b64 = base64.b64encode(encrypted_bytes).decode('utf-8')

            msg_data = {
                'type': 'encrypted_message',
                'data': encrypted_b64
            }

            return self.send_json_message(sock, msg_data)
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: [Sender] Küldési hiba: {e}")
            return False

    def create_and_send_encrypted_message(self, sock, plain_data, message_type):
        if not self.peer_public_key:
            print(f"[{datetime.now()}] {self.client_name}: [Sender] Nincs peer publikus kulcs!")
            return False
        try:
            encrypted_data = self.rsa_encrypt(json.dumps(plain_data))
            message = { 'type': f'encrypted_{message_type}', 'data': encrypted_data}
            return self.send_json_message(sock, message)
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: [Sender] RSA titkosítási hiba: {e}")
            return False

    def rsa_encrypt(self, message):
        public_key = serialization.load_pem_public_key(self.peer_public_key.encode('utf-8'),backend=default_backend())
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        else:
            message_bytes = message

        encrypted = public_key.encrypt(message_bytes,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

        return base64.b64encode(encrypted).decode('utf-8')

    def send_json_message(self, sock, message_dict):
        try:
            message_json = json.dumps(message_dict)
            sock.send(message_json.encode('utf-8'))
            return True
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: [Sender] JSON küldési hiba: {e}")
            return False

    def send_bye(self, sock):
        print(f"[{datetime.now()}] {self.client_name}: [Sender] Bye küldése")

        bye_data = {
            'type': 'bye',
            'sender_id': self.client_id,
            'message': 'Kommunikacio vege'
        }

        return self.send_json_message(sock, bye_data)
