# Sistema Restaurante — Semana 12

**Estudiante:** _Walter Ivan Flores Rivera_

Evolución del sistema de gestión de restaurante desarrollado en la
Semana 11 (productos con stock, usuarios, ventas y persistencia JSON).
Esta entrega **no se agrega funcionalidades nuevas**: solamente se mejora internamente
cómo el programa busca y consulta información, agregando índices en
memoria basados en `dict` para evitar recorrer listas completas cada
vez que se necesita un producto, un usuario o las ventas de un
usuario.

## Descripción general

El sistema permite registrar productos (con su stock disponible) y
usuarios, y realizar ventas que descuentan unidades del stock y quedan
registradas en una colección de ventas. Toda la información se guarda
en archivos JSON y se recupera automáticamente cada vez que el
programa se ejecuta.

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

## Mejoras de la Semana 12: búsquedas y consultas con colecciones

En la Semana 11, `buscar_producto`, `buscar_usuario` y
`consultar_ventas_por_usuario` recorrían la lista completa comparando
cada elemento hasta encontrar coincidencia (búsqueda O(n)). Esta
semana `servicios/restaurante.py` agrega **tres índices en memoria**
basados en `dict`, sin eliminar ninguna lista principal:

| Índice (dict) | Clave | Valor | Reemplaza a |
|---|---|---|---|
| `_indice_productos` | código del producto | objeto `Producto` | recorrido en `buscar_producto` |
| `_indice_usuarios` | identificación del usuario | objeto `Usuario` | recorrido en `buscar_usuario` |
| `_ventas_por_usuario` | identificación del usuario | lista de sus `Venta` | recorrido en `consultar_ventas_por_usuario` |

Las listas `_productos`, `_usuarios` y `_ventas` se conservan tal cual
estaban: siguen siendo las colecciones que se recorren para listar
todo (`listar_productos`, `listar_usuarios`, `listar_ventas`) y las
que se convierten a diccionarios y se guardan en JSON. Los índices son
una capa auxiliar de solo-lectura para acelerar las búsquedas por
clave; nunca reemplazan a los objetos `Producto`, `Usuario` o `Venta`.

**¿Por qué no se usó `set`?** En este proyecto no existe ninguna
operación que solo necesite saber si un valor pertenece a una
colección sin recuperar el objeto asociado. Las claves de los `dict`
ya cumplen esa función (`codigo in self._indice_productos` sería
equivalente a tener un `set` aparte), así que agregar un `set`
adicional solo duplicaría información sin aportar una mejora real.
Por eso se optó por no forzar su uso, siguiendo la recomendación de la
guía de no crear estructuras que el sistema nunca use.

### Sincronización de los índices

- **Al iniciar el programa**: `Restaurante.__init__` carga las listas
  desde JSON y llama a `_reconstruir_indices()`, que reconstruye los
  tres `dict` a partir de los objetos recién cargados.
- **Al registrar** un producto o usuario: se agrega tanto a la lista
  como al índice correspondiente.
- **Al actualizar** un producto o usuario: la clave del índice (código
  o identificación) no cambia, y el objeto se modifica en el mismo
  lugar de memoria, así que el índice queda coherente automáticamente.
- **Al eliminar** un producto o usuario: se elimina de la lista y con
  `del` también del índice.
- **Al vender un producto**: la nueva `Venta` se agrega a la lista
  `_ventas` y, en el mismo paso, a `_ventas_por_usuario` bajo la
  identificación del comprador. Si la venta debe revertirse (por
  ejemplo porque el descuento de stock falla), se quita de ambos
  lugares para que no queden desincronizados.

## Eliminación de la fecha en las ventas

A pedido explícito, se quitó por completo la marca de fecha/hora que
tenía `Venta` en la Semana 11 (`self.fecha = datetime.now()...`). La
clase `Venta` ahora solo registra `usuario_id`, `producto_codigo` y
`cantidad`; se eliminó el `import datetime`, el atributo `fecha`, su
inclusión en `convertir_a_diccionario()` / `crear_desde_diccionario()`
y su impresión en `main.py` y en `__str__`/`__repr__`. Los archivos
`datos/ventas.json` existentes también se actualizaron para no incluir
esa clave.

## Responsabilidad de los componentes

- **modelos/producto.py**: clase `Producto`. Valida código, nombre,
  precio y stock (nunca negativo). Sabe vender unidades de sí mismo
  (`vender`) y convertirse a/desde diccionario para JSON.
