import uvicorn
from fastapi import FastAPI, HTTPException

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


@app.get("/", summary='Home screen', tags=['default hands'])
def first_func() -> str:
    return 'Hellow world!!!'


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
