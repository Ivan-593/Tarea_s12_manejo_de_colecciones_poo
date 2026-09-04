
class Usuario:

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str = "",
    ) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        valor = (valor or "").strip()
        if valor and "@" not in valor:
            raise ValueError("El correo del usuario no tiene un formato válido.")
        self._correo = valor

    def convertir_a_diccionario(self) -> dict:

        return {
            "identificacion": self._identificacion,
            "nombre": self._nombre,
            "correo": self._correo,
        }

    @classmethod
    def crear_desde_diccionario(cls, datos: dict) -> "Usuario":

        try:
            return cls(
                identificacion=datos["identificacion"],
                nombre=datos["nombre"],
                correo=datos.get("correo", ""),
            )
        except KeyError as error:
            raise KeyError(
                f"El registro de usuario no contiene la clave esperada: {error}"
            ) from error

    def __str__(self) -> str:
        correo = f" ({self._correo})" if self._correo else ""
        return f"[{self._identificacion}] {self._nombre}{correo}"

    def __repr__(self) -> str:
        return (
            f"Usuario(identificacion={self._identificacion!r}, "
            f"nombre={self._nombre!r}, correo={self._correo!r})"
        )