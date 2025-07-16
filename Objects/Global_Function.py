# MKQueue/Objects/function.py

"""
    INDICE DE FUNCIONES

    1. Navegacion
    1.1 Autenticacion de Login
    1.2 Navegacion a Dashboard
    1.3 Navegacion a Queue Tree
    1.4 Navegacion a Router
    1.5 Navegacion a Settings
    1.6 Navegacion a Add New User
    1.7 Navegacion a Add New Router
    1.8 Navegacion a Add New Queue Tree

    2. Eventos
    2.1 Funcion de Limpieza de controles
   
"""

#! Importaciones
import flet as ft
import psycopg2 as ps
from Styles import styles
from Database.querys import Connect_db

#! Navegacion

#? Navegacion Login to Dashboard
def Authentication(page, Username, Password):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "SELECT username, email, name, last_name FROM users WHERE username = %s AND password = %s LIMIT 1",
        (
            Username,
            Password
        )
    )
    validation = psql.fetchone()

    if validation is None:
        psql.close()
        conn.close()
        page.open(ft.SnackBar(ft.Text("Credenciales incorrectas.")))
    else:
        # Guardar datos del usuario activo en la página
        page.user_data = {
            "username": validation[0],
            "email": validation[1],
            "name": validation[2],
            "last_name": validation[3]
        }
        psql.close()
        conn.close()
        navigate_to_dashboard(page)

#? Navegacion to Dashboard
def navigate_to_dashboard(page):
    from Pages.dashboard import Dashboard
    Dashboard(page)

#? Navegacion to Queue Tree
def navigate_to_queue_tree(page):
    from Pages.QueueTree import QueueTree
    QueueTree(page)

#? Navegacion to Queue Type
# def navigate_to_queue_type(page):
#     from Pages.QueueType import QueueType
#     QueueType(page)

#? Navegacion to Router
def navigate_to_router(page):
    from Pages.Router import Router
    Router(page)

#? Navegacion to Settings
def navigate_to_settings(page):
    from Pages.Settings import Settings
    Settings(page)

#? Navegacion to Add New User
def navigate_to_add_new_user(page):
    from Pages.Sub_Pages.Add_New_User import Add_New_User
    Add_New_User(page)

#? Navegacion to Add New Router
def navigate_to_add_new_router(page):
    from Pages.Sub_Pages.Add_Router import Add_Router
    Add_Router(page)

#? Navegacion to Add New Queue Tree
def navigate_to_add_new_queue_tree(page):
    from Pages.Sub_Pages.Add_Queue_tree import Add_Queue_tree
    Add_Queue_tree(page)

#? Navegacion to Load File
def navigate_to_load_file(page):
    from Pages.load_file import Load_File
    Load_File(page)

#? Obtener datos del usuario activo
def get_active_user_data(page):
    """Obtiene los datos del usuario activo desde la página"""
    if hasattr(page, 'user_data'):
        return page.user_data
    return None

#? Verificar si el usuario está autenticado
def require_auth(page):
    """Verifica si el usuario está autenticado, si no, redirige al login"""
    if not get_active_user_data(page):
        from Pages.Login import Login
        Login(page)
        return False
    return True

#! Eventos

#? Funcion de Limpieza de controles
def clear_controls(page, function_page):
    function_page(page)
