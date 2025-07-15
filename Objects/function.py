# MKQueue/Objects/function.py

#! Importaciones
import flet as ft
from Styles import styles
import psycopg2 as ps
from Database.querys import Connect_db

#! Funciones de Navegacion

#? Navegacion Login to Dashboard
def Authentication(page, Username, Password):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "SELECT username FROM users WHERE username = %s AND password = %s LIMIT 1",
        (
            Username,
            Password
        )
    )
    validation = psql.fetchone()

    if validation is None:
        page.open(ft.SnackBar(ft.Text("Credenciales incorrectas.")))
    else:
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

#! Funciones para eventos

#? Funcion de Limpieza de controles
def clear_controls(page, function_page):
    function_page(page)

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


#? Funcion para agregar router
def AddRouter (router_name, router_ip, router_user, router_password, router_port):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "INSERT INTO router (router_name, router_ip, router_user, router_password,router_port) VALUES (%s, %s, %s, %s, %s)",
        (
            router_name,
            router_ip,
            router_user,
            router_password,
            router_port
        )
    )
    conn.commit()
    psql.close()
    conn.close()

#? Funcion para listar routers
def ListRouter(page, DropDown):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "SELECT router_name FROM router"
    )
    list_router = psql.fetchall()
    psql.close()
    conn.close()
    
    options = []
    
    for router in list_router:
        #router = str(router[0]).strip(" '\"")
        options.append(
            ft.DropdownOption(key=router[0])
        )

    DropDown.options=options
    page.update()

#? Funcion para listar de Parientes
def ListParent(page, DropDown, router):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "SELECT parent_name FROM parent WHERE router = %s ",
        (router,)
    )
    list_parent = psql.fetchall()
    psql.close()
    conn.close()
    
    options = []
    
    for parent in list_parent:
        options.append(
            ft.DropdownOption(key=parent[0])
        )

    DropDown.options=options
    DropDown.disabled= False
    page.update()

def AddQueueTree(queuetree_name, queuetree_router, queuetree_parent, speed, download_queue, upload_queue):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "INSERT INTO queue_tree (queuetree_name, queuetree_router, queuetree_parent, speed, download_queue, upload_queue) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            queuetree_name, 
            queuetree_router,
            queuetree_parent,
            speed,
            download_queue,
            upload_queue
        )
    )
    conn.commit()
    psql.close()
    conn.close()

def ViewRouter(page, DataTable, Edit_function, Delete_function):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "SELECT router_name, router_ip, router_user, router_password, router_port FROM router"
    )
    routers = psql.fetchall()
    psql.close()
    conn.close()

    
    for router in routers:

        idrouter = router[0]
        router_name = router[0]
        router_ip = router[1]
        router_user = router[2]
        router_password = router[3]
        router_port = router[4]

        edit_router = styles.Edit_button(
            on_click= lambda e, rid=idrouter, rname= router_name,  rip= router_ip, ruser= router_user,rpass= router_password, rport= router_port:  Edit_function(page, rid, rname, rip, ruser, rpass, rport)
            )

        delete_router = styles.delete_button(
            on_click= lambda e, rid= idrouter: Delete_function(page, rid)
        )

        router_container_action = styles.ContainerAction(
            content= ft.Row([edit_router,delete_router])
        )

        DataTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(router[0])),
                    ft.DataCell(ft.Text(router[1])),
                    ft.DataCell(ft.Text(router[2])),
                    ft.DataCell(ft.Text(router[4])),
                    ft.DataCell(router_container_action)
                ]
            )
        )

def EditRouterFunction(page, idrouter, router_name, router_ip, router_user, router_password, router_port):
    def EditRouter(page, idrouter, router_name,router_ip, router_user, router_password, router_port, dialog):
            conn = Connect_db()
            psql = conn.cursor()
            try:
                psql.execute(
                    "UPDATE router SET router_name = %s, router_ip = %s, router_user = %s, router_password = %s, router_port = %s WHERE router_name = %s",
                    (
                        router_name,
                        router_ip,
                        router_user,
                        router_password,
                        router_port,
                        idrouter
                    )
                )
                conn.commit()
                psql.close()
                conn.close()
                page.close(dialog)
                navigate_to_router(page)

            except ps.errors.UniqueViolation:
                page.open(ft.SnackBar(ft.Text("No se pudo editar ya que el nombre del router ya existe")))


    Txtf_routername = styles.Login_textfield(
        label= "Router Name", 
        value = router_name
        )
    Txtf_routerip = styles.Login_textfield(
        label= "Router Ip", 
        value = router_ip
        )
    Txtf_routeruser = styles.Login_textfield(
        label= "Router User", 
        value = router_user
        )
    Txtf_routerpassword = styles.Login_textfield(
        label= "Router Password", 
        value = router_password
        )
    Txtf_routerport = styles.Login_textfield(
        label= "Router Port", 
        value = router_port
        )

    cancel= ft.ElevatedButton(
        style=styles.Secundary_Button, 
        text="Cancel",
        on_click= lambda e: page.close(EditDialog)
    )

    edit= ft.ElevatedButton(
        style=styles.Primary_Button, 
        text="Edit Router", 
        on_click=lambda e: EditRouter(page, idrouter, Txtf_routername.value, Txtf_routerip.value,Txtf_routeruser.value, Txtf_routerpassword.value, Txtf_routerport.value, EditDialog)
    )

    EditDialog = ft.AlertDialog(
        modal= True,
        title= ft.Text("Edit Router", style=styles.Page_Subtitle),
        alignment=ft.alignment.center,
        content= ft.Column(
            [
                Txtf_routername,
                Txtf_routerip,
                Txtf_routeruser,
                Txtf_routerpassword,
                Txtf_routerport
            ]
        ),
        actions_alignment= ft.MainAxisAlignment.END,
        actions= [
            cancel,
            edit
        ],
        on_dismiss= lambda e: page.close(EditDialog)
    )

    page.open(EditDialog)

def DeleteRouterFunction(page, idrouter):
    def DeleteRouter(page, dialog):
        conn = Connect_db()
        psql = conn.cursor()
        psql.execute(
            "DELETE FROM router WHERE router_name = %s",
            (idrouter,)
        )
        conn.commit()
        psql.close()
        conn.close()
        page.close(dialog)
        navigate_to_router(page)
    
    confirmation_Dialog= ft.AlertDialog(
        modal= True,
        title= ft.Text(style=styles.Page_Subtitle, value="Confirmation Delete"),
        actions_alignment= ft.MainAxisAlignment.END,
        actions=[
            ft.ElevatedButton(style= styles.Secundary_Button, text="Cancel", on_click= lambda e: page.close(confirmation_Dialog)),
            ft.ElevatedButton("Confirm", style= styles.Primary_Button, on_click=lambda e: DeleteRouter(page, confirmation_Dialog))
        ]
    )

    page.open(confirmation_Dialog)