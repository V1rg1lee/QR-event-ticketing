from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import qrcode
import sqlite3
import uuid
import os

# Charger la clé privée RSA
def load_private_key():
    with open("private_key.pem", "r") as f:
        return RSA.import_key(f.read())

# Générer une signature pour un UUID
def sign_uuid(uuid_str, private_key):
    h = SHA256.new(uuid_str.encode())
    signature = pkcs1_15.new(private_key).sign(h)
    return base64.b64encode(signature).decode()  # Encodage en base64

# Générer un QR code et l'enregistrer en PNG
def generate_qr_code(content, file_path):
    qr = qrcode.make(content)
    qr.save(file_path)

# Générer les QR codes signés
def generate_qr_codes(db_path, output_folder, num_codes=2000):
    # Assurer l'existence du dossier de sortie
    os.makedirs(output_folder, exist_ok=True)

    # Charger la clé privée
    private_key = load_private_key()

    # Connexion à la base SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Création de la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qrcodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE,
            used INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    for i in range(1, num_codes + 1):
        # Générer un UUID
        unique_id = str(uuid.uuid4())

        # Signer l'UUID
        signature = sign_uuid(unique_id, private_key)

        # Contenu du QR Code
        qr_content = f"{unique_id}|{signature}"

        # Insérer dans la base de données
        cursor.execute("INSERT INTO qrcodes (uuid) VALUES (?)", (unique_id,))
        conn.commit()

        # Générer et sauvegarder le QR code
        file_path = os.path.join(output_folder, f"{i}.png")
        generate_qr_code(qr_content, file_path)

        print(f"✅ QR Code {i}/{num_codes} généré avec signature.")

    conn.close()
    print("🎉 Génération terminée !")

# Exécution de la génération
if __name__ == "__main__":  
    generate_qr_codes("qrcodes.db", "qrcodes", num_codes=2000)
