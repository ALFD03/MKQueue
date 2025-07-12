# MKQueue/Objects/function.py

#! Importaciones
import flet as ft
from Database.querys import Connect_db

#! Funciones de Navegacion

#? Navegacion Login to Dashboard
def Authentication(page, Username, Password):
    if Username == "admin" and Password == "admin":
        navigate_to_dashboard(page)
    else:
        page.open(ft.SnackBar(ft.Text("Credenciales incorrectas.")))

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

#! Funciones para eventos

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

#? Funcion de Limpieza de controles
def clear_controls(page, function_page):
    function_page(page)


            