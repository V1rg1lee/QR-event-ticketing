import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from sqlalchemy.orm import Session
from .db import SessionLocal


def get_db() -> Session:
    """
    Get a database session from the connection pool.

    Returns:
    Session: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_public_key() -> RSA.RsaKey:
    """
    Load the public key from the file `public_key.pem`.

    Returns:
    RSA.RsaKey: The public key.
    """
    with open("public_key.pem", "r") as f:
        return RSA.import_key(f.read())


def verify_signature(uuid: str, signature: str, public_key: RSA.RsaKey) -> bool:
    """
    Verify the signature of a UUID.

    Args:
    uuid (str): The UUID to verify.
    signature (str): The signature of the UUID.
    public_key (RSA.RsaKey): The public key to verify the signature.

    Returns:
    bool: True if the signature is valid, False otherwise.
    """
    try:
        decoded_signature = base64.b64decode(signature)
        h = SHA256.new(uuid.encode())
        pkcs1_15.new(public_key).verify(h, decoded_signature)
        return True
    except (ValueError, TypeError):
        return False
