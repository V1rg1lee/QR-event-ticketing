#!/usr/bin/env python

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os

CERTS_DIR = "certs"
CERT_FILE = os.path.join(CERTS_DIR, "cert.pem")
KEY_FILE = os.path.join(CERTS_DIR, "key.pem")

def generate_self_signed_cert():
    """Generate a self-signed certificate and private key."""
    if not os.path.exists(CERTS_DIR):
        os.makedirs(CERTS_DIR)

    # Generate a private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Informations about the certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "FR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Paris"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Paris"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Local Server"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    # Create a self-signed certificat
    cert = x509.CertificateBuilder() \
        .subject_name(subject) \
        .issuer_name(issuer) \
        .public_key(key.public_key()) \
        .serial_number(x509.random_serial_number()) \
        .not_valid_before(datetime.datetime.now()) \
        .not_valid_after(datetime.datetime.now() + datetime.timedelta(days=365)) \
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False
        ) \
        .sign(key, hashes.SHA256())

    # Save the private key
    with open(KEY_FILE, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save the certificate
    with open(CERT_FILE, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"✅ Certificate and private key generated in {CERTS_DIR}")

if __name__ == "__main__":
    generate_self_signed_cert()
