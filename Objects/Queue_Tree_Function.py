# MKQueue/Objects/function2.py

"""
    INDICE DE FUNCIONES

    1. Funciones de Eventos
    1.1 Funcion para listar Queue Tree
    1.2 Funcion para editar Queue Tree
    1.2.1 Funcion para editar Queue Tree y sincronizar con base de datos
    1.3 Funcion para eliminar Queue Tree
    1.3.1 Funcion para eliminar Queue Tree y sincronizar con base de datos
"""

#! Importaciones

import flet as ft
import psycopg2 as ps
from Styles import styles
from Database.querys import Connect_db
from Objects import Global_Function
from Objects import Queue_Tree_Function
from Objects import Router_Function

#! Eventos

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

#? Funcion para agregar queue trees
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

#? Funcion para listar Queue Tree
def ViewQueue(page, DataTable, Edit_Queue_Function, Delete_Queue_Function):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "SELECT * FROM queue_tree"
    )
    queues = psql.fetchall()
    psql.close()
    conn.close()

    for queue in queues:
        idqueue = queue[0]
        qname = queue[1]
        qrouter = queue[2]
        qparent = queue[3]
        qspeed = queue[4]
        dqueue= queue[5]
        uqueue= queue[6]

        edit_queue = styles.Edit_button(
            on_click= lambda e, idqueue=idqueue, qname=qname, qrouter=qrouter, qparent=qparent, qspeed=qspeed, dqueue=dqueue, uqueue=uqueue: Edit_Queue_Function(page, idqueue, qname, qrouter, qparent, qspeed, dqueue, uqueue)
        )
        delete_queue = styles.delete_button(
            on_click= lambda e, idqueue=idqueue: Delete_Queue_Function(page, idqueue)
        )
        container_action = styles.ContainerAction(
            content= ft.Row([edit_queue,delete_queue])
        )

        DataTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(queue[1])),
                    ft.DataCell(ft.Text(queue[2])),
                    ft.DataCell(ft.Text(queue[3])),
                    ft.DataCell(container_action)
                ]
            )
        )

#? Funcion para editar Queue Tree
def EditQueueFunction(page, idqueue, qname, qrouter, qparent, qspeed, dqueue, uqueue):

    #* Funcion para editar Queue Tree y sincronizar con base de datos
    def EditQueue(page, idqueue, qname, qrouter, qparent, qspeed, dqueue, uqueue, dialog):
        conn = Connect_db()
        psql = conn.cursor()
        psql.execute(
            "UPDATE queue_tree SET queuetree_name = %s, queuetree_router = %s, queuetree_parent = %s, speed = %s, download_queue = %s, upload_queue = %s WHERE id = %s",
            (
                qname,
                qrouter,
                qparent,
                qspeed,
                dqueue,
                uqueue,
                idqueue
            )
        )
        conn.commit()
        psql.close()
        conn.close()
        page.close(dialog)
        Global_Function.navigate_to_queue_tree(page)

    Txtf_qname = styles.Login_textfield(label= "Queue Name", value= qname)
    Txtf_qrouter = styles.DropDown(label= "Router", value= qrouter, on_change= lambda e: Queue_Tree_Function.ListParent(page, Txtf_qparent, Txtf_qrouter.value))
    Txtf_qparent = styles.DropDown(label= "Parent", value= qparent)
    Txtf_qspeed = styles.Login_textfield(label= "Speed", value= qspeed)
    Txtf_dqueue = styles.Login_textfield(label= "Download Queue", value= dqueue)
    Txtf_uqueue = styles.Login_textfield(label= "Upload Queue", value= uqueue)

    Router_Function.ListRouter(page, Txtf_qrouter)
    Queue_Tree_Function.ListParent(page, Txtf_qparent, qrouter)

    cancel= ft.ElevatedButton(
        style=styles.Secundary_Button, 
        text="Cancel", 
        on_click= lambda e: page.close(EditDialog)
    )

    edit= ft.ElevatedButton(
        style=styles.Primary_Button, 
        text="Edit Queue", 
        on_click= lambda e: EditQueue(page, idqueue, Txtf_qname.value, Txtf_qrouter.value, Txtf_qparent.value, Txtf_qspeed.value, Txtf_dqueue.value, Txtf_uqueue.value, EditDialog)
        )

    EditDialog = ft.AlertDialog(
        modal= True,
        title= ft.Text("Edit Queue", style=styles.Page_Subtitle),
        content= ft.Column([
            Txtf_qname,
            Txtf_qrouter,
            Txtf_qparent,
            Txtf_qspeed,
            Txtf_dqueue,
            Txtf_uqueue
        ],
        height=300
        ),
        actions_alignment= ft.MainAxisAlignment.END,
        actions= [
            cancel,
            edit
        ]
    )

    page.open(EditDialog)

#? Funcion para eliminar Queue Tree
def DeleteQueueFunction(page, idqueue):

    #* Funcion para eliminar Queue Tree y sincronizar con base de datos
    def DeleteQueue(page, dialog):
        conn = Connect_db()
        psql = conn.cursor()
        psql.execute(
            "DELETE FROM queue_tree WHERE id = %s",
            (idqueue,)
        )
        conn.commit()
        psql.close()
        conn.close()
        page.close(dialog)
        Global_Function.navigate_to_queue_tree(page)

    confirmation_Dialog= ft.AlertDialog(
        modal= True,
        title= ft.Text(style=styles.Page_Subtitle, value="Confirmation Delete"),
        actions_alignment= ft.MainAxisAlignment.END,
        actions=[
            ft.ElevatedButton(style= styles.Secundary_Button, text="Cancel", on_click= lambda e: page.close(confirmation_Dialog)),
            ft.ElevatedButton("Confirm", style= styles.Primary_Button, on_click=lambda e: DeleteQueue(page, confirmation_Dialog))
        ]
    )

    page.open(confirmation_Dialog)