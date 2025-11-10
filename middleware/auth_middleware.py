from fastapi import Request, HTTPException
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from utils.auth_utils import SECRET_KEY, ALGORITHM
from database.database import get_db
from models.mahasiswa import Mahasiswa

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Endpoint yang tidak perlu login
        public_paths = ["/auth/login", "/auth/register", "/docs", "/openapi.json"]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        # Ambil token dari header Authorization
        authorization: str | None = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(status_code=401, content={"detail": "Token tidak ditemukan"})

        # Ambil token dari format "Bearer <token>"
        try:
            token = authorization.split(" ")[1]
        except IndexError:
            return JSONResponse(status_code=401, content={"detail": "Format Authorization header salah"})

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_email: str = payload.get("sub")
            if not user_email:
                raise HTTPException(status_code=401, detail="Token tidak valid")

            # Ambil user dari database
            db = next(get_db())
            user = db.query(Mahasiswa).filter(Mahasiswa.email == user_email).first()

            if not user:
                return JSONResponse(status_code=404, content={"detail": "User tidak ditemukan"})

            # Tambahkan user info ke request.state
            request.state.user_email = user.email
            request.state.user_id = user.id  # ⚡ ini penting buat transaksi
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Token tidak valid atau kadaluarsa"})

        # Lanjutkan ke route berikutnya
        return await call_next(request)
