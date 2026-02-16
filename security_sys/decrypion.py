import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


class Decryption():
    def __init__(self):
        self.pas = input("Enter private key password :").encode()
        with open('private_key.pem', 'rb') as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=self.pas
            )
    
    def decrypt_aes_key(self, encrypted_key):
        """
        Decrypt AES key using RSA-2048 with OAEP padding
        """
        aes_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return aes_key
    
    def decrypt_data(self, encrypted_data, aes_key):
        """
        Decrypt data using AES-256-GCM
        Format: nonce (12 bytes) + ciphertext + tag (16 bytes)
        """
        # Extract nonce (first 12 bytes)
        nonce = encrypted_data[:12]
        # Extract tag (last 16 bytes)
        tag = encrypted_data[-16:]
        # Ciphertext is in between
        ciphertext = encrypted_data[12:-16]
        
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag))
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        return decrypted_data.decode()
    
    def decrypt_payload(self, encrypted_payload, aes_key):
        """
        Decrypt entire payload and return as dictionary
        """
        json_str = self.decrypt_data(encrypted_payload, aes_key)
        return json.loads(json_str)

