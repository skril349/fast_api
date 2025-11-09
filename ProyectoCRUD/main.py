from pydantic import BaseModel, Field
from typing import Annotated, Literal
from fastapi import FastAPI, Depends, HTTPException

class Tarea(BaseModel):
    id: Annotated[int, Field(gt=0)]
    titulo: Annotated[str, Field(min_length=3)]
    estado: Literal["pendiente", "completado"] = "pendiente"

class FilterParams(BaseModel):
    limit: Annotated[int, Field(ge=1)] = 5
    offset: Annotated[int, Field(ge=0)] = 0
    estado: Literal["pendiente", "completado"] | None = None
    search: str | None = None

fake_db: list[Tarea] = [
    Tarea(id=1, titulo="Estudiar Python", estado="pendiente"),
    Tarea(id=2, titulo="Lavar la ropa", estado="completado"),
    Tarea(id=3, titulo="Leer un libro", estado="pendiente"),
    Tarea(id=4, titulo="Ir al gimnasio", estado="completado"),
    Tarea(id=5, titulo="Comprar comida", estado="pendiente"),
    Tarea(id=6, titulo="Limpiar el cuarto", estado="pendiente"),
    Tarea(id=7, titulo="Pagar cuentas", estado="completado"),
    Tarea(id=8, titulo="Llamar a mamá", estado="pendiente"),
    Tarea(id=9, titulo="Revisar correo", estado="pendiente"),
    Tarea(id=10, titulo="Lavar carro", estado="pendiente"),
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


@app.get("/tareas/{id}")
def get_tarea(id: int):
    for tarea in fake_db:
        if tarea.id == id:
            return tarea    
    raise HTTPException(status_code=404, detail = "No existe el id")