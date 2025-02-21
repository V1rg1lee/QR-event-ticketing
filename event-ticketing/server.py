from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from .db import QRCodes, init_db
from .utils import get_db, load_public_key, verify_signature, create_access_token, is_authenticated

app = FastAPI()
templates = Jinja2Templates(directory="static")


@app.on_event("startup")
async def startup_event():
    """
    Initialize the database on startup.
    """
    await init_db()


@app.post("/verify")
async def verify_qr_code(request: Request, db: AsyncSession = Depends(get_db), is_auth: bool = Depends(is_authenticated)) -> JSONResponse:
    """
    Verify the QR code and mark it as used if valid.

    Args:
    request (Request): The request object.
    db (Session): The database session.
    is_auth (bool): Whether the user is authenticated.

    Returns:
    JSONResponse: The response object.
    """
    if not is_auth:
        return JSONResponse({"error": "❌ Unauthorized. Reload the page and log in."}, status_code=401)

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

    stmt = select(QRCodes).filter_by(uuid=uuid)
    result = await db.execute(stmt)
    qr_code = result.scalars().first()
    if not qr_code:
        return JSONResponse({"error": "❌ QR code unrecognized"}, status_code=404)

    if qr_code.used:
        return JSONResponse({"error": "❌ QR code already used"}, status_code=400)

    qr_code.used = True
    await db.commit()
    return JSONResponse({"message": "✅ QR code valid"})


@app.get("/")
def serve_frontend(request: Request, is_auth: bool = Depends(is_authenticated)) -> HTMLResponse:
    """
    Serve the frontend.

    Args:
    request (Request): The request object.
    is_auth (bool): Whether the user is authenticated.

    Returns:
    HTMLResponse: The response object.
    """
    if not is_auth:
        return templates.TemplateResponse("login.html", {"request": request, "api_login_url": request.url_for('login').replace(scheme="https")})
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
async def login(request: Request) -> JSONResponse:
    """
    Log in the user.

    Args:
    request (Request): The request object.

    Returns:
    JSONResponse: The response object.
    """
    data = await request.json()
    password = data.get("password", None)

    if password == os.getenv("PASSWORD"):
        token = create_access_token()
        response = JSONResponse({"message": "Login successful"})
        response.set_cookie("token", token, httponly=True, samesite="strict",
                            max_age=900, expires=900, secure=True, path="/")
        return response
    return JSONResponse({"error": "Login failed"}, status_code=401)


@app.get("/robots.txt")
def serve_robots() -> FileResponse:
    """
    Serve the robots.txt file.

    Returns:
    FileResponse: The response object.
    """
    return FileResponse("static/robots.txt")


@app.get("/favicon.png")
def serve_favicon() -> FileResponse:
    """
    Serve the favicon.png file.

    Returns:
    FileResponse: The response object.
    """
    return FileResponse("static/favicon.png")
