# MKQueue/Database/querys.py

#! Importaciones
import psycopg2 as ps
from dotenv import load_dotenv
import os

#! Carga de variables de entorno
load_dotenv()

def Connect_db():
    conn = ps.connect(
        host= os.getenv("DB_HOST"),
        port= os.getenv("DB_PORT"),
        dbname= "mkqueue",
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD")
    )

    return conn