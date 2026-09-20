from pathlib import Path
from typing import Callable, Dict, List, Tuple

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante import Restaurante


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================

OPCIONES_MENU: List[Tuple[str, str]] = [
    ("1", "Registrar producto"),
    ("2", "Buscar producto"),
    ("3", "Actualizar producto"),
    ("4", "Eliminar producto"),
    ("5", "Listar productos"),
    ("6", "Registrar usuario"),
    ("7", "Buscar usuario"),
    ("8", "Actualizar usuario"),
    ("9", "Eliminar usuario"),
    ("10", "Listar usuarios"),
    ("11", "Mostrar categorías"),
    ("12", "Vender producto"),
    ("13", "Consultar ventas de un usuario"),
    ("14", "Listar todas las ventas"),
    ("15", "Salir"),
]

SEPARADOR_DOBLE = "=" * 40
SEPARADOR_SIMPLE = "-" * 40


def mostrar_menu() -> None:
    print(SEPARADOR_DOBLE)
    print("        SISTEMA DE RESTAURANTE")
    print(SEPARADOR_DOBLE)

    for numero, descripcion in OPCIONES_MENU:

        if numero == "6":
            print(SEPARADOR_SIMPLE)

        if numero == "11":
            print(SEPARADOR_SIMPLE)

        if numero == "12":
            print(SEPARADOR_SIMPLE)

        if numero == "15":
            print(SEPARADOR_SIMPLE)

        print(f"{numero}. {descripcion}")

    print(SEPARADOR_SIMPLE)


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def leer_precio(mensaje: str) -> float:
    while True:
        entrada = input(mensaje).strip()

        try:
            precio = float(entrada)

            if precio < 0:
                print(
                    "El precio no puede ser negativo"
                    "Intentelo nuevamente."
                )
                continue

            return precio

        except ValueError:
            print(
                "Valor incorrecto. Ingrese un número válido, "
                "por ejemplo 5.50."
            )


def leer_entero(mensaje: str, valor_por_defecto: int = None) -> int:
    while True:
        entrada = input(mensaje).strip()

        if entrada == "" and valor_por_defecto is not None:
            return valor_por_defecto

        try:
            valor = int(entrada)

            if valor < 0:
                print(
                    "El valor no puede ser negativo. "
                    "Intentelo nuevamente."
                )
                continue

            return valor

        except ValueError:
            print(
                "Valor incorrecto. Ingrese un número entero, "
                "por ejemplo 10."
            )


def guardar_productos(archivo_servicio: ArchivoServicio, restaurante: Restaurante) -> None:
    guardado = archivo_servicio.guardar_productos(restaurante.listar_productos())
    if not guardado:
        print("Los cambios de productos no pudieron guardarse en el archivo.")


def guardar_usuarios(archivo_servicio: ArchivoServicio, restaurante: Restaurante) -> None:
    guardado = archivo_servicio.guardar_usuarios(restaurante.listar_usuarios())
    if not guardado:
        print("Los cambios de usuarios no pudieron guardarse en el archivo.")


def guardar_ventas(archivo_servicio: ArchivoServicio, restaurante: Restaurante) -> None:
    guardado = archivo_servicio.guardar_ventas(restaurante.listar_ventas())
    if not guardado:
        print("Los cambios de ventas no pudieron guardarse en el archivo.")


# ==========================================================
# OPCIÓN 1: REGISTRAR PRODUCTO
# ==========================================================

def opcion_registrar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio
) -> None:

    print("\n--- Registrar producto ---")

    codigo = input("Código: ").strip()
    nombre = input("Nombre: ").strip()
    categoria = input("Categoría: ").strip()
    precio = leer_precio("Precio: ")
    stock = leer_entero("Stock inicial: ", 0)

    try:
        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock,
        )

    except ValueError as error:
        print(f"No se pudo crear el producto: {error}")
        return

    if restaurante.registrar_producto(producto):
        print(
            f"Producto '{producto.nombre}' "
            "registrado correctamente."
        )
        guardar_productos(archivo_servicio, restaurante)
    else:
        print(
            f"Ya existe un producto con el código "
            f"'{producto.codigo}'."
        )


