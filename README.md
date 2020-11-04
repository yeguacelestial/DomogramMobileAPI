# DomogramMobile - API

## Uso
Todas las responses tendrán la siguiente forma
```json
{
    "data": "Contenido de la response",
    "message": "Descripcion de lo que paso",
}
```

Las siguientes definiciones solo detallarán el valor esperado del campo `data`.

### Listar todos los dispositivos

**Definición**

`GET /dispositivos`

- `200 OK` on success
```json
[
    {
        "identificador": "luz-habitacion",
        "nombre": "Luz de habitacion",
        "tipo_dispositivo": "led",
        "pin_dispositivo": "10"
    },
    {
        "identificador": "temp-humedad",
        "nombre": "Temperatura y humedad",
        "tipo_dispositivo": "sensor",
        "pin_dispositivo": "A10"
    }
]
```

### Registrar un nuevo dispositivo

**Definición**

`POST /dispositivos`

**Argumentos**
- `"identificador:string"`, identificador globalmente único para este dispositivo
- `"nombre:string"`, un nombre amigable para este dispositivo
- `"tipo_dispositivo:string"`, el tipo de dispositivo entendido por el cliente
- `"pin_dispositivo:string"`, número de pin en microcontrolador (Uso sugerido: Arduino)

Si el dispositivo con el identificador asignado ya existe, será sobre-escrito.

**Response**
- `201 Created` on success
```json
{
    "identificador": "luz-habitacion",
    "nombre": "Luz de habitacion",
    "tipo_dispositivo": "led",
    "pin_dispositivo": "10"
}
```

### Ver detalles de dispositivos registrados

`GET /dispositivos/<identificador>`

**Response**
- `404 Not Found` si el dispositivo no existe
- `200 OK` on success

```json
{
    "identificador": "luz-habitacion",
    "nombre": "Luz de habitacion",
    "tipo_dispositivo": "led",
    "pin_dispositivo": "10"
}
```

## Eliminar un dispositivo

**Definición**

`DELETE /dispositivos/<identificador>`

**Response**
- `404 Not Found` si el dispositivo no existe
- `204 No Content` on success