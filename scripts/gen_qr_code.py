#!/usr/bin/env python

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import qrcode
import sqlite3
import uuid
import os


def load_private_key() -> RSA.RsaKey:
    """
    Load the private key from the file `private_key.pem`.

    Returns:
    RSA.RsaKey: The private key.
    """
    with open("data/private_key.pem", "r") as f:
        return RSA.import_key(f.read())


def sign_uuid(uuid_str: str, private_key: RSA.RsaKey) -> str:
    """
    Sign a UUID with the private key.

    Args:
    uuid_str (str): The UUID to sign.
    private_key (RSA.RsaKey): The private key to sign the UUID.

    Returns:
    str: The signature of the UUID.
    """
    h = SHA256.new(uuid_str.encode())
    signature = pkcs1_15.new(private_key).sign(h)
    return base64.b64encode(signature).decode()  # Encodage en base64


def generate_qr_code(content: str, file_path: str) -> None:
    """
    Generate a QR code with the given content and save it to the file.

    Args:
    content (str): The content of the QR code.
    file_path (str): The file path to save the QR code.
    """
    qr = qrcode.make(content)
    qr.save(file_path)


def generate_qr_codes(db_path: str, output_folder: str, num_codes: int) -> None:
    """
    Generate QR codes with unique UUIDs and signatures and save them to the output folder.

    Args:
    db_path (str): The path to the SQLite database.
    output_folder (str): The folder to save the QR codes.
    num_codes (int): The number of QR codes to generate.
    """
    os.makedirs(output_folder, exist_ok=True)
    private_key = load_private_key()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qrcodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE,
            used INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    for i in range(1, num_codes + 1):
        unique_id = str(uuid.uuid4())
        signature = sign_uuid(unique_id, private_key)
        qr_content = f"{unique_id}|{signature}"

        cursor.execute("INSERT INTO qrcodes (uuid) VALUES (?)", (unique_id,))
        conn.commit()

        file_path = os.path.join(output_folder, f"{i}.png")
        generate_qr_code(qr_content, file_path)

        print(f"✅ QR Code {i}/{num_codes} generated")

    conn.close()
    print("🎉 All QR Codes generated")


if __name__ == "__main__":
    generate_qr_codes("data/qrcodes.db", "data/qrcodes", num_codes=2000)