# ==========================================================
# OPCIÓN 2: BUSCAR PRODUCTO
# ==========================================================

def opcion_buscar_producto(
    restaurante: Restaurante
) -> None:

    print("\n--- Buscar producto ---")

    codigo = input("Código a buscar: ").strip()

    producto = restaurante.buscar_producto(codigo)

    if producto is not None:
        print("Producto encontrado:")
        print(producto)
    else:
        print(
            f"No se encontró ningún producto "
            f"con el código '{codigo}'."
        )


# ==========================================================
# OPCIÓN 3: ACTUALIZAR PRODUCTO
# ==========================================================

def opcion_actualizar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio
) -> None:

    print("\n--- Actualizar producto ---")

    codigo = input(
        "Código del producto a actualizar: "
    ).strip()

    if restaurante.buscar_producto(codigo) is None:
        print(
            f"No se encontró ningún producto "
            f"con el código '{codigo}'."
        )
        return

    print(
        "Deje el campo vacío si no desea modificarlo."
    )

    nombre = input("Nuevo nombre: ").strip()
    categoria = input("Nueva categoría: ").strip()
    entrada_precio = input("Nuevo precio: ").strip()

    precio = None

    if entrada_precio != "":
        try:
            precio = float(entrada_precio)

            if precio < 0:
                print(
                    "El precio no puede ser negativo."
                )
                return

        except ValueError:
            print(
                "Precio incorrecto. "
                "No se actualizará el precio."
            )
            precio = None

    try:
        actualizado = restaurante.actualizar_producto(
            codigo=codigo,
            nombre=nombre if nombre != "" else None,
            categoria=categoria
            if categoria != ""
            else None,
            precio=precio
        )

    except ValueError as error:
        print(
            f"No se pudo actualizar el producto: {error}"
        )
        return

    if actualizado:
        print("Producto actualizado correctamente.")
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("No se pudo actualizar el producto.")


# ==========================================================
# OPCIÓN 4: ELIMINAR PRODUCTO
# ==========================================================

def opcion_eliminar_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio
) -> None:

    print("\n--- Eliminar producto ---")

    codigo = input(
        "Código del producto a eliminar: "
    ).strip()

    if restaurante.eliminar_producto(codigo):
        print("Producto eliminado correctamente.")
        guardar_productos(archivo_servicio, restaurante)
    else:
        print(
            f"No se encontró ningún producto "
            f"con el código '{codigo}'."
        )


# ==========================================================
# OPCIÓN 5: LISTAR PRODUCTOS
# ==========================================================

def opcion_listar_productos(
    restaurante: Restaurante
) -> None:

    print("\n--- Listado de productos ---")

    productos = restaurante.listar_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    for producto in productos:
        print(producto)


# ==========================================================
# OPCIÓN 6: REGISTRAR USUARIO
# ==========================================================

def opcion_registrar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio
) -> None:

    print("\n--- Registrar usuario ---")

    identificacion = input(
        "Identificación: "
    ).strip()

    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()

    try:
        usuario = Usuario(
            identificacion=identificacion,
            nombre=nombre,
            correo=correo
        )

    except ValueError as error:
        print(
            f"No se pudo crear el usuario: {error}"
        )
        return

    if restaurante.registrar_usuario(usuario):
        print(
            f"Usuario '{usuario.nombre}' "
            "registrado correctamente."
        )
        guardar_usuarios(archivo_servicio, restaurante)
    else:
        print(
            f"Ya existe un usuario con la "
            f"identificación '{usuario.identificacion}'."
        )


# ==========================================================
# OPCIÓN 7: BUSCAR USUARIO
# ==========================================================

def opcion_buscar_usuario(
    restaurante: Restaurante
) -> None:

    print("\n--- Buscar usuario ---")

    identificacion = input(
        "Identificación a buscar: "
    ).strip()

    usuario = restaurante.buscar_usuario(identificacion)

    if usuario is not None:
        print("Usuario encontrado:")
        print(usuario)
    else:
        print(
            f"No se encontró ningún usuario "
            f"con la identificación '{identificacion}'."
        )


