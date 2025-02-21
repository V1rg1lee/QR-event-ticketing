#!/usr/bin/env python

from Crypto.PublicKey import RSA


def generate_rsa_keys() -> None:
    """
    Generate RSA keys and save them to the files `private_key.pem` and `public_key.pem`.
    """
    key = RSA.generate(2048)

    # Save the private key to a file in PKCS#1 format
    with open("data/private_key.pem", "wb") as priv_file:
        priv_file.write(key.export_key(format="PEM", pkcs=1))

    # Save the public key to a file in PKCS#1 format
    with open("data/public_key.pem", "wb") as pub_file:
        pub_file.write(key.publickey().export_key(format="PEM"))

    print("✅ RSA keys generated successfully.")
    print("🔑 Private key: private_key.pem")
    print("🔓 Public key: public_key.pem")


if __name__ == "__main__":
    generate_rsa_keys()
