from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.base import Base
from utils.auth_utils import hash_password
from models.associations import mahasiswa_matakuliah  # ← AMAN

class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    id = Column(Integer, primary_key=True)
    nama = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    nim = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    semester = Column(Integer, default=1)

    # 🔥 FIELD BARU
    tahun_masuk = Column(Integer, nullable=True)
    alamat = Column(String, nullable=True)
    tanggal_lahir = Column(Date, nullable=True)

    kelas_id = Column(Integer, ForeignKey("kelas.id"))
    kelas = relationship("Kelas", back_populates="mahasiswa")

    matakuliah = relationship(
        "Matakuliah",
        secondary=mahasiswa_matakuliah,
        back_populates="mahasiswa"
    )

    password_hash = Column(String, nullable=False, default=lambda: hash_password("123456"))
    saldo = Column(Float, default=0.0)