# ==========================================================
# OPCIÓN 8: ACTUALIZAR USUARIO
# ==========================================================

def opcion_actualizar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio
) -> None:

    print("\n--- Actualizar usuario ---")

    identificacion = input(
        "Identificación del usuario a actualizar: "
    ).strip()

    if restaurante.buscar_usuario(identificacion) is None:
        print(
            f"No se encontró ningún usuario "
            f"con la identificación '{identificacion}'."
        )
        return

    print(
        "Deje el campo vacío si no desea modificarlo."
    )

    nombre = input("Nuevo nombre: ").strip()
    correo = input("Nuevo correo: ").strip()

    try:
        actualizado = restaurante.actualizar_usuario(
            identificacion=identificacion,
            nombre=nombre if nombre != "" else None,
            correo=correo if correo != "" else None,
        )

    except ValueError as error:
        print(
            f"No se pudo actualizar el usuario: {error}"
        )
        return

    if actualizado:
        print("Usuario actualizado correctamente.")
        guardar_usuarios(archivo_servicio, restaurante)
    else:
        print("No se pudo actualizar el usuario.")


# ==========================================================
# OPCIÓN 9: ELIMINAR USUARIO
# ==========================================================

def opcion_eliminar_usuario(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio
) -> None:

    print("\n--- Eliminar usuario ---")

    identificacion = input(
        "Identificación del usuario a eliminar: "
    ).strip()

    if restaurante.buscar_usuario(identificacion) is None:
        print(
            f"No se encontró ningún usuario "
            f"con la identificación '{identificacion}'."
        )
        return

    if restaurante.usuario_tiene_ventas(identificacion):
        print(
            "No se puede eliminar: el usuario ya tiene ventas registradas."
        )
        return

    if restaurante.eliminar_usuario(identificacion):
        print("Usuario eliminado correctamente.")
        guardar_usuarios(archivo_servicio, restaurante)
    else:
        print("No se pudo eliminar el usuario.")


# ==========================================================
# OPCIÓN 10: LISTAR USUARIOS
# ==========================================================

def opcion_listar_usuarios(
    restaurante: Restaurante
) -> None:

    print("\n--- Listado de usuarios ---")

    usuarios = restaurante.listar_usuarios()

    if not usuarios:
        print("No hay usuarios registrados.")
        return

    for usuario in usuarios:
        print(usuario)


# ==========================================================
# OPCIÓN 11: MOSTRAR CATEGORÍAS
# ==========================================================

def opcion_mostrar_categorias(
    restaurante: Restaurante
) -> None:

    print("\n--- Categorías registradas ---")

    categorias = restaurante.obtener_categorias()

    if not categorias:
        print(
            "No hay categorías registradas todavía."
        )
        return

    for categoria in sorted(categorias):
        print(f"- {categoria}")


# ==========================================================
# OPCIÓN 12: VENDER PRODUCTO (MEJORA SEMANA 11)
# ==========================================================

def opcion_vender_producto(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio
) -> None:

    print("\n--- Vender producto ---")

    identificacion_usuario = input(
        "Identificación del usuario: "
    ).strip()

    usuario = restaurante.buscar_usuario(identificacion_usuario)
    if usuario is None:
        print(
            f"No se encontró ningún usuario "
            f"con la identificación '{identificacion_usuario}'."
        )
        return

    codigo_producto = input("Código del producto: ").strip()

    producto = restaurante.buscar_producto(codigo_producto)
    if producto is None:
        print(
            f"No se encontró ningún producto "
            f"con el código '{codigo_producto}'."
        )
        return

    cantidad = leer_entero("Cantidad a vender: ", 1)

    if cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        return

    if producto.stock < cantidad:
        print(
            f"No hay stock suficiente. "
            f"Stock disponible: {producto.stock}."
        )
        return

    vendido = restaurante.vender_producto(
        codigo_producto=codigo_producto,
        identificacion_usuario=identificacion_usuario,
        cantidad=cantidad,
    )

    if vendido:
        print(
            f"Venta registrada correctamente. "
            f"Stock actual de '{producto.nombre}': {producto.stock}."
        )
        guardar_ventas(archivo_servicio, restaurante)
        guardar_productos(archivo_servicio, restaurante)
    else:
        print("No fue posible realizar la venta.")


