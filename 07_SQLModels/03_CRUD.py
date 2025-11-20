from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Annotated
from fastapi import FastAPI, Depends, Query, HTTPException
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


# CRUD Operations
# Get heroes
@app.get("/heroes/", response_model=list[HeroPublic])
def get_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10
    ):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Get Hero by ID
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def get_hero_by_id(hero_id: int,session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Create Hero
@app.post("/heroes/", response_model=HeroPublic, status_code=201)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# Update Hero
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(
    hero_id: int,
    hero_update: HeroUpdate,
    session: SessionDep
    ):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    hero_data = hero_update.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# Delete Hero
@app.delete("/heroes/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: SessionDep):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(db_hero)
    session.commit()
    return {"ok": True}