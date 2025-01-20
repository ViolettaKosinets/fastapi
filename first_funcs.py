import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

films = [
    {
        'id': 1,
        'name': 'Star Wars',
        'issue_year': 1999,
        'genre': 'Научная фантастика',
        'country': 'USA',
        'director': 'Джордж Лукас'
    },
    {
        'id': 2,
        'name': 'Василий',
        'issue_year': 2024,
        'genre': 'Комедия',
        'country': 'Росиия',
        'director': 'Дмитрий Литвиненко'
    }
]


@app.get('/films', tags=['Фильмы'], summary='Get list of films')
def get_films() -> list:
    return films


@app.get('/films/{film_id}', tags=['Фильмы'], summary='Get film by id')
def get_film(film_id: int) -> dict:
    for film in films:
        if film['id'] == film_id:
            return film
    raise HTTPException(status_code=404, detail='Фильм не найден')


class FilmSchema(BaseModel):
    name: str = Field(max_length=100)
    issue_year: int = Field(ge=1895, le=2025)
    genre: str | tuple[str]
    country: str = Field(max_length=20)
    director: str

    model_config = ConfigDict(extra='forbid')


@app.post('/films', tags=['Фильмы'], summary='Add new film to books list')
def add_film(film: FilmSchema):
    films.append(
        {
            'id': films[-1]['id'] + 1,
            'name': film.name,
            'issue_year': film.issue_year,
            'genre': film.genre,
            'country': film.country,
            'director': film.director
        }
    )
    return {'post_status': True, 'message': 'Фильм добавлен'}


@app.get("/", summary='Home screen', tags=['default hands'])
def first_func() -> str:
    return 'Hellow world!!!'


if __name__ == "__main__":
    uvicorn.run("first_funcs:app", reload=True)
