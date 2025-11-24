from fastapi import Request, HTTPException
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from utils.auth_utils import SECRET_KEY, ALGORITHM
from database.database import get_db
from models.mahasiswa import Mahasiswa

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Endpoint yang tidak butuh login
        public_paths = [
            "/auth/login",
            "/auth/register",
            "/kelas",
            "/matakuliah",
            "/produk",
            "/docs",
            "/openapi.json"
        ]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        # Ambil header Authorization
        authorization: str | None = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(status_code=401, content={"detail": "Token tidak ditemukan"})

        # Format "Bearer <token>"
        try:
            token = authorization.split(" ")[1]
        except IndexError:
            return JSONResponse(status_code=401, content={"detail": "Format Authorization header salah"})

        # Decode token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")     # ⚡ SEKARANG AMBIL USER_ID, BUKAN EMAIL

            if not user_id:
                return JSONResponse(status_code=401, content={"detail": "Token tidak valid"})

            db = next(get_db())

            # Cari user berdasar ID (stabil, tidak berubah)
            user = db.query(Mahasiswa).filter(Mahasiswa.id == int(user_id)).first()

            if not user:
                return JSONResponse(status_code=404, content={"detail": "User tidak ditemukan"})

            # Simpan user ke request
            request.state.user_id = user.id
            request.state.user_email = user.email
            request.state.user = user

        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Token tidak valid atau kadaluarsa"})

        return await call_next(request)
