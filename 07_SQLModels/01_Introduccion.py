from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Annotated
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

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
