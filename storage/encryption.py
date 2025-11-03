"""Simple wrapper for symmetric encryption using Fernet."""

from cryptography.fernet import Fernet
import os

KEY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "secret.key"
)


def get_key():
    try:
        with open(KEY_PATH, "rb") as f:
            return f.read()
    except Exception:
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(KEY_PATH), exist_ok=True)
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        return key


def encrypt_bytes(data: bytes) -> bytes:
    f = Fernet(get_key())
    return f.encrypt(data)


def decrypt_bytes(token: bytes) -> bytes:
    f = Fernet(get_key())
    return f.decrypt(token)
