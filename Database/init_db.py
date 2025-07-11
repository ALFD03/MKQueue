# MKQueue/database/init_db.py

#! Importaciones

import psycopg2 as ps
from dotenv import load_dotenv
import json
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)
variables_path = os.path.join(app_root, 'Variables.json')

#! Carga de variables de entorno
load_dotenv()

#? Variables para Base de Datos
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DBNAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

#! Carga de variables json
with open(variables_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

ROUTERS = data.get('ROUTERS', [])
PARENT = data.get('PARENT', [])
PLANES = data.get('PLANES', [])

#! Funciones

#? Estableciendo Conexion con Base de datos
def init_db(HOST, PORT, DBNAME, USER, PASSWORD, ROUTERS, PARENT, PLANES):
    #* Establecer conexion con base de datos si ya estta creada
    try:
        conn = ps.connect(
            host= HOST,
            port= PORT,
            dbname= "mkqueue",
            user= USER,
            password= PASSWORD
        )
        
        create_tables(conn)
        initial_data(conn, ROUTERS, PARENT, PLANES)
    
    #* Crear Base de datos 
    except UnicodeDecodeError:
        conn = ps.connect(
            host= HOST,
            port= PORT,
            dbname= DBNAME,
            user= USER,
            password= PASSWORD,
            
        )
        conn.autocommit = True
        psql = conn.cursor()
        psql.execute("CREATE DATABASE mkqueue;")
        conn.commit()
        psql.close()
        conn.close()

        conn = ps.connect(
            host= HOST,
            port= PORT,
            dbname= "mkqueue",
            user= USER,
            password= PASSWORD
        )

        create_tables(conn)
        initial_data(conn, ROUTERS, PARENT, PLANES)

#? Creacion de tablas en la base de datos
def create_tables(conn):
    psql = conn.cursor()
    psql.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    username VARCHAR(255) NOT NULL PRIMARY KEY UNIQUE,
                    email VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255),
                    password VARCHAR(255) NOT NULL,
                    confirm_password VARCHAR(255) NOT NULL,
                    privileges INT NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS router(
                    router_name VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
                    router_ip CIDR NOT NULL,
                    router_user VARCHAR(255) NOT NULL,
                    router_password VARCHAR(255) NOT NULL,
                    router_port VARCHAR(255) NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS parent(
                    id SERIAL PRIMARY KEY,
                    parent_name VARCHAR(255) NOT NULL,
                    parent VARCHAR(255),
                    download_queue VARCHAR(255) NOT NULL,
                    upload_queue VARCHAR(255) NOT NULL,
                    router VARCHAR(255) NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS queue_tree(
                    id SERIAL PRIMARY KEY,
                    queuetree_name VARCHAR(255) NOT NULL,
                    queuetree_router VARCHAR(255) NOT NULL,
                    queuetree_parent VARCHAR(255),
                    speed INT NOT NULL,
                    download_queue VARCHAR(255) NOT NULL,
                    upload_queue VARCHAR(255) NOT NULL
                );
    """)
    conn.commit()
    psql.close()

#? Carga inicial de datos
def initial_data(conn, ROUTERS, PARENT, PLANES):
    try:
        psql = conn.cursor()
        psql.execute("SELECT 1 FROM router LIMIT 1;")
        validation_router = psql.fetchone()

        if validation_router is None:
            for router in ROUTERS:
                psql.execute(
                    "INSERT INTO router (router_name, router_ip, router_user, router_password, router_port) VALUES (%s, %s, %s, %s, %s)",
                    (
                        router["nombre"],
                        router["ip"],
                        router["usuario"],
                        router["contraseña"],
                        router["puerto"]
                    )
                )
            conn.commit()
            print("Datos de router cargados")

        else:
            print("Datos de routers ya insertados")
        
        psql.execute("SELECT 1 FROM parent LIMIT 1;")
        validation_parent = psql.fetchone()

        if validation_parent is None:
            for parent in PARENT:
                psql.execute(
                    "INSERT INTO parent (parent_name, parent, download_queue, upload_queue, router) VALUES (%s, %s, %s, %s, %s)",
                    (
                        parent["nombre"],
                        parent["padre"],
                        parent["download"],
                        parent["upload"],
                        parent["router"]
                    )
                )
            conn.commit()
            print("Datos de parent cargados")

        else:
            print("Datos de parent ya insertados")

        psql.execute("SELECT 1 FROM queue_tree LIMIT 1;")
        Validation_queuetree = psql.fetchone()

        if Validation_queuetree is None:
            for plan in PLANES:
                psql.execute(
                    "INSERT INTO queue_tree (queuetree_name, queuetree_router, queuetree_parent, speed, download_queue, upload_queue) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        plan["nombre"],
                        plan["router"],
                        plan["parent"],
                        plan["velocidad"],
                        plan["download"],
                        plan["upload"]
                    )
                )
            conn.commit()
            print("Datos de queue cargados")

        else:
            print("Datos de queue ya insertados")
        
        psql.close()

    except:
        print('Datos Iniciales no fueron cargados')

if __name__ == "__main__":
    init_db(HOST, PORT, DBNAME, USER, PASSWORD, ROUTERS, PARENT, PLANES)