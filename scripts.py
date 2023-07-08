import psycopg2
from decouple import config
import json


class CarBrand:
    def __init__(self):
        self.conn = psycopg2.connect(
            database=config('DB_NAME'),
            user=config('USER'),
            password=config('PASSWORD'),
            host=config('HOST')
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        query = """CREATE TABLE cars (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            model VARCHAR(100),
            year INTEGER,
            color VARCHAR(50),
            price DECIMAL(10, 2)
        )"""

        self.cursor.execute(query)
        self.conn.commit()

    def insert_data_from_json(self, json_file):
        with open(json_file) as file:
            data = json.load(file)
        for record in data:
            self.insert_record(record)
        self.conn.commit()

    def insert_record(self, record):
        query = """INSERT INTO cars (name, model, year, color, price)
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (record['name'], record['model'], record['year'], record['color'], record['price'])
        self.cursor.execute(query, values)

    def close_db(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    save = CarBrand()
    save.create_table()
    save.insert_data_from_json('cars.json')
    save.close_db()