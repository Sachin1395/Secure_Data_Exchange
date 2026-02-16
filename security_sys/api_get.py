from main import Login
import requests
import json
import base64
from decrypion import Decryption

print("* * * Receiver Side * * *")

user = Login().login()

acsess_token = input("Enter access token for the api : ")
url = f"http://127.0.0.1:5000/{acsess_token}"
responce = requests.get(url)

# Check if request was successful
if responce.status_code != 200:
    print(f"Error: {responce.status_code} - {responce.json()}")
    exit()

# responce.json() already returns a dict
received_data = responce.json()

# Decode Base64 strings back into bytes
try:
    encrypted_payload = base64.b64decode(received_data["payload"].encode('utf-8'))
    encrypted_aes_key = base64.b64decode(received_data["aes"].encode('utf-8'))
except Exception as e:
    print(f"Error decoding Base64: {e}")
    exit()

# Initialize Decryption and decrypt AES key
dec = Decryption()
dec_key = dec.decrypt_aes_key(encrypted_aes_key)

print("\n✓ Successfully received encrypted data!")
print("✓ AES key decrypted using RSA-2048\n")

# Decrypt the entire payload
try:
    decrypted_payload = dec.decrypt_payload(encrypted_payload, dec_key)
    print("✓ Data decryption successful!\n")
    print("Decryption Details:")
    print(f"  - Method: AES-256-GCM")
    print(f"  - RSA Key: 2048-bit OAEP\n")
    print("=" * 50)
    print("DECRYPTED DATA:")
    print("=" * 50)
    for key, value in decrypted_payload.items():
        print(f"{key}: {value}")
    print("=" * 50)
except Exception as e:
    print(f"Error decrypting payload: {e}")
    exit()
    print(f"{keys} = {dec_data}")

