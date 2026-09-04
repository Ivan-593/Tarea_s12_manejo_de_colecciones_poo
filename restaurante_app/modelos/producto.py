class Producto:


    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int = 0,
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            valor_float = float(valor)
        except (TypeError, ValueError) as error:
            raise ValueError("El precio debe ser un valor numérico.") from error
        if valor_float <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = valor_float

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        try:
            valor_int = int(valor)
        except (TypeError, ValueError) as error:
            raise ValueError("El stock debe ser un valor entero.") from error
        if valor_int < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        self._stock = valor_int

    def hay_stock_suficiente(self, cantidad: int) -> bool:

        return cantidad > 0 and self._stock >= cantidad

    def vender(self, cantidad: int) -> None:

        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        if cantidad > self._stock:
            raise ValueError("No hay stock suficiente para realizar la venta.")
        self._stock -= cantidad

    def reponer_stock(self, cantidad: int) -> None:

        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor que cero.")
        self._stock += cantidad


    def convertir_a_diccionario(self) -> dict:

        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "precio": self._precio,
            "stock": self._stock,
        }

    @classmethod
    def crear_desde_diccionario(cls, datos: dict) -> "Producto":

        try:
            return cls(
                codigo=datos["codigo"],
                nombre=datos["nombre"],
                precio=datos["precio"],
                stock=datos.get("stock", 0),
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de producto no contiene la clave esperada: {error}"
            ) from error

    def __str__(self) -> str:
        return (
            f"[{self._codigo}] {self._nombre} - ${self._precio:.2f} "
            f"(stock: {self._stock})"
        )

    def __repr__(self) -> str:
        return (
            f"Producto(codigo={self._codigo!r}, nombre={self._nombre!r}, "
            f"precio={self._precio!r}, stock={self._stock!r})"
        )
