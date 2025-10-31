from fastapi import APIRouter, Depends
from dbmanager import insertPedido, getCursor
from dbmanager import Pedido, Pedido_, insertPedido


router = APIRouter()
pedidos = insertPedido()

@router.get("/pedidos/", response_model=list[Pedido])
def get_pedidos(cursor=Depends(getCursor)):
    return pedidos.mostrar(cursor)

@router.post("/pedidos/agregar", response_model=Pedido)
def post_pedido(pedido: Pedido_, cursor=Depends(getCursor)):
    return pedidos.agregar(pedido, cursor)

@router.put("/pedidos/{id}", response_model=Pedido)
def put_pedido(id: int, pedido: Pedido_, cursor=Depends(getCursor)):
    pedidos.modificar("id_cliente", pedido.id_cliente, id, cursor)
    pedidos.modificar("id_respuesto", pedido.id_respuesto, id, cursor)
    pedidos.modificar("respuesto", pedido.respuesto, id, cursor)
    pedidos.modificar("fecha_pedido", pedido.fecha_pedido, id, cursor)
    
    cursor.execute('SELECT "id", "id_cliente", "id_respuesto", "respuesto", "fecha_pedido" FROM "Pedido" WHERE "id" = %s', (id,))
    return cursor.fetchone()

@router.delete("/pedidos/{id}", response_model=dict)
def delete_pedido(id: int, cursor=Depends(getCursor)):
    return {"mensaje": pedidos.eliminar(id, cursor)}


