from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
from .db import Base, QRCodes, engine
from .utils import get_db, load_public_key, verify_signature

app = FastAPI()
templates = Jinja2Templates(directory="static")

Base.metadata.create_all(bind=engine)


@app.post("/verify")
async def verify_qr_code(request: Request, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Verify the QR code and mark it as used if valid.

    Args:
    request (Request): The request object.
    db (Session): The database session.

    Returns:
    JSONResponse: The response object.
    """
    data = await request.json()
    qr_content = data.get("uuid", "").strip()

    if not qr_content:
        return JSONResponse({"error": "❌ QR code format incorrect"}, status_code=400)

    parts = qr_content.split("|")
    if len(parts) != 2:
        return JSONResponse({"error": "❌ QR code format incorrect"}, status_code=400)

    uuid, signature = parts
    public_key = load_public_key()

    if not verify_signature(uuid, signature, public_key):
        return JSONResponse({"error": "❌ QR code falsified"}, status_code=403)

    qr_code = db.query(QRCodes).filter_by(uuid=uuid).first()
    if not qr_code:
        return JSONResponse({"error": "❌ QR code unrecognized"}, status_code=404)

    if qr_code.used:
        return JSONResponse({"error": "❌ QR code already used"}, status_code=400)

    qr_code.used = True
    db.session.commit()
    return JSONResponse({"message": "✅ QR code valid"})


@app.get("/")
def serve_frontend(request: Request) -> HTMLResponse:
    """
    Serve the frontend.

    Args:
    request (Request): The request object.

    Returns:
    HTMLResponse: The response object.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/robots.txt")
def serve_robots() -> FileResponse:
    """
    Serve the robots.txt file.

    Returns:
    FileResponse: The response object.
    """
    return FileResponse("static/robots.txt")