- **modelos/usuario.py**: clase `Usuario`. Valida identificación,
  nombre y correo. Se convierte a/desde diccionario para JSON.
- **modelos/venta.py**: clase `Venta`. Representa la relación entre un
  usuario y un producto vendido: `usuario_id`, `producto_codigo` y
  `cantidad` (sin fecha). Se convierte a/desde diccionario para JSON.
- **servicios/archivo_servicio.py**: clase `ArchivoServicio`. Centraliza
  la lectura y escritura de `productos.json`, `usuarios.json` y
  `ventas.json`, usando `json.load()` / `json.dump()` con `with open()`
  y codificación UTF-8. Maneja `FileNotFoundError`,
  `json.JSONDecodeError`, `PermissionError` y `KeyError` sin detener la
  aplicación.
- **servicios/restaurante.py**: clase `Restaurante`. Mantiene las
  colecciones de productos, usuarios y ventas en memoria (listas) junto
  con los índices auxiliares (`dict`) descritos arriba, ejecuta la
  lógica de negocio (registrar, buscar, actualizar, eliminar, vender,
  consultar) y delega la persistencia en `ArchivoServicio`.
- **main.py**: punto de entrada. Muestra el menú de consola y traduce
  cada opción en una llamada al servicio `Restaurante`; no administra
  colecciones ni índices directamente.

## Flujo de guardado y carga (sin cambios respecto a la Semana 11)

```
Objetos -> convertir_a_diccionario() -> lista de diccionarios -> json.dump() -> archivo JSON
archivo JSON -> json.load() -> diccionarios -> reconstrucción de objetos (crear_desde_diccionario)
```

Se guarda tras cada operación que modifique una colección, y al
guardar también se mantienen sincronizados los índices en memoria como
se explicó arriba. Al iniciar el programa, las tres colecciones se
recuperan desde JSON y los índices se reconstruyen inmediatamente
después.

## Excepciones controladas

`ArchivoServicio` maneja explícitamente:

- **FileNotFoundError**: si un archivo JSON todavía no existe, la
  colección correspondiente se inicia vacía.
- **json.JSONDecodeError**: si el archivo tiene contenido JSON
  inválido, se avisa y se inicia la colección vacía en lugar de
  detener la aplicación.
- **PermissionError**: si no hay permisos de lectura o escritura, se
  informa el problema sin interrumpir el programa.
- **KeyError**: si un registro JSON no contiene una clave esperada, ese
  registro se omite y se informa.
- **ValueError**: se mantiene en los modelos (`Producto`, `Usuario`,
  `Venta`) para validaciones propias (precios, stock, cantidades,
  campos vacíos, etc.).

## Instrucciones para ejecutar el programa

1. Ubicarse dentro de la carpeta `restaurante_app/`.
2. Ejecutar:
   ```bash
   python3 main.py
   ```
3. Usar el menú numerado para registrar/listar/actualizar/eliminar
   productos y usuarios, vender productos, consultar las ventas de un
   usuario o listar todas las ventas.
4. Seleccionar `0` para salir.

## Pruebas realizadas

1. Se ejecutó `main.py` cargando los datos existentes de
   `productos.json`, `usuarios.json` y `ventas.json`, confirmando que
   los índices quedaron disponibles desde el arranque.
2. Se buscó un producto por su código y un usuario por su
   identificación, verificando que la respuesta viene del índice
   (`_indice_productos` / `_indice_usuarios`).
3. Se consultaron las ventas de un usuario existente y se confirmó que
   la lista devuelta correspondía únicamente a sus ventas.
4. Se registró un producto y un usuario nuevos y se comprobó que
   aparecían de inmediato en las búsquedas por clave (índice
   actualizado en el mismo momento del registro).
5. Se realizó una venta válida: el stock del producto disminuyó
   correctamente, la venta se agregó a `_ventas_por_usuario` y quedó
   reflejada al instante en la consulta de ventas por usuario.
6. Se eliminó un producto y se verificó que una búsqueda posterior por
   su código ya no lo encontraba (índice sincronizado tras eliminar).
7. Se cerró el programa y se volvió a ejecutar, confirmando que
   productos, usuarios y ventas se recuperaron desde los archivos JSON
   y que los índices se reconstruyeron correctamente a partir de esos
   datos (las búsquedas y la consulta de ventas por usuario siguieron
   funcionando igual que antes de cerrar).