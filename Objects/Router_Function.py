#MKQueue/Objects/Router_Function.py

"""
    INDICE DE FUNCIONES

    1. EVENTOS
    1.1 Funcion para agregar router
    1.2 Funcion para listar routers
    1.3 Funcion para editar Router
    1.3.1 Funcion para editar el router y sincronizar con base de datos
    1.4 Funcion para Borrar Router
    1.4.1 Funcion para Borrar router y sincronizar con base de datos
"""
#! Importaciones
import flet as ft
import psycopg2 as ps
from Styles import styles
from Database.querys import Connect_db
from Objects.Global_Function import navigate_to_router

#! Eventos

#? Funcion para agregar router
def AddRouter (page, router_name, router_ip, router_user, router_password, router_port):
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
    navigate_to_router(page)


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

#? Funcion para lista de routers en pagina de router
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

#? Funcion para editar Router
def EditRouterFunction(page, idrouter, router_name, router_ip, router_user, router_password, router_port):

    #* Funcion para editar el router y sincronizar con base de datos
    def EditRouter(page, idrouter, router_name,router_ip, router_user, router_password, router_port, dialog):
            conn = Connect_db()
            psql = conn.cursor()

            # Funcion de Borrar registros de queue que tengan el router
            def EditRouterQueue(router_name, idrouter):
                psql.execute(
                    "UPDATE queue_tree SET queuetree_router = %s WHERE queuetree_router = %s",
                    (
                        router_name,
                        idrouter
                    )
                )
                conn.commit()
            def EditRouterParent(router_name, idrouter):
                psql.execute(
                    "UPDATE parent SET router = %s WHERE router = %s",
                    (
                        router_name,
                        idrouter
                    )
                )
            
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
                EditRouterQueue(router_name,idrouter)
                EditRouterParent(router_name,idrouter)
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
            ],
            height=300
        ),
        actions_alignment= ft.MainAxisAlignment.END,
        actions= [
            cancel,
            edit
        ],
        on_dismiss= lambda e: page.close(EditDialog),
    )

    page.open(EditDialog)

#? Funcion para Borrar Router
def DeleteRouterFunction(page, idrouter):

    #* Funcion para Borrar router y sincronizar con base de datos
    def DeleteRouter(page, dialog):
        conn = Connect_db()
        psql = conn.cursor()

        # Funcion para borar registros de Queue que tengan el router
        def DeleteRouterQueue(idrouter):
            psql.execute(
                "DELETE FROM queue_tree WHERE queuetree_router = %s",
                (idrouter,)
            )
            conn.commit()
        def DeleteRouterParent(idrouter):
            psql.execute(
                "DELETE FROM parent WHERE router = %s",
                (idrouter,)
            )
        psql.execute(
            "DELETE FROM router WHERE router_name = %s",
            (idrouter,)
        )
        conn.commit()
        DeleteRouterQueue(idrouter)
        DeleteRouterParent(idrouter)
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