import os
import psycopg
from psycopg.rows import dict_row
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Generator

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def getCursor() -> Generator[psycopg.Cursor, None, None]:
    conn = psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
        sslmode="require"
    )
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    finally:
        cursor.close()
        conn.close()

class Clientes(BaseModel):
    id: int
    Nombre: str
    Apellido: str
    NumeroTelefono: str

class Clientes_(BaseModel):
    Nombre: str
    Apellido: str
    NumeroTelefono: str

class Inventario(BaseModel):
    id: int
    respuesto: str
    marca: str
    estado: str
    vehiculo: str
    precio: int

class Inventario_(BaseModel):
    respuesto: str
    marca: str
    estado: str
    vehiculo: str
    precio: int

class Pedido(BaseModel):
    id: int
    id_cliente: int
    id_respuesto: int
    respuesto: str
    fecha_pedido: str

class Pedido_(BaseModel):
    id_cliente: int
    id_respuesto: int
    respuesto: str
    fecha_pedido: str

class insertCliente:
    def agregar(self, cliente: Clientes_, cursor: psycopg.Cursor):
        res = cursor.execute(
            'INSERT INTO "Cliente" ("Nombre", "Apellido", "NumeroTelefono") VALUES (%s,%s,%s) RETURNING id;',
            (cliente.Nombre, cliente.Apellido, cliente.NumeroTelefono)
        )
        id_nuevo = cursor.fetchone()["id"]

        return {
            "id": id_nuevo,
            "Nombre": cliente.Nombre,
            "Apellido": cliente.Apellido,
            "NumeroTelefono": cliente.NumeroTelefono
    }


    def Mostrar(self, cursor: psycopg.Cursor) -> list:
        res = cursor.execute('SELECT id, "Nombre", "Apellido", "NumeroTelefono" FROM "Cliente"').fetchall()
        return [
            {
                "id": row["id"],
                "Nombre": row["Nombre"],
                "Apellido": row["Apellido"],
                "NumeroTelefono": row["NumeroTelefono"]
            }
            for row in res
        ]

    def modificar(self, atributo: str, nuevo_valor, id: int, cursor: psycopg.Cursor):
        cursor.execute(
            f'UPDATE "Cliente" SET "{atributo}" = %s WHERE "id" = %s',
            (nuevo_valor, id)
        )
        return "Cliente modificado con éxito!"


    def eliminar(self, id_cliente: int, cursor: psycopg.Cursor):
        cursor.execute('DELETE FROM "Cliente" WHERE id = %s', (id_cliente,))
        return "Cliente eliminado con éxito!"


class insertInventario:
    def agregar(self, inventario: Inventario_, cursor: psycopg.Cursor):
        cursor.execute(
            'INSERT INTO "Inventario" ("respuesto", "marca", "estado", "vehiculo", "precio") VALUES (%s,%s,%s,%s,%s) RETURNING id;',
            (inventario.respuesto, inventario.marca, inventario.estado, inventario.vehiculo, inventario.precio)
        )
        id_nuevo = cursor.fetchone()["id"]
        return {
            "id": id_nuevo,
            "respuesto": inventario.respuesto,
            "marca": inventario.marca,
            "estado": inventario.estado,
            "vehiculo": inventario.vehiculo,
            "precio": inventario.precio
        }

    def mostrar(self, cursor: psycopg.Cursor) -> list:
        res = cursor.execute('SELECT "id", "respuesto", "marca", "estado", "vehiculo", "precio" FROM "Inventario"').fetchall()
        return [
            {
                "id": row["id"],
                "respuesto": row["respuesto"],
                "marca": row["marca"],
                "estado": row["estado"],
                "vehiculo": row["vehiculo"],
                "precio": row["precio"]
            }
            for row in res
        ]

    def modificar(self, atributo, nuevo_valor, id_inventario, cursor: psycopg.Cursor):
        cursor.execute(
            f'UPDATE "Inventario" SET "{atributo}" = %s WHERE "id" = %s',
            (nuevo_valor, id_inventario)
        )
        return "Inventario modificado con éxito!"

    def eliminar(self, id_inventario, cursor: psycopg.Cursor):
        cursor.execute('DELETE FROM "Inventario" WHERE "id" = %s', (id_inventario,))
        return "Inventario eliminado con éxito!"



class insertPedido:
    def agregar(self, pedido: Pedido_, cursor: psycopg.Cursor):
        cursor.execute(
            'INSERT INTO "Pedido" ("id_cliente", "id_respuesto", "respuesto", "fecha_pedido") VALUES (%s,%s,%s,%s) RETURNING id;',
            (pedido.id_cliente, pedido.id_respuesto, pedido.respuesto, pedido.fecha_pedido)
        )
        id_nuevo = cursor.fetchone()["id"]
        return {
            "id": id_nuevo,
            "id_cliente": pedido.id_cliente,
            "id_respuesto": pedido.id_respuesto,
            "respuesto": pedido.respuesto,
            "fecha_pedido": pedido.fecha_pedido
        }

    def mostrar(self, cursor: psycopg.Cursor) -> list:
        res = cursor.execute('SELECT "id", "id_cliente", "id_respuesto", "respuesto", "fecha_pedido" FROM "Pedido"').fetchall()
        return [
            {
                "id": row["id"],
                "id_cliente": row["id_cliente"],
                "id_respuesto": row["id_respuesto"],
                "respuesto": row["respuesto"],
                "fecha_pedido": row["fecha_pedido"]
            }
            for row in res
        ]

    def modificar(self, atributo, nuevo_valor, id_pedido, cursor: psycopg.Cursor):
        cursor.execute(
            f'UPDATE "Pedido" SET "{atributo}" = %s WHERE "id" = %s',
            (nuevo_valor, id_pedido)
        )
        return "Pedido modificado con éxito!"

    def eliminar(self, id_pedido, cursor: psycopg.Cursor):
        cursor.execute('DELETE FROM "Pedido" WHERE "id" = %s', (id_pedido,))
        return "Pedido eliminado con éxito!"

