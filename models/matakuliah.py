from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base
from models.associations import mahasiswa_matakuliah

class Matakuliah(Base):
    __tablename__ = "matakuliah"

    id = Column(Integer, primary_key=True)
    nama = Column(String, nullable=False)
    sks = Column(Integer, nullable=False, default=2)

    mahasiswa = relationship(
        "Mahasiswa",
        secondary=mahasiswa_matakuliah,
        back_populates="matakuliah"
    )
