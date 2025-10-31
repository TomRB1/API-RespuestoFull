from fastapi import APIRouter, Depends
from dbmanager import insertCliente, getCursor
from dbmanager import Clientes, Clientes_, insertCliente


router = APIRouter()
clientes = insertCliente()

@router.get("/clientes/", response_model=list[Clientes])
def get_clientes(cursor=Depends(getCursor)):
    return clientes.Mostrar(cursor)

@router.post("/clientes/añadir", response_model=Clientes)
def post_clientes(cliente: Clientes_, cursor=Depends(getCursor)):
    return clientes.agregar(cliente, cursor)

@router.put("/clientes/{id}", response_model=Clientes)
def put_clientes(id: int, cliente: Clientes_, cursor=Depends(getCursor)):
    clientes.modificar("Nombre", cliente.Nombre, id, cursor)
    clientes.modificar("Apellido", cliente.Apellido, id, cursor)
    clientes.modificar("NumeroTelefono", cliente.NumeroTelefono, id, cursor)
    cursor.execute('SELECT "id" AS id, "Nombre", "Apellido", "NumeroTelefono" FROM "Cliente" WHERE "id" = %s',(id,))

    return cursor.fetchone()

@router.delete("/clientes/{id}", response_model=dict)
def delete_clientes(id: int, cursor=Depends(getCursor)):
    return {"mensaje": clientes.eliminar(id, cursor)}
