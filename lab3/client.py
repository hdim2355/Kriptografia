import hashlib
import socket
import json
import base64
import threading
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime
from Crypter import Crypter
from MessageSender import MessageSender
from MessageReceiver import MessageReceiver


class Client:
    def __init__(self, client_id='8001', keyserver_host='localhost', keyserver_port=8000,client_name='Client', supported_ciphers=None, block_size_bits= None):
        self.client_id = client_id
        self.keyserver_host = keyserver_host
        self.keyserver_port = keyserver_port
        self.client_name = client_name
        self.supported_ciphers = supported_ciphers

        self.private_key = None
        self.public_key = None
        self.peer_public_key = None
        self.common_key = None
        self.crypter = None

        self.server_socket = None
        self.running = False
        self.connected_peer = None

        self.__sender = None
        self.__receiver = None

        self.__block_size_bits = block_size_bits

        print(f"[{datetime.now()}] {self.client_name} tamogatott titkositok: {self.supported_ciphers}")


    def initialize_communication_roles(self):
        self.__sender = MessageSender(client_name=self.client_name,client_id=self.client_id,private_key=self.private_key)
        self.__receiver = MessageReceiver(client_name=self.client_name,client_id=self.client_id,private_key=self.private_key,supported_ciphers=self.supported_ciphers)

        if self.peer_public_key:
            self.__sender.set_peer_public_key(self.peer_public_key)
            self.__receiver.set_peer_public_key(self.peer_public_key)


    def generateRSAKeyPair(self):
        print(f"[{datetime.now()}] {self.client_name}: RSA kulcspar generalasa")

        private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())
        public_key = private_key.public_key()

        self.private_key = private_key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption()).decode('utf-8')

        self.public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')

        print(f"[{datetime.now()}] {self.client_name}: RSA kulcspar generalva")
        return self.private_key, self.public_key

    def registerPubKey(self):
        request = { 'command': 'register', 'client_id': self.client_id,'public_key': self.public_key }
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.keyserver_host, self.keyserver_port))
                success = self._send_json_message(sock, request)
                if not success:
                    return False
                response = self._receive_complete_message(sock)
                if response and response.get('status') == 'success':
                    print(f"[{datetime.now()}] {self.client_name}: Sikeres regisztracio a KeyServer-nel")
                    return True
                else:
                    print(f"[{datetime.now()}] {self.client_name}: Regisztráció sikertelen")
                    return False
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: Hiba a regisztracioban: {e}")
            return False

    def getPublicKey(self, peer_id):
        request = { 'command': 'get_key', 'client_id': peer_id }
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.keyserver_host, self.keyserver_port))
                success = self._send_json_message(sock, request)
                if not success:
                    return None

                response = self._receive_complete_message(sock)

                if response and response.get('status') == 'success':
                    peer_key = response.get('public_key')
                    self.peer_public_key = peer_key

                    if self.__sender:
                        self.__sender.set_peer_public_key(peer_key)
                    if self.__receiver:
                        self.__receiver.set_peer_public_key(peer_key)

                    print(f"[{datetime.now()}] {self.client_name}: Peer kulcs lekérve: {peer_id}")
                    return peer_key
                else:
                    print(f"[{datetime.now()}] {self.client_name}: Kulcs lekérés sikertelen")
                    return None
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: Hiba a kulcs lekérése során: {e}")
            return None

    def sendHello(self, peer_id, ciphers):
        peer_port = int(peer_id)
        return self._send_hello('localhost', peer_port, ciphers)

    def _send_hello(self, peer_host, peer_port, ciphers):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer_host, peer_port))

            if not self.__sender.send_hello(sock, ciphers, self.__block_size_bits):
                print(f"[{datetime.now()}] {self.client_name}: Hello küldése sikertelen")
                sock.close()
                return False
            else:
                print(f"[{datetime.now()}] {self.client_name}: [Sender] Hello kezfogas elkuldve")

            success, ack_data = self.__receiver.receive_ack(sock)

            if not success:
                print(f"[{datetime.now()}] {self.client_name}: Ack fogadása sikertelen")
                sock.close()
                return False

            secret_key = self.__sender.generate_random_secret()
            print(f"[{datetime.now()}] {self.client_name}: [Sender] HalfSecret generalva")

            if not self.__sender.send_half_secret(sock, secret_key):
                print(f"[{datetime.now()}] {self.client_name}: Titok küldése sikertelen")
                sock.close()
                return False
            else:
                print(f"[{datetime.now()}] {self.client_name}: [Sender] HalfSecret elkuldve")

            if not self.__receiver.receive_half_secret(sock):
                print(f"[{datetime.now()}] {self.client_name}: Peer titok fogadása sikertelen")
                sock.close()
                return False
            else:
                print(f"[{datetime.now()}] {self.client_name}: [Receiver] HalfSecret fogadasa")

            if self.__sender.key1 and self.__receiver.key1:
                self.common_key = self.generateCommonSecret(self.__sender.key1, self.__receiver.key1)

                if not self.init_block_cipher():
                    print(f"[{datetime.now()}] {self.client_name}: Titkosítás inicializálása sikertelen")
                    sock.close()
                    return False

                self.connected_peer = sock

                return True

            return False

        except Exception as e:
            print(f"\n[{datetime.now()}] {self.client_name}: Hiba kulcscsere közben: {e}")
            import traceback
            traceback.print_exc()
            return False

    def handle_peer_connection(self, sock, address):
        try:
            print(f"\n[{datetime.now()}] {self.client_name}: Elfogadja a kezfogast")

            hello_data = self.__receiver.receive_hello(sock)
            if not hello_data:
                print(f"[{datetime.now()}] {self.client_name}: Hello üzenet fogadása sikertelen")
                sock.close()
                return
            self.__block_size_bits = hello_data.get('block_size_bits', 128)

            if not self.__sender.send_ack(sock, self.__receiver.selected_cipher,self.supported_ciphers):
                print(f"[{datetime.now()}] {self.client_name}: Ack küldése sikertelen")
                sock.close()
                return
            else:
                print(f"[{datetime.now()}] {self.client_name}: [Sender] Ack elkuldve")

            secret_key = self.__receiver.generate_random_secret()
            print(f"[{datetime.now()}] {self.client_name}: [Receiver] HalfSecret generalva")

            if not self.__receiver.receive_half_secret(sock):
                print(f"[{datetime.now()}] {self.client_name}: HalfSecret fogadása sikertelen")
                sock.close()
                return
            else:
                print(f"[{datetime.now()}] {self.client_name}: [Receiver] HalfSecret fogadva")


            if not self.__sender.send_half_secret(sock, secret_key):
                print(f"[{datetime.now()}] {self.client_name}: Titok küldése sikertelen")
                sock.close()
                return
            else:
                print(f"[{datetime.now()}] {self.client_name}: [Sender] HalfSecret elkuldve")

            if self.__receiver.key1 and self.__receiver.key2:
                self.common_key = self.generateCommonSecret(self.__receiver.key1, self.__receiver.key2)

                if not self.init_block_cipher():
                    print(f"[{datetime.now()}] {self.client_name}: Titkosítás inicializálása sikertelen")
                    sock.close()
                    return
                self.connected_peer = sock

            else:
                print(f"[{datetime.now()}] {self.client_name}: Közös kulcs generálása sikertelen")
                sock.close()

        except Exception as e:
            print(f"\n[{datetime.now()}] {self.client_name}: Hiba kulcscsere közben: {e}")
            import traceback
            traceback.print_exc()
            sock.close()

    def init_block_cipher(self):
        algorithm_parts = self.__receiver.selected_cipher.split("-")
        algorithm, mode = algorithm_parts

        config = {
            "algorithm": algorithm,
            "block_size_bits": self.__block_size_bits,
            "mode": mode,
            "key": base64.b64encode(self.common_key).decode('utf-8'),
            "iv": 42,
            "padding": "zero"
        }

        try:
            self.crypter = Crypter(config)
            print(f"[{datetime.now()}] {self.client_name}: Titkositas inicializalva. Algoritmus: {algorithm}-{mode}")
            return True
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: Crypter inicializálási hiba: {e}")
            return False

    def send_encrypted_message(self, message):
        if not self.crypter or not self.connected_peer:
            print(f"[{datetime.now()}] {self.client_name}: Nincs titkosítás inicializálva vagy nincs kapcsolat!")
            return False

        algorithm = self.__receiver.selected_cipher.split("-")[0]
        print(f"[{datetime.now()}] {self.client_name}: Uzenet kuldese ({len(message)} karakter)")
        print(f'Uzenet:{message}')
        return self.__sender.send_encrypted_message(self.connected_peer, message, self.crypter, algorithm)

    def start_server(self, host='localhost', port=None):
        if port is None:
            port = int(self.client_id)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.running = True

        print(f"[{datetime.now()}] {self.client_name}: Szerver elinditva: {host}:{port}")

        server_thread = threading.Thread(target=self.accept_connections)
        server_thread.daemon = True
        server_thread.start()

        return port

    def accept_connections(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"[{datetime.now()}] {self.client_name}: Kapcsolat fogadva: {client_address}")

                handler_thread = threading.Thread(target=self.handle_peer_connection,args=(client_socket, client_address))
                handler_thread.daemon = True
                handler_thread.start()
            except:
                break

    def generateCommonSecret(self, key1, key2):
        min_len = min(len(key1), len(key2))
        combined = bytearray()
        for i in range(min_len):
            combined.append(key1[i] ^ key2[i])
        self.common_key = hashlib.sha256(bytes(combined)).digest()

        print(f"Kozos kulcs generalva: {self.common_key.hex()}")

        return self.common_key

    def _send_json_message(self, sock, message_dict):
        try:
            message_json = json.dumps(message_dict)
            sock.send(message_json.encode('utf-8'))
            return True
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: JSON küldési hiba: {e}")
            return False

    def _receive_complete_message(self, sock):
        try:
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
        except Exception as e:
            print(f"[{datetime.now()}] {self.client_name}: Üzenetfogadási hiba: {e}")
            return None

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.connected_peer:
            self.connected_peer.close()
        print(f"[{datetime.now()}] {self.client_name}: Leállítva")

    def send_bye(self):
        if not self.connected_peer:
            print(f"[{datetime.now()}] {self.client_name}: Nincs kapcsolat a peer-rel")
            return False

        print(f"\n[{datetime.now()}] {self.client_name}: kominukacio befejezese")

        success = self.__sender.send_bye(self.connected_peer)
        if success:
            print(f"[{datetime.now()}] {self.client_name}: Bye uzenet elkuldve")
        else:
            print(f"[{datetime.now()}] {self.client_name}: Bye küldése sikertelen")

        if self.connected_peer:
            self.connected_peer.close()
            self.connected_peer = None

        return success

    def wait_for_bye(self, timeout=10):
        if not self.connected_peer:
            print(f"[{datetime.now()}] {self.client_name}: Nincs kapcsolat a peer-rel")
            return False

        print(f"\n[{datetime.now()}] {self.client_name}: Bye varasa")

        bye_received = self.__receiver.receive_bye(self.connected_peer, timeout)

        if bye_received:
            print(f"[{datetime.now()}] {self.client_name}: Kapcsolat bucsuzott")
        else:
            print(f"[{datetime.now()}] {self.client_name}: Nem erkezett Bye uzenet")

        if self.connected_peer:
            self.connected_peer.close()
            self.connected_peer = None

        return bye_received
