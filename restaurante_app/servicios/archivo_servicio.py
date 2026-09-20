import json
from pathlib import Path
from typing import List

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class ArchivoServicio:
    def __init__(self, ruta_datos: str = "datos") -> None:
        ruta_datos_path = Path(ruta_datos)
        self._ruta_productos = ruta_datos_path / "productos.json"
        self._ruta_usuarios = ruta_datos_path / "usuarios.json"
        self._ruta_ventas = ruta_datos_path / "ventas.json"

    # ---------- Productos (logica original del alumno) ----------
    def cargar_productos(self) -> List[Producto]:
        try:
            with open(self._ruta_productos, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("El archivo de productos no tiene un formato JSON valido.")
            return []
        except PermissionError:
            print("No hay permisos suficientes para leer el archivo de productos.")
            return []

        if not isinstance(datos, list):
            print("El archivo de productos debe contener una lista de registros.")
            return []

        productos: List[Producto] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Se encontro un registro de producto con formato invalido y fue omitido.")
                continue
            try:
                producto = Producto(
                    codigo=item["codigo"],
                    nombre=item["nombre"],
                    categoria=item["categoria"],
                    precio=item["precio"],
                    stock=item.get("stock", 0),
                )
                productos.append(producto)
            except KeyError:
                print("Se encontro un registro de producto incompleto y fue omitido.")
            except ValueError as error:
                print(f"Se encontro un producto con datos invalidos: {error}")
        return productos

    def guardar_productos(self, productos: List[Producto]) -> bool:
        datos = [producto.convertir_a_diccionario() for producto in productos]
        try:
            self._ruta_productos.parent.mkdir(parents=True, exist_ok=True)
            with open(self._ruta_productos, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print("No hay permisos suficientes para guardar el archivo de productos.")
            return False

    def cargar_usuarios(self) -> List[Usuario]:
        try:
            with open(self._ruta_usuarios, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("El archivo de usuarios no tiene un formato JSON valido.")
            return []
        except PermissionError:
            print("No hay permisos suficientes para leer el archivo de usuarios.")
            return []

        if not isinstance(datos, list):
            print("El archivo de usuarios debe contener una lista de registros.")
            return []

        usuarios: List[Usuario] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Se encontro un registro de usuario con formato invalido y fue omitido.")
                continue
            try:
                usuario = Usuario(
                    identificacion=item["identificacion"],
                    nombre=item["nombre"],
                    correo=item["correo"],
                )
                usuarios.append(usuario)
            except KeyError:
                print("Se encontro un registro de usuario incompleto y fue omitido.")
            except ValueError as error:
                print(f"Se encontro un usuario con datos invalidos: {error}")
        return usuarios

    def guardar_usuarios(self, usuarios: List[Usuario]) -> bool:
        datos = [usuario.convertir_a_diccionario() for usuario in usuarios]
        try:
            self._ruta_usuarios.parent.mkdir(parents=True, exist_ok=True)
            with open(self._ruta_usuarios, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print("No hay permisos suficientes para guardar el archivo de usuarios.")
            return False

    def cargar_ventas(self) -> List[Venta]:
        try:
            with open(self._ruta_ventas, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("El archivo de ventas no tiene un formato JSON valido.")
            return []
        except PermissionError:
            print("No hay permisos suficientes para leer el archivo de ventas.")
            return []

        if not isinstance(datos, list):
            print("El archivo de ventas debe contener una lista de registros.")
            return []

        ventas: List[Venta] = []
        for item in datos:
            if not isinstance(item, dict):
                print("Se encontro un registro de venta con formato invalido y fue omitido.")
                continue
            try:
                venta = Venta(
                    usuario_id=item["usuario_id"],
                    producto_codigo=item["producto_codigo"],
                    cantidad=item["cantidad"],
                )
                ventas.append(venta)
            except KeyError:
                print("Se encontro un registro de venta incompleto y fue omitido.")
            except ValueError as error:
                print(f"Se encontro una venta con datos invalidos: {error}")
        return ventas

    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        datos = [venta.convertir_a_diccionario() for venta in ventas]
        try:
            self._ruta_ventas.parent.mkdir(parents=True, exist_ok=True)
            with open(self._ruta_ventas, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except PermissionError:
            print("No hay permisos suficientes para guardar el archivo de ventas.")
            return False