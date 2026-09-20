from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    def __init__(
        self,
        productos_iniciales: list[Producto] | None = None,
        usuarios_iniciales: list[Usuario] | None = None,
        ventas_iniciales: list[Venta] | None = None,
    ) -> None:
        self._productos: list[Producto] = productos_iniciales.copy() if productos_iniciales else []
        self._usuarios: list[Usuario] = usuarios_iniciales.copy() if usuarios_iniciales else []
        self._ventas: list[Venta] = ventas_iniciales.copy() if ventas_iniciales else []

        self._productos_por_codigo: dict[str, Producto] = {}
        self._usuarios_por_identificacion: dict[str, Usuario] = {}
        self._ventas_por_usuario: dict[str, list[Venta]] = {}
        self._categorias: set[str] = set()

        self._reconstruir_indices()

    def _reconstruir_indices(self) -> None:
        self._productos_por_codigo = {}
        self._usuarios_por_identificacion = {}
        self._ventas_por_usuario = {}
        self._categorias = set()

        for producto in self._productos:
            self._productos_por_codigo[producto.codigo] = producto
            self._categorias.add(producto.categoria)

        for usuario in self._usuarios:
            self._usuarios_por_identificacion[usuario.identificacion] = usuario

        for venta in self._ventas:
            self._ventas_por_usuario.setdefault(venta.usuario_id, []).append(venta)

    def _reconstruir_indice_categorias(self) -> None:
        self._categorias = {producto.categoria for producto in self._productos}

    # ---------- Productos ----------
    def existe_codigo_producto(self, codigo: str) -> bool:
        return self.buscar_producto(codigo) is not None

    def registrar_producto(self, producto: Producto) -> bool:
        if self.buscar_producto(producto.codigo) is not None:
            return False

        self._productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        self._categorias.add(producto.categoria)
        return True

    def buscar_producto(self, codigo: str) -> Producto | None:
        codigo = codigo.strip()
        return self._productos_por_codigo.get(codigo)

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str | None = None,
        categoria: str | None = None,
        precio: float | None = None,
    ) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False

        producto.actualizar(
            nombre=nombre,
            categoria=categoria,
            precio=precio,
        )
        self._reconstruir_indice_categorias()
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False

        self._productos.remove(producto)
        self._productos_por_codigo.pop(producto.codigo, None)
        self._reconstruir_indice_categorias()
        return True

    def listar_productos(self) -> list[Producto]:
        return self._productos.copy()

    def obtener_categorias(self) -> set[str]:
        return self._categorias.copy()

    # ---------- Usuarios ----------
    def existe_identificacion_usuario(self, identificacion: str) -> bool:
        return self.buscar_usuario(identificacion) is not None

    def registrar_usuario(self, usuario: Usuario) -> bool:
        if self.buscar_usuario(usuario.identificacion) is not None:
            return False

        self._usuarios.append(usuario)
        self._usuarios_por_identificacion[usuario.identificacion] = usuario
        return True

    def buscar_usuario(self, identificacion: str) -> Usuario | None:
        identificacion = identificacion.strip()
        return self._usuarios_por_identificacion.get(identificacion)

    def actualizar_usuario(
        self,
        identificacion: str,
        nombre: str | None = None,
        correo: str | None = None,
    ) -> bool:
        # Operacion que faltaba: actualizar los datos de un usuario ya
        # registrado, siguiendo el mismo patron que actualizar_producto().
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False

        if nombre is not None and nombre.strip() != "":
            usuario.nombre = nombre
        if correo is not None and correo.strip() != "":
            usuario.correo = correo

        return True

    def usuario_tiene_ventas(self, identificacion: str) -> bool:
        identificacion = identificacion.strip()
        return len(self._ventas_por_usuario.get(identificacion, [])) > 0

    def eliminar_usuario(self, identificacion: str) -> bool:
        usuario = self.buscar_usuario(identificacion)
        if usuario is None:
            return False
        if self.usuario_tiene_ventas(usuario.identificacion):
            return False

        self._usuarios.remove(usuario)
        self._usuarios_por_identificacion.pop(usuario.identificacion, None)
        return True

    def listar_usuarios(self) -> list[Usuario]:
        return self._usuarios.copy()

    # ---------- Ventas ----------
    def vender_producto(
        self,
        codigo_producto: str,
        identificacion_usuario: str,
        cantidad: int,
    ) -> bool:
        usuario = self.buscar_usuario(identificacion_usuario)
        producto = self.buscar_producto(codigo_producto)

        # Reglas de negocio antes de crear la relacion.
        if usuario is None or producto is None:
            return False
        if cantidad <= 0 or producto.stock < cantidad:
            return False

        # Aqui se crea la relacion entre usuario y producto.
        venta = Venta(usuario.identificacion, producto.codigo, cantidad)
        self._ventas.append(venta)
        self._ventas_por_usuario.setdefault(usuario.identificacion, []).append(venta)
        # Y aqui se ve el cambio interno del producto: stock disminuye.
        producto.vender(cantidad)
        return True

    def listar_ventas(self) -> list[Venta]:
        return self._ventas.copy()

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> list[Venta]:
        identificacion_usuario = identificacion_usuario.strip()
        return self._ventas_por_usuario.get(identificacion_usuario, []).copy()