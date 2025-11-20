from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Annotated
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager


# Modelo base para los usuarios
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int = Field(index=True, default=None)

# Modelo base de datos
class Hero(HeroBase, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
    secret_name: str

# Modelo publico (respuestas API)
class HeroPublic(HeroBase):
    id: int

# Modelo para crear 
class HeroCreate(HeroBase):
    secret_name: str

# Modelo para actualizar
class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


# Configuracion de la base de datos
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    echo=True
    )


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Crear sesion y dependencia
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Lifespan Events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Codigo que ejecutar al iniciar la aplicacion
    create_db_and_tables()
    yield 
    # Codigo que ejecutar al cerrar la aplicacion

app = FastAPI(lifespan=lifespan)
