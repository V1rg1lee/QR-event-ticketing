import base64
from typing import AsyncGenerator
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from sqlalchemy.ext.asyncio import AsyncSession
from .db import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get the database session.

    Yields:
    AsyncSession: The database session.
    """
    async with AsyncSessionLocal() as session:
        yield session


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
