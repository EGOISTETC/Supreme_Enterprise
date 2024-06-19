import os
from dotenv import load_dotenv
import psycopg2
load_dotenv()

class PgDataBase:
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = int(os.getenv('DB_PORT'))


class PgDriver:
    def __init__(self):
        self.dbname = PgDataBase.DB_NAME
        self.user = PgDataBase.DB_USER
        self.password = PgDataBase.DB_PASSWORD
        self.host = PgDataBase.DB_HOST
        self.port = PgDataBase.DB_PORT
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def execute_query(self, query, params=None):
        if self.conn is None:
            raise Exception("Connection is not established. Call connect() method first.")

        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur

    def commit(self):
        if self.conn is not None:
            self.conn.commit()

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.commit()
        self.close_connection()


def get_referal_id(id: int):
     with PgDriver() as curr:
                data = curr.execute_query(""" SELECT * FROM "analytic_referal" WHERE login = %s;
                """, (id,)).fetchone()