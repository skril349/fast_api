from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from typing import Annotated
from fastapi import FastAPI, Depends, Query, HTTPException
from contextlib import asynccontextmanager


# Modelo base 
class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str | None = None

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(index=True, default=None)

class Team(TeamBase, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
    heroes: list["Hero"] = Relationship(back_populates="team")


# Modelo base de datos
class Hero(HeroBase, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
    secret_name: str
    team_id: Annotated[int | None, Field(foreign_key="team.id")] = None
    team: Team | None = Relationship(back_populates="heroes")

# Modelo publico (respuestas API)
class TeamPublic(TeamBase):
    id: int

class HeroPublic(HeroBase):
    id: int
    team_id: int | None = None

# Modelo para crear 

class TeamCreate(TeamBase):
    pass

class HeroCreate(HeroBase):
    team_id: int | None = None
    secret_name: str

# Modelo para actualizar

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None

class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
    team_id: int | None = None

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
    db_hero.sqlmodel_update(hero_data)
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

# Teams
# ------------------------
# Create team
@app.post("/teams/", response_model=TeamPublic)
def create_team(team: TeamCreate, session: SessionDep):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

# Get teams
@app.get("/teams/", response_model=list[TeamPublic])
def get_teams(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 10
    ):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams

# Get team by ID
@app.get("/teams/{team_id}", response_model=TeamPublic)
def get_team_by_id(team_id: int,session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Update team
@app.patch("/teams/{team_id}", response_model=TeamPublic)
def update_team(
    team_id: int,
    team_update: TeamUpdate,
    session: SessionDep
    ):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team_data = team_update.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

# Delete team
@app.delete("/teams/{team_id}", status_code=204)
def delete_team(team_id: int, session: SessionDep):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    for hero in team.heroes:
        hero.team_id = None
        hero.team = None
    session.delete(team)
    session.commit()
    return {"ok": True}