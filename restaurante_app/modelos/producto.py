class Producto:
    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int = 0,
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        # MEJORA SEMANA 11: se agrega el atributo stock, validado para que
        # nunca quede en un valor negativo.
        self.stock = stock

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El código no puede estar vacío.")
        self._codigo = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La categoría no puede estar vacía.")
        self._categoria = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        try:
            precio_convertido = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser un valor numérico.")
        if precio_convertido < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = precio_convertido

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        # MEJORA SEMANA 11: el stock siempre debe ser un entero valido y no negativo.
        try:
            stock_convertido = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser un valor numérico entero.")
        if stock_convertido < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = stock_convertido

    def actualizar(
        self,
        nombre: str = None,
        categoria: str = None,
        precio: float = None,
    ) -> None:
        if nombre is not None and nombre.strip() != "":
            self.nombre = nombre
        if categoria is not None and categoria.strip() != "":
            self.categoria = categoria
        if precio is not None:
            self.precio = precio

    def vender(self, cantidad: int) -> None:
        # MEJORA SEMANA 11: descuenta stock solo si la cantidad es valida
        # y hay stock suficiente disponible.
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        if cantidad > self._stock:
            raise ValueError("No hay stock suficiente para realizar la venta.")
        self._stock -= cantidad

    def convertir_a_diccionario(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    def __str__(self) -> str:
        return (
            f"Código: {self.codigo} | Nombre: {self.nombre} | "
            f"Categoría: {self.categoria} | Precio: ${self.precio:.2f} | "
            f"Stock: {self.stock}"
        )