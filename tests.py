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
        sql = f'CREATE TABLE {name} ({fields})'
        cursor.execute(sql)
        conn.commit()


# create_table('film', 'id SERIAL PRIMARY KEY, title VARCHAR(50),  year DATE')
conn.close()
