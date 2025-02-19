from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
import os

db_path = os.path.abspath("qrcodes.db")
app = Flask(__name__, static_folder="../static")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class QRCodes(db.Model):
    __tablename__ = "qrcodes"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

def load_public_key():
    with open("public_key.pem", "r") as f:
        return RSA.import_key(f.read())

def verify_signature(uuid, signature, public_key):
    try:
        decoded_signature = base64.b64decode(signature)
        h = SHA256.new(uuid.encode())
        pkcs1_15.new(public_key).verify(h, decoded_signature)
        return True
    except (ValueError, TypeError) as e:
        print("❌ Signature invalide")
        print(f"Error: {e}")
        return False

@app.route("/verify", methods=["POST"])
def verify_qr_code():
    data = request.json
    qr_content = data.get("uuid", "").strip()

    if not qr_content:
        return "❌ QR Code invalide", 400

    parts = qr_content.split("|")
    if len(parts) != 2:
        return "❌ Format QR Code incorrect", 400

    uuid, signature = parts
    public_key = load_public_key()

    print(f"Vérification du QR Code {uuid} avec signature {signature}")
    print(f"Clé publique : {public_key.export_key().decode()}")
    if not verify_signature(uuid, signature, public_key):
        return "❌ QR Code falsifié", 403

    qr_code = QRCodes.query.filter_by(uuid=uuid).first()
    if not qr_code:
        return "❌ QR Code non reconnu", 404

    if qr_code.used:
        return "❌ QR Code déjà utilisé", 400

    qr_code.used = True
    db.session.commit()
    return "✅ QR Code valide, accès autorisé", 200

@app.route("/")
def serve_frontend():
    print(app.static_folder)
    return send_from_directory(app.static_folder, "index.html")
