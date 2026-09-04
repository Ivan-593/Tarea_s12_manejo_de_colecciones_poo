from servicios.restaurante import Restaurante


def solicitar_texto(mensaje: str) -> str:
    return input(mensaje).strip()


def solicitar_entero(mensaje: str) -> int | None:
    texto = input(mensaje).strip()
    try:
        return int(texto)
    except ValueError:
        print("Debe ingresar un número entero válido.")
        return None


def solicitar_decimal(mensaje: str) -> float | None:
    texto = input(mensaje).strip()
    try:
        return float(texto)
    except ValueError:
        print("Debe ingresar un número válido.")
        return None


def menu_registrar_producto(restaurante: Restaurante) -> None:
    print("\n--- Registrar producto ---")
    codigo = solicitar_texto("Código del producto: ")
    nombre = solicitar_texto("Nombre del producto: ")
    precio = solicitar_decimal("Precio del producto: ")
    if precio is None:
        return
    stock = solicitar_entero("Stock inicial disponible: ")
    if stock is None:
        return
    if restaurante.registrar_producto(codigo, nombre, precio, stock):
        print("Producto registrado correctamente.")


def menu_listar_productos(restaurante: Restaurante) -> None:
    print("\n--- Productos registrados ---")
    productos = restaurante.listar_productos()
    if not productos:
        print("No hay productos registrados.")
        return
    for producto in productos:
        print(producto)


def menu_actualizar_producto(restaurante: Restaurante) -> None:
    print("\n--- Actualizar producto ---")
    codigo = solicitar_texto("Código del producto a actualizar: ")
    nombre = solicitar_texto("Nuevo nombre (Enter para mantener el actual): ")
    precio_texto = input("Nuevo precio (Enter para mantener el actual): ").strip()
    precio = None
    if precio_texto:
        try:
            precio = float(precio_texto)
        except ValueError:
            print("El precio ingresado no es válido. No se actualizará el precio.")
    if restaurante.actualizar_producto(
        codigo, nombre or None, precio
    ):
        print("Producto actualizado correctamente.")


def menu_eliminar_producto(restaurante: Restaurante) -> None:
    print("\n--- Eliminar producto ---")
    codigo = solicitar_texto("Código del producto a eliminar: ")
    if restaurante.eliminar_producto(codigo):
        print("Producto eliminado correctamente.")


def menu_registrar_usuario(restaurante: Restaurante) -> None:
    print("\n--- Registrar usuario ---")
    identificacion = solicitar_texto("Identificación del usuario: ")
    nombre = solicitar_texto("Nombre del usuario: ")
    correo = solicitar_texto("Correo del usuario (opcional): ")
    if restaurante.registrar_usuario(identificacion, nombre, correo):
        print("Usuario registrado correctamente.")


def menu_listar_usuarios(restaurante: Restaurante) -> None:
    print("\n--- Usuarios registrados ---")
    usuarios = restaurante.listar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for usuario in usuarios:
        print(usuario)


def menu_eliminar_usuario(restaurante: Restaurante) -> None:
    print("\n--- Eliminar usuario ---")
    identificacion = solicitar_texto("Identificación del usuario a eliminar: ")
    if restaurante.eliminar_usuario(identificacion):
        print("Usuario eliminado correctamente.")


def menu_vender_producto(restaurante: Restaurante) -> None:
    print("\n--- Vender producto ---")
    identificacion_usuario = solicitar_texto("Identificación del usuario: ")
    codigo_producto = solicitar_texto("Código del producto: ")
    cantidad = solicitar_entero("Cantidad a vender: ")
    if cantidad is None:
        return
    restaurante.vender_producto(codigo_producto, identificacion_usuario, cantidad)


def menu_consultar_ventas_usuario(restaurante: Restaurante) -> None:
    print("\n--- Ventas de un usuario ---")
    identificacion_usuario = solicitar_texto("Identificación del usuario: ")
    ventas = restaurante.consultar_ventas_por_usuario(identificacion_usuario)
    if not ventas:
        print("Este usuario no registra ventas.")
        return
    for venta in ventas:
        producto = restaurante.buscar_producto(venta.producto_codigo)
        nombre_producto = producto.nombre if producto else "(producto no encontrado)"
        print(
            f"- Producto: {venta.producto_codigo} "
            f"({nombre_producto}) | Cantidad: {venta.cantidad}"
        )


def menu_listar_ventas(restaurante: Restaurante) -> None:
    print("\n--- Todas las ventas registradas ---")
    ventas = restaurante.listar_ventas()
    if not ventas:
        print("No hay ventas registradas.")
        return
    for venta in ventas:
        print(venta)


def mostrar_menu() -> None:
    print("\n===== SISTEMA DE RESTAURANTE =====")
    print("1. Registrar producto")
    print("2. Listar productos")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Registrar usuario")
    print("6. Listar usuarios")
    print("7. Eliminar usuario")
    print("8. Vender producto")
    print("9. Consultar ventas de un usuario")
    print("10. Listar todas las ventas")
    print("0. Salir")


def main() -> None:
    restaurante = Restaurante()

    opciones = {
        "1": menu_registrar_producto,
        "2": menu_listar_productos,
        "3": menu_actualizar_producto,
        "4": menu_eliminar_producto,
        "5": menu_registrar_usuario,
        "6": menu_listar_usuarios,
        "7": menu_eliminar_usuario,
        "8": menu_vender_producto,
        "9": menu_consultar_ventas_usuario,
        "10": menu_listar_ventas,
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            print("Saliendo del sistema. ¡Hasta pronto!")
            break

        accion = opciones.get(opcion)
        if accion is None:
            print("Opción no válida. Intente nuevamente.")
            continue

        accion(restaurante)


if __name__ == "__main__":
    main()
