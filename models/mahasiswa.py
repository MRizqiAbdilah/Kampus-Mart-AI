from sqlalchemy import Column, Float, Integer, String

from database.base import Base


class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    nim = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    jurusan = Column(String)
    saldo = Column(Float, default=0.0)  # ✅ Tambahan kolom saldo
