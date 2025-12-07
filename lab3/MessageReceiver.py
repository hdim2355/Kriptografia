import os
import json
import base64
import socket
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


class MessageReceiver:
    def __init__(self, client_name, client_id, private_key, supported_ciphers):
        self.client_name = client_name
        self.client_id = client_id
        self.private_key = private_key
        self.supported_ciphers = supported_ciphers
        self.peer_public_key = None
        self.key1 = None
        self.key2 = None
        self.selected_cipher = None

    def set_peer_public_key(self, peer_public_key):
        self.peer_public_key = peer_public_key

    def receive_hello(self, sock):
        print(f"[{datetime.now()}] {self.client_name}: [Receiver] Hello varasa")

        success, hello_data = self.receive_and_decrypt_message(sock, 'hello')
        if not success:
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] Hello fogadása sikertelen")
            return None
        else:
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] Hello uzenet fogadva")

        sender_id = hello_data.get('sender_id')
        peer_ciphers = hello_data.get('ciphers', [])

        self.selected_cipher = None
        for cipher in peer_ciphers:
            if cipher in self.supported_ciphers:
                self.selected_cipher = cipher
                print(f"[{datetime.now()}] {self.client_name}: [Receiver] Kozos algoritmus kivalasztva: {cipher}")
                break

        if not self.selected_cipher:
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] HIBA: Nincs közös támogatott algoritmus!")

        return hello_data

    def generate_random_secret(self):
        self.key2 = os.urandom(32)
        return self.key2

    def receive_ack(self, sock):
        print(f"[{datetime.now()}] {self.client_name}: [Receiver] Ack varasa")

        success, ack_data = self.receive_and_decrypt_message(sock, 'ack')

        print(f"[{datetime.now()}] {self.client_name}: [Receiver] Ack kezfogas fogadva")
        if success and ack_data:
            selected_cipher = ack_data.get('selected_cipher')
            if selected_cipher:
                self.selected_cipher = selected_cipher
                print(f"[{datetime.now()}] {self.client_name}: [Receiver] Kozos algoritmus megallapitva: {selected_cipher}")

            return True, ack_data

        return False, None

    def receive_half_secret(self, sock):
        success, secret_data = self.receive_and_decrypt_message(sock, 'half_secret')
        if success and secret_data and secret_data.get('type') == 'half_secret':
            received_key = secret_data.get('secret')
            self.key1 = base64.b64decode(received_key)
            return True

        return False

    def receive_encrypted_message(self, sock, crypter, algorithm):
        try:
            message = self.receive_complete_message(sock)
            if not message:
                return None

            msg_type = message.get('type')

            if msg_type == 'encrypted_message':
                encrypted_b64 = message.get('data')
                if not encrypted_b64:
                    return None

                encrypted_bytes = base64.b64decode(encrypted_b64)

                decrypted_bytes = crypter.decrypt(encrypted_bytes, algorithm)
                return decrypted_bytes.decode('utf-8')

            return None
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] Fogadási hiba: {e}")
            return None

    def receive_and_decrypt_message(self, sock, expected_type):
        try:
            message = self.receive_complete_message(sock)
            if not message:
                return False, None

            if message.get('type') != f'encrypted_{expected_type}':
                return False, None

            encrypted_data = message.get('data')
            if not encrypted_data:
                return False, None

            decrypted_json = self.rsa_decrypt(encrypted_data)
            decrypted_data = json.loads(decrypted_json)

            return True, decrypted_data
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] RSA visszafejtési hiba: {e}")
            return False, None

    def rsa_decrypt(self, encrypted_b64):
        private_key = serialization.load_pem_private_key(self.private_key.encode('utf-8'),password=None,backend=default_backend())

        encrypted = base64.b64decode(encrypted_b64)

        decrypted = private_key.decrypt(encrypted,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

        return decrypted.decode('utf-8')

    def receive_complete_message(self, sock, timeout=None):
        try:
            if timeout:
                sock.settimeout(timeout)

            data = b''
            while True:
                chunk = sock.recv(1024)
                if not chunk:
                    return None
                data += chunk
                try:
                    if b'}' in data:
                        return json.loads(data.decode('utf-8'))
                except:
                    continue
            return None
        except socket.timeout:
            return None
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] Üzenetfogadási hiba: {e}")
            return None
        finally:
            if timeout:
                sock.settimeout(None)

    def receive_bye(self, sock, timeout=5):
        print(f"[{datetime.now()}] {self.client_name}: [Receiver] Bye várása")
        try:
            sock.settimeout(timeout)
            message = self.receive_complete_message(sock)
            sock.settimeout(None)

            if message and message.get('type') == 'bye':
                print(f"[{datetime.now()}] {self.client_name}: [Receiver] Bye fogadva")
                print(f"  Üzenet: {message.get('message', 'N/A')}")
                print(f"  Küldő: {message.get('sender_id', 'N/A')}")
                return True
            return False
        except socket.timeout:
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] Timeout Bye várakozás közben")
            return False
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] Hiba Bye fogadás közben: {e}")
            return False