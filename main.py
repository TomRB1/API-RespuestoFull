from fastapi import FastAPI
from routes.cliente import router as routerClientes
from routes.inventario import router as routerInventario
from routes.pedido import router as routerPedidos

app = FastAPI()

app.include_router(routerClientes)
app.include_router(routerInventario)
app.include_router(routerPedidos)
