import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi  # ✅ Tambahkan ini
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

# ✅ Tambahkan skema security untuk Swagger UI
from database.base import Base
from database.database import engine
from middleware.auth_middleware import AuthMiddleware
from routes.auth_route import router as auth_router
from routes.mahasiswa_route import router as mahasiswa_router
from routes.produk_route import router as produk_router
from routes.qris_route import router as qris_router
from routes.saldo_route import router as saldo_router
from routes.transaksi_route import router as transaksi_router
from routes.user_route import router as user_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Kampus Mart",
    version="1.0.1",
    description="API documentation for Kampus Mart, Menjual aneka produk yang sangat-sangat enak dan bergizi banget",
)


security_scheme = HTTPBearer()

app.openapi_schema = None


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.add_middleware(AuthMiddleware)


# Setelah inisialisasi app
app.include_router(mahasiswa_router)
app.include_router(produk_router)
app.include_router(transaksi_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(qris_router)
app.include_router(saldo_router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Create database tables on startup
Base.metadata.create_all(bind=engine)


# ---- Cek koneksi database ----
@app.on_event("startup")
async def startup_event():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Database connected successfully.")
    except Exception as e:
        print(f"❌ Failed to connect to the database: {e}")
        raise SystemExit("Database connection failed — exiting app.")


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Store"}


if __name__ == "__main__":
    port = os.environ.get("PORT")
    if not port:
        raise EnvironmentError("PORT environment variable is not set")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
