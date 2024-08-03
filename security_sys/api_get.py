from main import Login
import requests
import json
import base64
from decrypion import Decryption

print("* * * Receiver Side * * * ")

user =Login().login()

acsess_token = input("Enter access token for the api : ")
url=f"http://127.0.0.1:5000/{acsess_token}"
responce = requests.get(url)
"""print(responce.status_code)
print(responce.json())"""

data=responce.json()
json_dict = json.loads(data)

# Decode Base64 strings back into bytes
decoded_dict = {key: base64.b64decode(value.encode('utf-8')) for key, value in json_dict.items()}

'''# Print the decoded dictionary
for key, value in decoded_dict.items():
    print(f"{key}: {value}")'''

dec=Decryption()
dec_key = dec.decrypt_aes_key(decoded_dict["aes"])
del decoded_dict["aes"]
print("\n")
print("Successfully received Data!\n")
print("Data decryption successful!\n")
for keys in decoded_dict:
    dec_data = dec.decrypt_data(decoded_dict[keys], dec_key)
    print(f"{keys} = {dec_data}")

