from .server import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000,
                ssl_certfile="certs/cert.pem", ssl_keyfile="certs/key.pem")
