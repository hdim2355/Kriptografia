import time
from datetime import datetime
from client import Client


def main():
    print("=" * 70)
    print("Client 2 start (ID: 8002)")
    print("=" * 70)

    client2_ciphers = ['DIS-CBC', 'XOR-CBC','CUSTOM-ECB']

    client2 = Client(client_id='8002',keyserver_host='localhost',keyserver_port=8000,client_name="Client_2",supported_ciphers=client2_ciphers)

    client2.generateRSAKeyPair()

    client2.registerPubKey()

    time.sleep(2)
    client2.getPublicKey('8001')

    print(f"\n[{datetime.now()}] {client2.client_id}: Sender es receiver osztalyok inicializalasa")
    client2.initialize_communication_roles()

    client2.start_server('localhost', 8002)
    print(f"\n[{datetime.now()}] {client2.client_id}: Szerver elinditva")

    print(f"\n[{datetime.now()}] Varunk a masik kliens elindulasara")

    print(f"\n[{datetime.now()}] {client2.client_id} Varom a kezfogast")

    time.sleep(10)

    # return
    responses = [
        "1. Köszönöm az üzenetedet Client1! A kriptográfia valóban alapvető fontosságú. A modern titkosítási algoritmusok biztosítják az adatok biztonságos átvitelét. A hibrid rendszerek ötvözik az aszimmetrikus titkosítás előnyeit a szimmetrikus titkosítás hatékonyságával. A kulcsmenedzsment megfelelő megvalósítása kulcsfontosságú a rendszer biztonsága szempontjából.",
        "2. Köszönöm az üzenetedet Client1! Igen, a hibrid titkosítási rendszerek valóban hatékonyak. Az RSA algoritmus biztosítja a biztonságos kulcscserét, míg az AES gyors adattitkosítást tesz lehetővé. Fontos továbbá, hogy a rendszer támogassa a kulcsrotációt és a kompromittált kulcsok gyors visszavonását. A kvantumrezisztens algoritmusok bevezetése is fontos lesz a jövőben."
    ]

    try:

        for i in range(2):
            print(f"\n[{datetime.now()}] Várakozás {i + 1}. üzenetre...")

            algorithm = client2._Client__receiver.selected_cipher.split("-")[0]

            message = client2._Client__receiver.receive_encrypted_message(client2.connected_peer,client2.crypter,algorithm)

            if message:
                print(f"Üzenet hossz: {len(message)} karakter")
                print(f"Üzenet: {message}")

                print(f"\n[{datetime.now()}] {client2.client_id}: {i + 1}. válasz küldése...")
                print(f"Válasz hossz: {len(responses[i])} karakter")
                if client2.send_encrypted_message(responses[i]):
                    print(f"[{datetime.now()}] Válasz sikeresen elküldve!")
                else:
                    print(f"[{datetime.now()}] Válasz küldése sikertelen!")
            else:
                print(f"[{datetime.now()}] Nem érkezett üzenet vagy hiba történt")
                break

            time.sleep(1)

    except Exception as e:
        print(f"[{datetime.now()}] Hiba a kommunikációban: {e}")

    bye_received = client2.wait_for_bye(timeout=10)
    print(f"\n[{datetime.now()}] Client2 befejezve")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Client2 leállítása...")
        client2.stop()


if __name__ == "__main__":
    main()