# ==========================================================
# OPCIÓN 13: CONSULTAR VENTAS DE UN USUARIO (MEJORA SEMANA 11)
# ==========================================================

def opcion_consultar_ventas_usuario(
    restaurante: Restaurante
) -> None:

    print("\n--- Consultar ventas de un usuario ---")

    identificacion_usuario = input(
        "Identificación del usuario: "
    ).strip()

    usuario = restaurante.buscar_usuario(identificacion_usuario)
    if usuario is None:
        print(
            f"No se encontró ningún usuario "
            f"con la identificación '{identificacion_usuario}'."
        )
        return

    ventas = restaurante.consultar_ventas_usuario(identificacion_usuario)

    print(f"\nVentas de {usuario.nombre}:")

    if not ventas:
        print("- Sin ventas registradas.")
        return

    for venta in ventas:
        producto = restaurante.buscar_producto(venta.producto_codigo)
        nombre_producto = producto.nombre if producto is not None else "Producto no encontrado"
        print(
            f"- {venta.producto_codigo} | {nombre_producto} | "
            f"Cantidad: {venta.cantidad}"
        )


# ==========================================================
# OPCIÓN 14: LISTAR TODAS LAS VENTAS (MEJORA SEMANA 11)
# ==========================================================

def opcion_listar_ventas(
    restaurante: Restaurante
) -> None:

    print("\n--- Listado de ventas ---")

    ventas = restaurante.listar_ventas()

    if not ventas:
        print("No hay ventas registradas.")
        return

    for venta in ventas:
        print(venta)


# ==========================================================
# OPCIÓN 15: SALIR
# ==========================================================

def opcion_salir() -> None:
    print(
        "\nGracias por utilizar el sistema "
        "de restaurante. ¡Hasta pronto!"
    )


# ==========================================================
# ACCIONES DEL MENÚ
# ==========================================================

def construir_acciones_menu(
    restaurante: Restaurante,
    archivo_servicio: ArchivoServicio
) -> Dict[str, Callable[[], None]]:

    return {
        "1": lambda: opcion_registrar_producto(restaurante, archivo_servicio),
        "2": lambda: opcion_buscar_producto(restaurante),
        "3": lambda: opcion_actualizar_producto(restaurante, archivo_servicio),
        "4": lambda: opcion_eliminar_producto(restaurante, archivo_servicio),
        "5": lambda: opcion_listar_productos(restaurante),
        "6": lambda: opcion_registrar_usuario(restaurante, archivo_servicio),
        "7": lambda: opcion_buscar_usuario(restaurante),
        "8": lambda: opcion_actualizar_usuario(restaurante, archivo_servicio),
        "9": lambda: opcion_eliminar_usuario(restaurante, archivo_servicio),
        "10": lambda: opcion_listar_usuarios(restaurante),
        "11": lambda: opcion_mostrar_categorias(restaurante),
        "12": lambda: opcion_vender_producto(restaurante, archivo_servicio),
        "13": lambda: opcion_consultar_ventas_usuario(restaurante),
        "14": lambda: opcion_listar_ventas(restaurante),
        "15": lambda: opcion_salir(),
    }


# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================

def main() -> None:

    ruta_datos = Path(__file__).resolve().parent / "datos"
    archivo_servicio = ArchivoServicio(str(ruta_datos))

    productos_iniciales = archivo_servicio.cargar_productos()
    usuarios_iniciales = archivo_servicio.cargar_usuarios()
    ventas_iniciales = archivo_servicio.cargar_ventas()

    restaurante = Restaurante(
        productos_iniciales,
        usuarios_iniciales,
        ventas_iniciales,
    )

    acciones = construir_acciones_menu(restaurante, archivo_servicio)

    while True:

        mostrar_menu()

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        accion = acciones.get(opcion)

        if accion is None:
            print(
                "Opción inválida. "
                "Intente nuevamente."
            )
            continue

        accion()

        if opcion == "15":
            break


if __name__ == "__main__":
    main()