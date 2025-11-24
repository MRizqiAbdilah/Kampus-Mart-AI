from sqlalchemy import Table, Column, Integer, ForeignKey
from database.base import Base

mahasiswa_matakuliah = Table(
    "mahasiswa_matakuliah",
    Base.metadata,
    Column("mahasiswa_id", Integer, ForeignKey("mahasiswa.id"), primary_key=True),
    Column("matakuliah_id", Integer, ForeignKey("matakuliah.id"), primary_key=True)
)
