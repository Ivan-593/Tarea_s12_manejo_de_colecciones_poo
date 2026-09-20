class Usuario:
    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La identificación no puede estar vacía.")
        self._identificacion = valor.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El correo no puede estar vacío.")
        if "@" not in valor:
            raise ValueError("El correo debe tener un formato válido (debe contener '@').")
        self._correo = valor.strip()

    def convertir_a_diccionario(self) -> dict:

        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    def __str__(self) -> str:
        return f"Identificación: {self.identificacion} | Nombre: {self.nombre} | Correo: {self.correo}"