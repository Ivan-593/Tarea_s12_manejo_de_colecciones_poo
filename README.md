# Sistema Restaurante — Semana 12

**Estudiante:** _Walter Ivan Flores Rivera_

Evolución del sistema de gestión de restaurante desarrollado en la
Semana 11 (productos con stock, usuarios, ventas y persistencia JSON).
El objetivo de esta entrega es mejorar internamente cómo el programa
busca y consulta información usando colecciones de Python: **índices
en memoria basados en `dict`** (para no recorrer listas completas cada
vez que se necesita un producto, un usuario o las ventas de un
usuario) y un **`set`** para manejar categorías únicas. La lógica de
negocio de la Semana 11 no cambia; lo único que el usuario ve como
novedad es la opción **11. Mostrar categorías** del menú.

## Descripción general

El sistema permite registrar productos (con su categoría, precio y
stock disponible) y usuarios, y realizar ventas que descuentan unidades
del stock y quedan registradas en una colección de ventas. Toda la
información se guarda en archivos JSON y se recupera automáticamente
cada vez que el programa se ejecuta. El programa se maneja desde un
menú de consola con 15 opciones (ver la sección _Menú de opciones_).

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante.py
├── main.py
└── README.md
```

Los archivos de `datos/` incluyen información de ejemplo: 3 productos
(`P001` a `P003`), 3 usuarios y 1 venta.

## Menú de opciones

| N.º | Opción | N.º | Opción |
|---|---|---|---|
| 1 | Registrar producto | 9 | Eliminar usuario |
| 2 | Buscar producto | 10 | Listar usuarios |
| 3 | Actualizar producto | 11 | Mostrar categorías |
| 4 | Eliminar producto | 12 | Vender producto |
| 5 | Listar productos | 13 | Consultar ventas de un usuario |
| 6 | Registrar usuario | 14 | Listar todas las ventas |
| 7 | Buscar usuario | 15 | Salir |
| 8 | Actualizar usuario | | |

## Mejoras de la Semana 12: búsquedas y consultas con colecciones

En la Semana 11, `buscar_producto`, `buscar_usuario` y
`consultar_ventas_usuario` recorrían la lista completa comparando cada
elemento hasta encontrar coincidencia (búsqueda O(n)). Esta semana
`servicios/restaurante.py` agrega **tres índices en memoria basados en
`dict` y un `set`**, sin eliminar ninguna lista principal:

| Estructura | Tipo | Clave | Valor | Se usa en |
|---|---|---|---|---|
| `_productos_por_codigo` | `dict` | código del producto | objeto `Producto` | `buscar_producto` (y, a través de ella, `existe_codigo_producto`, `registrar_producto`, `actualizar_producto`, `eliminar_producto` y `vender_producto`) |
| `_usuarios_por_identificacion` | `dict` | identificación del usuario | objeto `Usuario` | `buscar_usuario` (y, a través de ella, `existe_identificacion_usuario`, `registrar_usuario`, `actualizar_usuario`, `eliminar_usuario` y `vender_producto`) |
| `_ventas_por_usuario` | `dict` | identificación del usuario | lista de sus `Venta` | `consultar_ventas_usuario` y `usuario_tiene_ventas` |
| `_categorias` | `set` | — | texto de la categoría | `obtener_categorias` (opción 11 del menú) |

Las listas `_productos`, `_usuarios` y `_ventas` se conservan tal cual
estaban: siguen siendo las colecciones que se recorren para listar
todo (`listar_productos`, `listar_usuarios`, `listar_ventas`) y las
que se convierten a diccionarios y se guardan en JSON. Los índices y el
`set` son una capa auxiliar para acelerar las consultas; nunca
reemplazan a los objetos `Producto`, `Usuario` o `Venta`: los `dict`
guardan referencias a los mismos objetos que están en las listas, no
copias.

Además:

- `buscar_producto` y `buscar_usuario` aplican `strip()` a la clave
  antes de consultar el `dict`, por lo que `" P001 "` y `"P001"`
  encuentran el mismo producto.
- `registrar_producto` y `registrar_usuario` usan esas búsquedas por
  clave para detectar duplicados sin recorrer la lista.
- `listar_productos`, `listar_usuarios`, `listar_ventas`,
  `obtener_categorias` y `consultar_ventas_usuario` devuelven **copias**
  (`.copy()`), de modo que quien las reciba no pueda modificar por
  accidente las colecciones internas del servicio.

**¿Por qué se usa un `set` para las categorías?** Muchos productos
pueden compartir la misma categoría (por ejemplo, varias bebidas). Un
`set` garantiza por sí mismo que cada categoría aparezca una sola vez,
sin tener que revisar manualmente si ya estaba en una lista.
`obtener_categorias()` devuelve una copia del `set` y el menú la
muestra ordenada alfabéticamente. En cambio, no se creó un `set` para
comprobar si un código o una identificación existen: las claves de los
`dict` ya cumplen esa función (`codigo in self._productos_por_codigo`
sería equivalente a tener un `set` aparte), y duplicar esa información
no aportaría ninguna mejora.

### Sincronización de los índices

- **Al iniciar el programa**: `main.py` lee los tres archivos JSON con
  `ArchivoServicio` y pasa las listas resultantes al constructor de
  `Restaurante`. `Restaurante.__init__` copia esas listas y llama a
  `_reconstruir_indices()`, que reconstruye los tres `dict` y el `set`
  de categorías a partir de los objetos recién cargados.
- **Al registrar** un producto: se agrega a la lista `_productos`, al
  índice `_productos_por_codigo` y su categoría al `set`. Al registrar
  un usuario: se agrega a la lista `_usuarios` y al índice
  `_usuarios_por_identificacion`. Si el código o la identificación ya
  existen, el registro se rechaza y ninguna estructura cambia.
- **Al actualizar** un producto o usuario: la clave del índice (código
  o identificación) no se puede modificar y el objeto se cambia en el
  mismo lugar de memoria, así que los `dict` quedan coherentes
  automáticamente. La única excepción es la categoría de un producto:
  como un `set` no sabe cuántos productos siguen usando una categoría,
  después de actualizar un producto se llama a
  `_reconstruir_indice_categorias()`, que recalcula el `set` a partir
  de los productos existentes (así, una categoría deja de aparecer si
  ya ningún producto la usa).
- **Al eliminar un producto**: se quita de la lista con `remove()`,
  del índice con `pop()` y se recalcula el `set` de categorías. La
  eliminación de un producto no se bloquea aunque tenga ventas; esas
  ventas se conservan y, al consultarlas, `main.py` muestra "Producto
  no encontrado" en lugar del nombre.
- **Al eliminar un usuario**: primero se comprueba con
  `usuario_tiene_ventas` (que consulta `_ventas_por_usuario`); si el
  usuario tiene ventas registradas, la eliminación se rechaza. Así
  nunca quedan ventas de un usuario que ya no existe y el índice
  `_ventas_por_usuario` no necesita limpieza al eliminar. Si no tiene
  ventas, se quita de la lista con `remove()` y del índice con `pop()`.
- **Al vender un producto**: `vender_producto` valida primero que el
  usuario exista, que el producto exista, que la cantidad sea mayor
  que cero y que haya stock suficiente. Solo entonces crea la `Venta`,
  la agrega a la lista `_ventas` y, en el mismo paso, a
  `_ventas_por_usuario` bajo la identificación del comprador, y
  finalmente descuenta el stock con `Producto.vender`. Como todas las
  validaciones se hacen antes de modificar algo, no puede quedar una
  venta registrada sin su descuento de stock, y por eso no hace falta
  un mecanismo de reversión.

## Eliminación de la fecha en las ventas

A pedido explícito, se quitó por completo la marca de fecha/hora que
tenía `Venta` en la Semana 11 (`self.fecha = datetime.now()...`). La
clase `Venta` ahora solo registra `usuario_id`, `producto_codigo` y
`cantidad`; se eliminó el `import datetime`, el atributo `fecha`, su
inclusión en `convertir_a_diccionario()`, su lectura en
`ArchivoServicio.cargar_ventas()` y su impresión en `main.py` y en
`__str__`. Los archivos `datos/ventas.json` existentes también se
actualizaron para no incluir esa clave.

## Responsabilidad de los componentes

- **modelos/producto.py**: clase `Producto` (código, nombre, categoría,
  precio y stock). Valida cada campo con `property` y `setter`: los
  textos no pueden estar vacíos, el precio debe ser numérico y no
  negativo, y el stock debe ser un entero nunca negativo. Sabe
  actualizarse (`actualizar`), vender unidades de sí mismo (`vender`,
  que rechaza cantidades no positivas o mayores que el stock) y
  convertirse a diccionario para JSON (`convertir_a_diccionario`).
- **modelos/usuario.py**: clase `Usuario` (identificación, nombre y
  correo). Valida que los campos no estén vacíos y que el correo
  contenga `@`. Se convierte a diccionario para JSON.
- **modelos/venta.py**: clase `Venta`. Representa la relación entre un
  usuario y un producto vendido: `usuario_id`, `producto_codigo` y
  `cantidad` (entero mayor que cero, sin fecha). Se convierte a
  diccionario para JSON.
- **servicios/archivo_servicio.py**: clase `ArchivoServicio`. Centraliza
  la lectura y escritura de `productos.json`, `usuarios.json` y
  `ventas.json` (`cargar_*` / `guardar_*`), usando `json.load()` /
  `json.dump()` con `with open()` y codificación UTF-8. Al cargar,
  reconstruye los objetos llamando directamente a los constructores de
  `Producto`, `Usuario` y `Venta`, por lo que los datos leídos también
  pasan por las validaciones de los modelos. Maneja `FileNotFoundError`,
  `json.JSONDecodeError`, `PermissionError` y `KeyError` sin detener la
  aplicación.
- **servicios/restaurante.py**: clase `Restaurante`. Mantiene las
  colecciones de productos, usuarios y ventas en memoria (listas) junto
  con los índices auxiliares (`dict`) y el `set` de categorías
  descritos arriba, y ejecuta la lógica de negocio (registrar, buscar,
  actualizar, eliminar, vender, consultar). No lee ni escribe archivos:
  recibe las listas ya cargadas al crearse y expone los métodos
  `listar_*` para que otra capa las guarde.
- **main.py**: punto de entrada. Al iniciar, carga los datos con
  `ArchivoServicio` y crea el `Restaurante`. Muestra el menú de
  consola, pide y valida los datos ingresados por el usuario
  (`leer_precio`, `leer_entero`), traduce cada opción en una llamada al
  servicio `Restaurante` y, después de cada operación que modifica una
  colección, pide a `ArchivoServicio` que la guarde. No administra
  colecciones ni índices directamente.

## Flujo de guardado y carga

```
Objetos -> convertir_a_diccionario() -> lista de diccionarios -> json.dump() -> archivo JSON
archivo JSON -> json.load() -> diccionarios -> constructores Producto/Usuario/Venta (con validación) -> objetos
objetos -> Restaurante(...) -> _reconstruir_indices() -> dict y set en memoria
```

Se guarda tras cada operación que modifique una colección:

| Operación | Archivos que se guardan |
|---|---|
| Registrar, actualizar o eliminar producto | `productos.json` |
| Registrar, actualizar o eliminar usuario | `usuarios.json` |
| Vender producto | `ventas.json` y `productos.json` (el stock cambió) |

Los índices en memoria se mantienen sincronizados dentro de
`Restaurante` en el momento de cada operación (ver la sección anterior);
no dependen del guardado. Al iniciar el programa, las tres colecciones
se recuperan desde JSON y los índices y el `set` se reconstruyen
inmediatamente después.

## Excepciones controladas

`ArchivoServicio` maneja explícitamente:

- **FileNotFoundError**: si un archivo JSON todavía no existe, la
  colección correspondiente se inicia vacía.
- **json.JSONDecodeError**: si el archivo tiene contenido JSON
  inválido, se avisa y se inicia la colección vacía en lugar de
  detener la aplicación.
- **PermissionError**: si no hay permisos de lectura o escritura, se
  informa el problema sin interrumpir el programa. Los métodos
  `guardar_*` devuelven `True` o `False`, y `main.py` avisa al usuario
  cuando un guardado no se pudo realizar.
- **KeyError**: si un registro JSON no contiene una clave esperada, ese
  registro se omite y se informa. (En productos, `stock` es opcional:
  si falta, se asume 0.)
- **ValueError**: si un registro tiene datos inválidos (por ejemplo,
  una cantidad negativa), ese registro se omite y se informa.

Además, si el archivo no contiene una lista, o si algún elemento de la
lista no es un objeto JSON, se avisa y se omite (o se inicia la
colección vacía) sin detener el programa.

`ValueError` también se mantiene en los modelos (`Producto`, `Usuario`,
`Venta`) para validaciones propias (precios, stock, cantidades, campos
vacíos, correo sin `@`, etc.), y `main.py` la captura al crear o
actualizar objetos para mostrar el mensaje al usuario.

## Instrucciones para ejecutar el programa

Requiere **Python 3.10 o superior** (el código usa anotaciones como
`list[Producto] | None`).

1. Ubicarse dentro de la carpeta `restaurante_app/`.
2. Ejecutar:
   ```bash
   python3 main.py
   ```
3. Usar el menú numerado para registrar, buscar, listar, actualizar y
   eliminar productos y usuarios (opciones 1 a 10), mostrar las
   categorías (11), vender productos (12), consultar las ventas de un
   usuario (13) o listar todas las ventas (14).
4. Seleccionar `15` para salir.

## Pruebas realizadas

1. Se ejecutó `main.py` cargando los datos existentes de
   `productos.json`, `usuarios.json` y `ventas.json`, confirmando que
   los índices y el `set` de categorías quedaron disponibles desde el
   arranque (la opción 11 mostró `Bebida`, `Plato fuerte` y
   `Tradicional`).
2. Se buscó un producto por su código y un usuario por su
   identificación, verificando que la respuesta viene del índice
   (`_productos_por_codigo` / `_usuarios_por_identificacion`), que el
   objeto devuelto es el mismo que está en la lista y que la búsqueda
   funciona aunque la clave lleve espacios al inicio o al final.
3. Se consultaron las ventas de un usuario con ventas y de un usuario
   sin ventas, y se confirmó que la lista devuelta correspondía
   únicamente a sus ventas (vacía en el segundo caso).
4. Se registró un producto con una categoría nueva y se comprobó que
   aparecía de inmediato en la búsqueda por código y que la categoría
   aparecía en el `set`. Se intentó registrar un código ya existente y
   fue rechazado sin modificar ninguna colección.
5. Se actualizó la categoría de ese producto a una ya existente y se
   verificó que la categoría anterior desapareció del `set`, porque
   ningún otro producto la usaba.
6. Se realizó una venta válida: el stock del producto disminuyó
   correctamente, la venta se agregó a `_ventas` y a
   `_ventas_por_usuario` y quedó reflejada al instante en la consulta
   de ventas por usuario.
7. Se intentaron ventas inválidas (stock insuficiente, usuario
   inexistente, producto inexistente y cantidad cero): todas fueron
   rechazadas y ni el stock ni las ventas cambiaron.
8. Se intentó eliminar un usuario con ventas y fue rechazado; se
   eliminó un usuario sin ventas y una búsqueda posterior ya no lo
   encontraba.
9. Se eliminó un producto y se verificó que una búsqueda posterior por
   su código ya no lo encontraba y que su categoría salió del `set`
   cuando ya ningún producto la usaba.
10. Se comprobó la coherencia entre listas e índices: cada producto y
    cada usuario de las listas estaba en su `dict` (con el mismo
    objeto) y la cantidad total de ventas en `_ventas_por_usuario`
    coincidía con la de `_ventas`.
11. Se cerró el programa y se volvió a ejecutar, confirmando que
    productos, usuarios y ventas se recuperaron desde los archivos JSON
    y que los índices y las categorías se reconstruyeron correctamente
    a partir de esos datos (las búsquedas, la consulta de ventas por
    usuario y la opción 11 siguieron funcionando igual que antes de
    cerrar).
12. Se probaron archivos dañados (JSON inválido, registros incompletos
    o que no son objetos, cantidad negativa en una venta y archivos
    inexistentes): el programa mostró el aviso correspondiente,
    omitió los registros inválidos y siguió funcionando.