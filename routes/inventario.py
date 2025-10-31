from fastapi import APIRouter, Depends
from dbmanager import insertInventario, getCursor
from dbmanager import Inventario, Inventario_, insertInventario


router = APIRouter()
inventarioG = insertInventario()

@router.get("/inventario/", response_model=list[Inventario])
def get_inventario(cursor=Depends(getCursor)):
    return inventarioG.mostrar(cursor)

@router.post("/inventario/agregar", response_model=Inventario)
def post_inventario(item: Inventario_, cursor=Depends(getCursor)):
    return inventarioG.agregar(item, cursor)

@router.put("/inventario/{id}", response_model=Inventario)
def put_inventario(id: int, item: Inventario_, cursor=Depends(getCursor)):
    inventarioG.modificar("respuesto", item.respuesto, id, cursor)
    inventarioG.modificar("marca", item.marca, id, cursor)
    inventarioG.modificar("estado", item.estado, id, cursor)
    inventarioG.modificar("vehiculo", item.vehiculo, id, cursor)
    inventarioG.modificar("precio", item.precio, id, cursor)
    
    cursor.execute('SELECT "id", "respuesto", "marca", "estado", "vehiculo", "precio" FROM "Inventario" WHERE "id" = %s', (id,))
    return cursor.fetchone()

@router.delete("/inventario/{id}", response_model=dict)
def delete_inventario(id: int, cursor=Depends(getCursor)):
    return {"mensaje": inventarioG.eliminar(id, cursor)}

