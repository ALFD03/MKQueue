#MKQueue/Objects/Settings_Function.py

"""
    INDICE DE FUNCIONES

    1. EVENTOS
    1.1 Funcion de Agregar user
"""

#! Importaciones
import flet as ft
import psycopg2 as ps
from Styles import styles
from Database.querys import Connect_db


#! Eventos

#? Funcion de Agregar user
def AddNewUser (Username, Email, Name, Last_name, Password, Confirm_Password, Privileges):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "INSERT INTO users (username, email, name, last_name, password, confirm_password, privileges) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            Username,
            Email,
            Name,
            Last_name,
            Password,
            Confirm_Password,
            Privileges
        )
    )
    conn.commit()
    psql.close()
    conn.close()
