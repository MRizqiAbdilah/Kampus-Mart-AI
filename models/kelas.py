from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


class Kelas(Base):
    __tablename__ = "kelas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nama: Mapped[str] = mapped_column(String, nullable=False)

    # One-to-Many → satu kelas banyak mahasiswa
    mahasiswa: Mapped[list["Mahasiswa"]] = relationship(
        back_populates="kelas",
        lazy="selectin"   # 🔥 agar list mahasiswa otomatis di-load
    )
