import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from sqlalchemy.orm import Session
from .db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_public_key() -> RSA.RsaKey:
    with open("public_key.pem", "r") as f:
        return RSA.import_key(f.read())


def verify_signature(uuid: str, signature: str, public_key: RSA.RsaKey) -> bool:
    try:
        decoded_signature = base64.b64decode(signature)
        h = SHA256.new(uuid.encode())
        pkcs1_15.new(public_key).verify(h, decoded_signature)
        return True
    except (ValueError, TypeError):
        return False
