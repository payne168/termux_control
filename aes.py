from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from base64 import b64decode, b64encode

backend = default_backend()
padder = padding.PKCS7(128).padder()
unpadder = padding.PKCS7(128).unpadder()


def encrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    data = data.encode('utf-8')
    data = padder.update(data) + padder.finalize()
    cipher = encryptor.update(data) + encryptor.finalize()
    return b64encode(cipher).decode('utf-8')


def decrypt(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    data = b64decode(data)
    plain = decryptor.update(data) + decryptor.finalize()
    plain = unpadder.update(plain) + unpadder.finalize()
    return plain.decode('utf-8')


if __name__ == '__main__':
    data = 'test'
    key = iv = b'1234567887654321'
    data = encrypt(data, key, iv)
    print(data)
    print(decrypt(data, key, iv))
