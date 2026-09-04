class Venta:

    def __init__(
        self,
        usuario_id: str,
        producto_codigo: str,
        cantidad: int,
    ) -> None:
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    @property
    def usuario_id(self) -> str:
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La venta debe estar asociada a un usuario válido.")
        self._usuario_id = valor.strip()

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La venta debe estar asociada a un producto válido.")
        self._producto_codigo = valor.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        try:
            valor_int = int(valor)
        except (TypeError, ValueError) as error:
            raise ValueError("La cantidad vendida debe ser un valor entero.") from error
        if valor_int <= 0:
            raise ValueError("La cantidad vendida debe ser mayor que cero.")
        self._cantidad = valor_int

    def convertir_a_diccionario(self) -> dict:

        return {
            "usuario_id": self._usuario_id,
            "producto_codigo": self._producto_codigo,
            "cantidad": self._cantidad,
        }

    @classmethod
    def crear_desde_diccionario(cls, datos: dict) -> "Venta":

        try:
            return cls(
                usuario_id=datos["usuario_id"],
                producto_codigo=datos["producto_codigo"],
                cantidad=datos["cantidad"],
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de venta no contiene la clave esperada: {error}"
            ) from error

    def __str__(self) -> str:
        return (
            f"Venta usuario={self._usuario_id} "
            f"producto={self._producto_codigo} cantidad={self._cantidad}"
        )

    def __repr__(self) -> str:
        return (
            f"Venta(usuario_id={self._usuario_id!r}, "
            f"producto_codigo={self._producto_codigo!r}, "
            f"cantidad={self._cantidad!r})"
        )
