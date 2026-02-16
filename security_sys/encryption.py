import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class Encryption():
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        with open('private_key.pem', 'rb') as f:
            pk = serialization.load_pem_private_key(
                f.read(),
                password=b'sachin'
            )
        self.public_key = pk.public_key()
        private_pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(b'sachin')
        )
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open('public_key.pem', 'wb') as f:
            f.write(public_pem)
        with open('private_key.pem', 'wb') as f:
            f.write(private_pem)

    def generate_aes_key(self):
        return os.urandom(32)  # Generate a 256-bit key for AES-256

    def encrypt_data(self, data, aes_key):
        """
        Encrypt data using AES-256-GCM
        Format: nonce (12 bytes) + ciphertext + tag (16 bytes)
        """
        nonce = os.urandom(12)  # 12-byte nonce for GCM
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce))
        encryptor = cipher.encryptor()
        
        # Convert data to JSON string if it's a dict
        if isinstance(data, dict):
            plaintext = json.dumps(data).encode()
        else:
            plaintext = data.encode() if isinstance(data, str) else data
        
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        tag = encryptor.tag
        
        # Return: nonce + ciphertext + tag
        return nonce + ciphertext + tag

    def encrypt_payload(self, payload_dict, aes_key):
        """
        Encrypt entire payload dictionary as JSON string
        """
        json_str = json.dumps(payload_dict)
        return self.encrypt_data(json_str, aes_key)

    def encrypt_aes_key(self, aes_key):
        """
        Encrypt AES key using RSA-2048 with OAEP padding
        """
        encrypted_key = self.public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_key















