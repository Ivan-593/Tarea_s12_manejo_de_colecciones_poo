import json
import os
from typing import Callable, TypeVar

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

T = TypeVar("T")

RUTA_PRODUCTOS = os.path.join("datos", "productos.json")
RUTA_USUARIOS = os.path.join("datos", "usuarios.json")
RUTA_VENTAS = os.path.join("datos", "ventas.json")


class ArchivoServicio:

    @staticmethod
    def _asegurar_carpeta(ruta_archivo: str) -> None:
        carpeta = os.path.dirname(ruta_archivo)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)

    @staticmethod
    def _cargar_lista_generica(
        ruta_archivo: str,
        constructor: Callable[[dict], T],
        nombre_coleccion: str,
    ) -> list[T]:

        objetos: list[T] = []
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except FileNotFoundError:
            print(
                f"Aviso: no se encontró '{ruta_archivo}'. "
                f"Se iniciará la colección de {nombre_coleccion} vacía."
            )
            return objetos
        except json.JSONDecodeError:
            print(
                f"Aviso: '{ruta_archivo}' contiene JSON inválido. "
                f"Se iniciará la colección de {nombre_coleccion} vacía."
            )
            return objetos
        except PermissionError:
            print(
                f"Error: no hay permisos de lectura sobre '{ruta_archivo}'. "
                f"Se iniciará la colección de {nombre_coleccion} vacía."
            )
            return objetos

        for registro in registros:
            try:
                objetos.append(constructor(registro))
            except KeyError as error:
                print(
                    f"Aviso: se omitió un registro de {nombre_coleccion} "
                    f"por falta de datos ({error})."
                )
            except ValueError as error:
                print(
                    f"Aviso: se omitió un registro de {nombre_coleccion} "
                    f"por datos inválidos ({error})."
                )
        return objetos

    @staticmethod
    def _guardar_lista_generica(
        ruta_archivo: str,
        objetos: list,
        nombre_coleccion: str,
    ) -> bool:

        try:
            ArchivoServicio._asegurar_carpeta(ruta_archivo)
            datos = [objeto.convertir_a_diccionario() for objeto in objetos]
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print(
                f"Error: no hay permisos de escritura sobre '{ruta_archivo}'. "
                f"No se pudo guardar la colección de {nombre_coleccion}."
            )
            return False

    @staticmethod
    def cargar_productos(ruta_archivo: str = RUTA_PRODUCTOS) -> list[Producto]:
        return ArchivoServicio._cargar_lista_generica(
            ruta_archivo, Producto.crear_desde_diccionario, "productos"
        )

    @staticmethod
    def guardar_productos(
        productos: list[Producto], ruta_archivo: str = RUTA_PRODUCTOS
    ) -> bool:
        return ArchivoServicio._guardar_lista_generica(
            ruta_archivo, productos, "productos"
        )

    @staticmethod
    def cargar_usuarios(ruta_archivo: str = RUTA_USUARIOS) -> list[Usuario]:
        return ArchivoServicio._cargar_lista_generica(
            ruta_archivo, Usuario.crear_desde_diccionario, "usuarios"
        )

    @staticmethod
    def guardar_usuarios(
        usuarios: list[Usuario], ruta_archivo: str = RUTA_USUARIOS
    ) -> bool:
        return ArchivoServicio._guardar_lista_generica(
            ruta_archivo, usuarios, "usuarios"
        )

    @staticmethod
    def cargar_ventas(ruta_archivo: str = RUTA_VENTAS) -> list[Venta]:
        return ArchivoServicio._cargar_lista_generica(
            ruta_archivo, Venta.crear_desde_diccionario, "ventas"
        )

    @staticmethod
    def guardar_ventas(ventas: list[Venta], ruta_archivo: str = RUTA_VENTAS) -> bool:
        return ArchivoServicio._guardar_lista_generica(ruta_archivo, ventas, "ventas")