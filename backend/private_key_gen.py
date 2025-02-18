from Crypto.PublicKey import RSA

def generate_rsa_keys():
    key = RSA.generate(2048)

    # Sauvegarde de la clé privée au format PKCS#1 (compatible Rust)
    with open("private_key.pem", "wb") as priv_file:
        priv_file.write(key.export_key(format="PEM", pkcs=1))

    # Sauvegarde de la clé publique pour la vérification en Flask
    with open("public_key.pem", "wb") as pub_file:
        pub_file.write(key.publickey().export_key(format="PEM"))

    print("✅ Clés RSA générées avec succès !")
    print("🔑 Clé privée : private_key.pem")
    print("🔓 Clé publique : public_key.pem")

# Exécute la génération des clés
generate_rsa_keys()
