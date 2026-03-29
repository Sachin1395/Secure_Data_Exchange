import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding


class Encryption():
    def __init__(self):
        # Load existing private key
        with open('private_key.pem', 'rb') as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=b'sachin'
            )

        # Load existing public key
        with open('public_key.pem', 'rb') as f:
            self.public_key = serialization.load_pem_public_key(
                f.read()
            )

    def generate_aes_key(self):
        return os.urandom(32)  # 256-bit AES key

    def encrypt_data(self, data, aes_key):
        nonce = os.urandom(12)  # 12-byte nonce for GCM
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce))
        encryptor = cipher.encryptor()

        if isinstance(data, dict):
            plaintext = json.dumps(data).encode()
        elif isinstance(data, str):
            plaintext = data.encode()
        else:
            plaintext = data

        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        tag = encryptor.tag

        return nonce + ciphertext + tag

    def encrypt_payload(self, payload_dict, aes_key):
        json_str = json.dumps(payload_dict)
        return self.encrypt_data(json_str, aes_key)

    def encrypt_aes_key(self, aes_key):
        encrypted_key = self.public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_key

    def sign_payload(self, encrypted_payload):
        signature = self.private_key.sign(
            encrypted_payload,
            asym_padding.PSS(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                salt_length=asym_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature
