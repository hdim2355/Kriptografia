import time
import socket
from datetime import datetime
from client import Client


def main():
    print("=" * 70)
    print("Client 1 start (ID: 8001):")
    print("=" * 70)

    client1_ciphers = ['DES-CBC','CUSTOM-ECB']

    client1 = Client(client_id='8001',keyserver_host='localhost',keyserver_port=8000,client_name="Client_1",supported_ciphers=client1_ciphers,block_size_bits=128)

    client1.generateRSAKeyPair()

    client1.registerPubKey()

    time.sleep(3)

    client1.getPublicKey('8002')

    print(f"\n[{datetime.now()}] {client1.client_id}: Sender es receiver osztalyok inicializalasa")
    client1.initialize_communication_roles()

    client1.start_server('localhost', 8001)
    print(f"\n[{datetime.now()}] {client1.client_id}: Szerver elinditva")

    print(f"\n[{datetime.now()}] Varunk a masik kliens elindulasara")
    time.sleep(3)

    print(f"\n[{datetime.now()}] {client1.client_id}: Kezdemenyezi a kezfogast")
    client1.sendHello('8002', client1_ciphers)


    print(f"\n[{datetime.now()}] Komunikacio inditasa")

    messages = [
        "1. A kriptográfia alapvető fontosságú a modern digitális kommunikációban. Titkosított csatornák biztosítják az adatok biztonságos átvitelét hálózatokon keresztül. A szimmetrikus és aszimmetrikus titkosítási algoritmusok együttes használata lehetővé teszi a biztonságos kulcscserét és a gyors adattitkosítást. Minden résztvevőnek egyedi kulcspárral kell rendelkeznie, és közösen kell megegyezniük a használandó titkosító algoritmusban. Ez a rendszer biztosítja az adatok integritását és bizalmasságát.",
        "2. Köszönöm a valaszt Client2! A hibrid titkosítási rendszerek ötvözik az aszimmetrikus és szimmetrikus titkosítás előnyeit. Az RSA algoritmus biztosítja a biztonságos kulcscserét, míg az AES vagy más szimmetrikus algoritmusok gyors adattitkosítást tesznek lehetővé. A kulcsmenedzsment megfelelő megvalósítása kulcsfontosságú a rendszer biztonsága szempontjából. Minden kommunikációs félnek egyedi kulcspárral kell rendelkeznie, és közösen kell megegyezniük a használandó titkosító algoritmusban."
    ]

    try:
        for i in range(2):
            print(f"\n[{datetime.now()}] {i + 1}. Uzenet kuldese...")
            if client1.send_encrypted_message(messages[i]):
                print(f"[{datetime.now()}] {client1.client_id}: Uzenet sikeresen elkuldve!")
            else:
                print(f"[{datetime.now()}] Üzenet küldése sikertelen!")
                break

            print(f"\n[{datetime.now()}] {client1.client_id}: Varakozas {i + 1}. valaszra...")

            algorithm = client1._Client__receiver.selected_cipher.split("-")[0]
            try:
                client1.connected_peer.settimeout(15.0)
                response = client1._Client__receiver.receive_encrypted_message(client1.connected_peer,client1.crypter,algorithm)
                client1.connected_peer.settimeout(None)
                if response:
                    print(f"Válasz hossz: {len(response)} karakter")
                    print(f"Válasz: {response}")
                else:
                    print(f"[{datetime.now()}] Nem érkezett válasz vagy hiba történt")

            except socket.timeout:
                print(f"[{datetime.now()}] Timeout a válaszra várakozás közben")
                break
            except Exception as e:
                print(f"[{datetime.now()}] Hiba válaszfogadás közben: {e}")
                break

            time.sleep(1)
    except Exception as e:
        print(f"[{datetime.now()}] Hiba a kommunikációban: {e}")

    print(f"\n[{datetime.now()}] Komunikacio befejezese")
    client1.send_bye()
    print(f"\n[{datetime.now()}] Client1 befejezve")


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Client1 leállítása...")
        client1.stop()


if __name__ == "__main__":
    main()