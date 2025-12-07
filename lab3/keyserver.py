import socket
import json
import threading
from datetime import datetime


class KeyServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.public_keys = {}
        self.server_socket = None
        self.running = False

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True

        print(f"[{datetime.now()}] KeyServer elindult: {self.host}:{self.port}")

        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client,args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
            except:
                break

    def handle_client(self, client_socket, client_address):
        try:
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                return

            request = json.loads(data)
            command = request.get('command')

            print(f"[{datetime.now()}] Kapott kérés: {command} from {client_address}")

            if command == 'register':
                response = self.register_key(request)
            elif command == 'get_key':
                response = self.get_key(request)
            else:
                response = {'status': 'error', 'message': 'Ismeretlen parancs'}

            client_socket.send(json.dumps(response).encode('utf-8'))
            print(f"[{datetime.now()}] Válasz küldve: {response['status']}")

        except json.JSONDecodeError:
            response = {'status': 'error', 'message': 'Érvénytelen JSON'}
            client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            print(f"[{datetime.now()}] Hiba: {e}")
        finally:
            client_socket.close()
            self.getAllKlientsAndKeys()


    def register_key(self, request):
        client_id = request.get('client_id')
        public_key = request.get('public_key')

        if not client_id or not public_key:
            return {'status': 'error', 'message': 'Hiányzó adatok'}

        self.public_keys[client_id] = public_key
        print(f"[{datetime.now()}] Kulcs regisztrálva: {client_id}")
        return {'status': 'success', 'message': f'Kulcs regisztrálva: {client_id}'}

    def get_key(self, request):
        client_id = request.get('client_id')

        if not client_id:
            return {'status': 'error', 'message': 'Hiányzó client_id'}

        if client_id in self.public_keys:
            print(f"[{datetime.now()}] Kulcs lekérve: {client_id}")
            return {'status': 'success', 'public_key': self.public_keys[client_id]}
        else:
            return {'status': 'error', 'message': f'Nem található kulcs: {client_id}'}

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print(f"[{datetime.now()}] KeyServer leállítva")

    def getAllKlientsAndKeys(self):
        print("======================================")
        for client_id, public_key in self.public_keys.items():
            print(f'{client_id}, {public_key[10:20]}')
        print("======================================")


if __name__ == "__main__":
    server = KeyServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()