import json
import base64
import requests
import random
import string

from main import Login
from encryption import Encryption

def main():
    print("* * * SENDER SIDE * * *\n")

    user = Login().login()

    data = {
        "Household ID": "",
        "Timestamp": "",
        "Energy Consumption": "",
        "Peak Demand": "",
        "Substation ID": "",
    }

    if user:
        en = Encryption()
        aes = en.generate_aes_key()
        print("Enter the relevant data :\n")

        # Collect all data from user
        for key in data:
            data[key] = input(f"enter {key} : ")

        # Encrypt entire payload as JSON
        encrypted_payload = en.encrypt_payload(data, aes)
        encrypted_aes_key = en.encrypt_aes_key(aes)

        # Generate random access token
        access_token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        # New structure: {"payload": encrypted_bytes, "aes": encrypted_aes_key}
        transmission_data = {
            "payload": base64.b64encode(encrypted_payload).decode('utf-8'),
            "aes": base64.b64encode(encrypted_aes_key).decode('utf-8')
        }

        # Upload to server
        try:
            response = requests.post(f"http://127.0.0.1:5000/upload/{access_token}", json=transmission_data)
            if response.status_code == 200:
                print("\n✓ Data is successfully encrypted and posted to the server.\n")
                print(f"Access Token: {access_token}")
                print(f"API URL: http://127.0.0.1:5000/{access_token}\n")
                print("Encryption Details:")
                print(f"  - Method: AES-256-GCM")
                print(f"  - Nonce: 12 bytes")
                print(f"  - Tag: 16 bytes")
                print(f"  - RSA Key: 2048-bit OAEP\n")
            else:
                try:
                    err = response.json()
                except Exception:
                    err = response.text
                print(f"Error uploading data: {response.status_code} - {err}\n")
        except requests.exceptions.RequestException as e:
            print("Error: Cannot connect to Flask server at http://127.0.0.1:5000/")
            print("Please make sure the server.py is running!\n")
            print(f"Details: {e}")
    else:
        print("Login failed!")

if __name__ == "__main__":
    main()