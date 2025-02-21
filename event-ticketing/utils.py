import base64
from typing import AsyncGenerator, Optional
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from fastapi import Depends, Request
from jwt.exceptions import PyJWTError
from typing import Annotated
from datetime import datetime, timedelta, timezone
import jwt
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
    with open("data/public_key.pem", "r") as f:
        return RSA.import_key(f.read())


def load_private_key() -> RSA.RsaKey:
    """
    Load the private key from the file `private_key.pem`.

    Returns:
    RSA.RsaKey: The private key.
    """
    with open("data/private_key.pem", "r") as f:
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


def create_access_token() -> str:
    """
    Create an access token, as a JWT, that expires in 15 minutes.

    Returns:
    str: The access token.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"exp": expire}
    encoded_jwt = jwt.encode(
        to_encode, load_private_key().export_key(), algorithm="RS256")
    return encoded_jwt


async def get_token_from_header(request: Request) -> Optional[str]:
    """
    Retrieve the token from the request header.

    Args:
    request (Request): The request object.

    Returns:
    Optional[str]: The token if present, None otherwise.
    """
    auth: Optional[str] = request.headers.get("Cookie")
    if not auth:
        return
    parts = auth.split('=')
    if parts[0].lower() != "token" or len(parts) != 2:
        return
    return parts[1]


def is_authenticated(token: Annotated[Optional[str], Depends(get_token_from_header)]) -> bool:
    """
    Check if the user is authenticated.

    Args:
    token (Annotated[Optional[str], Depends(get_token_from_header)]): The token to check.

    Returns:
    bool: True if the user is authenticated, False otherwise.
    """
    if not token:
        return False
    try:
        jwt.decode(token, load_public_key().export_key(), algorithms=["RS256"])
    except PyJWTError:
        return False
    return True
