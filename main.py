import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/", summary='Home screen', tags=['default hands'])
def first_func() -> str:
    return 'Hellow world!!!'


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
