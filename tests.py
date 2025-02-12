import psycopg2

conn = psycopg2.connect(dbname="cinemadb", host="127.0.0.1", user="postgres", password="BabyfooLPGSQL")


def create_db(name):
    conn.autocommit = True
    with conn.cursor() as cursor:
        # команда для создания базы данных metanit
        sql = f'CREATE DATABASE {name}'
        cursor.execute(sql)
    conn.autocommit = False


def create_table(name, fields):
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE films")
        sql = f'CREATE TABLE {name} ({fields})'
        cursor.execute(sql)
        conn.commit()


create_table('films', 'id SERIAL PRIMARY KEY, '
                      'title VARCHAR(50),  '
                      'year INTEGER CHECK (year >= 1981 and year <= 2027)')

with conn.cursor() as cursor:
    sql = 'INSERT INTO films (title, year) VALUES (%s, %s)'
    films = [('Матрица', 1999), ('Социальная сеть', 2010), ('Микки монстр', 2025)]
    cursor.executemany(sql, films)

    cursor.execute("SELECT * FROM films")
    for film in cursor.fetchall():
        print(f"{film[0]}) {film[1]} ({film[2]})")

    cursor.execute("SELECT title, year FROM films WHERE id=2")
    title, year = cursor.fetchone()
    print(f"\nВыборка по значению (вывод одного объекта):\n{title} ({year})\n")

    cursor.execute("UPDATE films SET title='Матрица 1' WHERE title='Матрица'")
    cursor.execute("SELECT * FROM films")
    print(f'Изменеyие значений объектов:\n{cursor.fetchall()}\n')

    cursor.execute("DELETE FROM films WHERE year=%s", (2010,))
    cursor.execute("SELECT * FROM films")
    print(f'Удаление объектов:\n{cursor.fetchall()}\n')

    conn.commit()


conn.close()
