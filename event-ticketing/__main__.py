import uvicorn
import argparse
from .server import app

parser = argparse.ArgumentParser(description="Launch the server")
parser.add_argument('--ssl', action='store_true', help="Enable SSL config")
args = parser.parse_args()

ssl_config = {}
if args.ssl:
    ssl_config = {
        'ssl_certfile': "certs/cert.pem",
        'ssl_keyfile': "certs/key.pem"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, **ssl_config)
