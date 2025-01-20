from typing import Annotated
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///films.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class FilmModel(Base):
    __tablename__ = 'films'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    director: Mapped[str]


@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return {'creation_db_status': True}


class FilmPostSchema(BaseModel):
    name: str
    director: str


class FilmSchema(FilmPostSchema):
    id: int


@app.post('/films')
async def add_film(base: FilmPostSchema, session: SessionDep):
    new_film = FilmModel(
        name=base.name,
        director=base.director
    )
    session.add(new_film)
    await session.commit()
    return {'post_to_db_status': True}


@app.get('/films')
async def get_films(session: SessionDep):
    query = select(FilmModel)
    result = await session.execute(query)  # iter
    return result.scalars().all()
