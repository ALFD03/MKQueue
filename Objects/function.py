# MKQueue/Objects/function.py

#! Importaciones
import flet as ft

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
