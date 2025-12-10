from sqlalchemy.sql.sqltypes import BigInteger
from datetime import date
from sqlalchemy import String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from utils.auth_utils import hash_password
from models.associations import mahasiswa_matakuliah


class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    id: Mapped[int] = mapped_column(primary_key=True)
    nama: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nim: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    semester: Mapped[int] = mapped_column(Integer, default=1)

    # FIELD BARU
    tahun_masuk: Mapped[int | None] = mapped_column(Integer, nullable=True)
    alamat: Mapped[str | None] = mapped_column(String, nullable=True)
    tanggal_lahir: Mapped[date | None] = mapped_column(Date, nullable=True)

    # RELASI KE KELAS
    kelas_id: Mapped[int | None] = mapped_column(ForeignKey("kelas.id"))
    kelas: Mapped["Kelas"] = relationship(
    back_populates="mahasiswa",
    lazy="selectin")  

    # RELASI MANY-TO-MANY
    matakuliah: Mapped[list["Matakuliah"]] = relationship(
        secondary=mahasiswa_matakuliah,
        back_populates="mahasiswa",
        lazy="selectin"     # ⬅ WAJIB

    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=lambda: hash_password("123456")
    )

    saldo: Mapped[float] = mapped_column(Float, default=0.0)
    
