from pydantic import BaseModel, Field
from typing import Annotated, Literal
from fastapi import FastAPI, Depends, HTTPException
from itertools import count

id_generator = count(start=1)
def obtener_nuevo_id() -> int:
    return next(id_generator)

class TareaBase(BaseModel):
    titulo: Annotated[str, Field(min_length=3)]
    estado: Literal["pendiente", "completado"] = "pendiente"

class Tarea(TareaBase):
    id: Annotated[int, Field(gt=0)]

class TareaCreate(TareaBase):
    pass 

class TareaUpdate(BaseModel):
    titulo: Annotated[str, Field(min_length=3)]
    estado: Literal["pendiente", "completado"]


class FilterParams(BaseModel):
    limit: Annotated[int, Field(ge=1)] = 5
    offset: Annotated[int, Field(ge=0)] = 0
    estado: Literal["pendiente", "completado"] | None = None
    search: str | None = None

fake_db: list[Tarea] = [
    Tarea(id=obtener_nuevo_id(), titulo="Estudiar Python", estado="pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo="Lavar la ropa", estado="completado"),
    Tarea(id=obtener_nuevo_id(), titulo="Leer un libro", estado="pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo="Ir al gimnasio", estado="completado"),
    Tarea(id=obtener_nuevo_id(), titulo="Comprar comida", estado="pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo="Limpiar el cuarto", estado="pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo="Pagar cuentas", estado="completado"),
    Tarea(id=obtener_nuevo_id(), titulo="Llamar a mamá", estado="pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo="Revisar correo", estado="pendiente"),
    Tarea(id=obtener_nuevo_id(), titulo="Lavar carro", estado="pendiente"),
]

app = FastAPI()

@app.get("/tareas/", response_model=list[Tarea])
async def get_tareas(filtros: FilterParams = Depends()):
    # punt de partida
    tareas_filtradas = fake_db

    # filtre per estat
    if filtros.estado:
        tareas_filtradas = [
            tarea for tarea in tareas_filtradas
            if tarea.estado == filtros.estado
        ]

    # filtre per text
    if filtros.search:
        tareas_filtradas = [
            t for t in tareas_filtradas
            if filtros.search.lower() in t.titulo.lower()
        ]

    # aplicar paginació
    inicio = filtros.offset
    fin = filtros.offset + filtros.limit
    return tareas_filtradas[inicio:fin]


@app.get("/tareas/{id}", response_model= Tarea)
def get_tarea(id: int):
    for tarea in fake_db:
        if tarea.id == id:
            return tarea    
    raise HTTPException(status_code=404, detail = "No existe el id")

@app.post("/tareas/",response_model= Tarea, status_code=201)
async def post_tarea(tarea:TareaCreate):
    nuevo_id : int = obtener_nuevo_id()
    nueva_tarea: Tarea = Tarea(id=nuevo_id, **tarea.model_dump())
    fake_db.append(nueva_tarea)
    return nueva_tarea

@app.put("/tareas/{id}", response_model= Tarea)
async def edit_tarea(id:int, datos: TareaUpdate):
    for i, tarea in enumerate(fake_db):
        if tarea.id == id:
            tarea_actualizada = tarea.model_copy(update=datos.model_dump())
            fake_db[i] = tarea_actualizada
            return tarea_actualizada
    raise HTTPException(status_code=404,detail = "No existe el id")


@app.delete("/tareas/{id}", response_model=Tarea)
async def delete_tarea(id: int):
    for i, tarea in enumerate(fake_db):
        if tarea.id == id:
            tarea_eliminada = fake_db.pop(i)
            return tarea_eliminada
    raise HTTPException(status_code=404, detail="No existe el id")
