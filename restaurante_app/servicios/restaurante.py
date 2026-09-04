from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class Restaurante:

    def __init__(self) -> None:
        self._productos: list[Producto] = ArchivoServicio.cargar_productos()
        self._usuarios: list[Usuario] = ArchivoServicio.cargar_usuarios()
        self._ventas: list[Venta] = ArchivoServicio.cargar_ventas()

        self._indice_productos: dict[str, Producto] = {}
        self._indice_usuarios: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}
        self._reconstruir_indices()



    def _reconstruir_indices(self) -> None:

        self._indice_productos = {
            producto.codigo: producto for producto in self._productos
        }
        self._indice_usuarios = {
            usuario.identificacion: usuario for usuario in self._usuarios
        }

        self._ventas_por_usuario = {}
        for venta in self._ventas:
            self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)


    def registrar_producto(
        self, codigo: str, nombre: str, precio: float, stock: int
    ) -> bool:

        if self.buscar_producto(codigo) is not None:
            print(f"Ya existe un producto con el código '{codigo}'.")
            return False
        try:
            producto = Producto(codigo=codigo, nombre=nombre, precio=precio, stock=stock)
        except ValueError as error:
            print(f"No se pudo registrar el producto: {error}")
            return False
        self._productos.append(producto)
        self._indice_productos[producto.codigo] = producto
        self._guardar_productos()
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:

        return self._indice_productos.get(codigo)

    def listar_productos(self) -> list[Producto]:

        return list(self._productos)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str | None = None,
        precio: float | None = None,
    ) -> bool:

        producto = self.buscar_producto(codigo)
        if producto is None:
            print(f"No existe un producto con el código '{codigo}'.")
            return False
        try:
            if nombre is not None:
                producto.nombre = nombre
            if precio is not None:
                producto.precio = precio
        except ValueError as error:
            print(f"No se pudo actualizar el producto: {error}")
            return False

        self._guardar_productos()
        return True

    def eliminar_producto(self, codigo: str) -> bool:

        producto = self.buscar_producto(codigo)
        if producto is None:
            print(f"No existe un producto con el código '{codigo}'.")
            return False
        self._productos.remove(producto)
        del self._indice_productos[codigo]
        self._guardar_productos()
        return True

    def _guardar_productos(self) -> None:
        ArchivoServicio.guardar_productos(self._productos)

    def registrar_usuario(
        self, identificacion: str, nombre: str, correo: str = ""
    ) -> bool:

        if self.buscar_usuario(identificacion) is not None:
            print(f"Ya existe un usuario con la identificación '{identificacion}'.")
            return False
        try:
            usuario = Usuario(identificacion=identificacion, nombre=nombre, correo=correo)
        except ValueError as error:
            print(f"No se pudo registrar el usuario: {error}")
            return False
        self._usuarios.append(usuario)
        self._indice_usuarios[usuario.identificacion] = usuario
        self._guardar_usuarios()
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:

        return self._indice_usuarios.get(identificacion)

    def listar_usuarios(self) -> list[Usuario]:

        return list(self._usuarios)

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str | None = None,
        correo: str | None = None,
    ) -> bool:

        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            print(f"No existe un usuario con la identificación '{identificacion}'.")
            return False
        try:
            if nombre is not None:
                usuario.nombre = nombre
            if correo is not None:
                usuario.correo = correo
        except ValueError as error:
            print(f"No se pudo actualizar el usuario: {error}")
            return False

        self._guardar_usuarios()
        return True

    def eliminar_usuario(self, identificacion: str) -> bool:

        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            print(f"No existe un usuario con la identificación '{identificacion}'.")
            return False
        self._usuarios.remove(usuario)
        del self._indice_usuarios[identificacion]
        self._guardar_usuarios()
        return True

    def _guardar_usuarios(self) -> None:
        ArchivoServicio.guardar_usuarios(self._usuarios)


    def vender_producto(
        self, codigo_producto: str, identificacion_usuario: str, cantidad: int
    ) -> bool:

        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        if usuario is None:
            print(f"No existe un usuario con la identificación '{identificacion_usuario}'.")
            return False
        if producto is None:
            print(f"No existe un producto con el código '{codigo_producto}'.")
            return False
        if cantidad <= 0:
            print("La cantidad solicitada debe ser mayor que cero.")
            return False
        if not producto.hay_stock_suficiente(cantidad):
            print(
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {producto.stock}, solicitado: {cantidad}."
            )
            return False

        try:
            venta = Venta(
                usuario_id=usuario.identificacion,
                producto_codigo=producto.codigo,
                cantidad=cantidad,
            )
        except ValueError as error:
            print(f"No se pudo registrar la venta: {error}")
            return False

        self._ventas.append(venta)
        self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)
        try:
            producto.vender(cantidad)
        except ValueError as error:
            self._ventas.remove(venta)
            self._ventas_por_usuario[venta.usuario_id].remove(venta)
            print(f"No se pudo registrar la venta: {error}")
            return False

        ArchivoServicio.guardar_ventas(self._ventas)
        self._guardar_productos()
        print(
            f"Venta registrada: {cantidad} x '{producto.nombre}' "
            f"para el usuario '{usuario.nombre}'."
        )
        return True

    def consultar_ventas_por_usuario(self, identificacion_usuario: str) -> list[Venta]:

        return list(self._ventas_por_usuario.get(identificacion_usuario, []))

    def listar_ventas(self) -> list[Venta]:

        return list(self._ventas)
