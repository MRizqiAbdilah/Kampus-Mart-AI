from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.base import Base


class Saldo(Base):
    __tablename__ = "saldo"

    id = Column(Integer, primary_key=True, index=True)
    mahasiswa_id = Column(Integer, ForeignKey("mahasiswa.id"), nullable=False)
    jumlah = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending / confirmed
    created_at = Column(DateTime, default=datetime.utcnow)

    mahasiswa = relationship("Mahasiswa", backref="transaksi_saldo")
