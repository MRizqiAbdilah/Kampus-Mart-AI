from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from models.associations import mahasiswa_matakuliah


class Matakuliah(Base):
    __tablename__ = "matakuliah"

    id: Mapped[int] = mapped_column(primary_key=True)
    nama: Mapped[str] = mapped_column(String, nullable=False)
    sks: Mapped[int] = mapped_column(Integer, nullable=False, default=2)

    # Many-to-Many ke Mahasiswa
    mahasiswa: Mapped[list["Mahasiswa"]] = relationship(
        secondary=mahasiswa_matakuliah,
        back_populates="matakuliah",
        lazy="selectin"     # ⬅ WAJIB

    )
