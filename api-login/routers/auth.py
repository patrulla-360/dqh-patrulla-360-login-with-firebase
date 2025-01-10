from fastapi import APIRouter, HTTPException, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.firebase_model import verify_token
from models.db import get_db
import requests
from fastapi.responses import JSONResponse
from sqlalchemy import text
router = APIRouter()

FIREBASE_API_KEY = "AIzaSyDnSFWEJ1A58r6uieJFNfW-XX44ZPIZ10Y"

@router.post("/login")
async def login(data: dict, db: AsyncSession = Depends(get_db)):
    email = data.get("email")
    password = data.get("password")

    # Firebase Auth para verificar credenciales
    firebase_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    params = {"key": FIREBASE_API_KEY}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }

    response = requests.post(firebase_api_url, params=params, json=payload)
    if response.status_code != 200:
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        raise HTTPException(status_code=401, detail=error_message)

    # Obtener el JWT del usuario
    token = response.json().get("idToken")

    # Consultar información adicional en la base de datos
    query = text("""
        SELECT rol, background_color_prefered 
        FROM usr_p360.usuarios 
        WHERE correo_electronico = :email
    """)

    result = await db.execute(query, {"email": email})
    user_info = result.fetchone()

    if not user_info:
        raise HTTPException(status_code=404, detail="User not found in database")

    rol, background_color_prefered = user_info

    # Crear respuesta con cookies
    resp = JSONResponse(content={
        "message": "Login successful",
        "token": token,
        "rol": rol,
        "background_color_prefered": background_color_prefered
    })
    resp.set_cookie(key="jwt", value=token, httponly=True, secure=True, samesite="strict")
    resp.set_cookie(key="rol", value=rol, httponly=True, secure=True, samesite="strict")
    resp.set_cookie(key="background_color_prefered", value=background_color_prefered, httponly=True, secure=True, samesite="strict")
    return resp
