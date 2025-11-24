from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base

class Kelas(Base):
    __tablename__ = "kelas"

    id = Column(Integer, primary_key=True)
    nama = Column(String, nullable=False)

    mahasiswa = relationship("Mahasiswa", back_populates="kelas")
