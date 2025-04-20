from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas, database
from tda_lista_doble import ListaDoble
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
lista_vuelos = ListaDoble()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vuelos/", response_model=schemas.VueloResponse)
def crear_vuelo(vuelo: schemas.VueloCreate, db: Session = Depends(get_db)):
    db_vuelo = models.Vuelo(**vuelo.dict())
    db.add(db_vuelo)
    db.commit()
    db.refresh(db_vuelo)

    if vuelo.estado == "emergencia":
        lista_vuelos.insertar_al_frente(db_vuelo)
    else:
        lista_vuelos.insertar_al_final(db_vuelo)
    return db_vuelo

@app.get("/vuelos/primero", response_model=schemas.VueloResponse)
def obtener_primer_vuelo():
    vuelo = lista_vuelos.obtener_primero()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos")
    return vuelo

@app.get("/vuelos/ultimo", response_model=schemas.VueloResponse)
def obtener_ultimo_vuelo():
    vuelo = lista_vuelos.obtener_ultimo()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos")
    return vuelo

@app.delete("/vuelos/{posicion}", response_model=schemas.VueloResponse)
def eliminar_por_posicion(posicion: int, db: Session = Depends(get_db)):
    vuelo = lista_vuelos.extraer_de_posicion(posicion)
    if vuelo is None:
        raise HTTPException(status_code=404, detail="Posición inválida")
    db_vuelo = db.query(models.Vuelo).filter_by(id=vuelo.id).first()
    if db_vuelo:
        db.delete(db_vuelo)
        db.commit()
    return vuelo
# Para longitud
@app.get("/vuelos/longitud")
def obtener_longitud():
    return {"longitud": lista_vuelos.longitud()}

# Para insertar en posición específica
@app.post("/vuelos/insertar/{posicion}", response_model=schemas.VueloResponse)
def insertar_en_posicion(vuelo: schemas.VueloCreate, posicion: int, db: Session = Depends(get_db)):
    db_vuelo = models.Vuelo(**vuelo.dict())
    db.add(db_vuelo)
    db.commit()
    db.refresh(db_vuelo)
    lista_vuelos.insertar_en_posicion(db_vuelo, posicion)
    return db_vuelo

@app.get("/vuelos/", response_model=list[schemas.VueloResponse])
def obtener_todos(db: Session = Depends(get_db)):
    return db.query(models.Vuelo).all()
