from pydantic import BaseModel

class VueloCreate(BaseModel):
    numero: str
    destino: str
    estado: str

class VueloResponse(VueloCreate):
    id: int

    class Config:
        orm_mode = True
