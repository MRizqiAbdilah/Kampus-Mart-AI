from pydantic import BaseModel

class ProdukBase(BaseModel):
    nama_produk: str
    deskripsi: str | None = None
    harga: float

class ProdukCreate(ProdukBase):
    pass

class ProdukResponse(ProdukBase):
    id: int
    penjual_id: int  # tetap ditampilkan saat response

    class Config:
        from_attributes = True
