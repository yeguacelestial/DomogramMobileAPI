# DomogramMobile API

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
        "pin_dispositivo": "10",
        "parametros":{
            "encendido": false
        }
    },
    {
        "identificador": "temp-humedad",
        "nombre": "Temperatura y humedad",
        "tipo_dispositivo": "sensor",
        "pin_dispositivo": "A10",
        "parametros":{
            "temperatura": 25.0,
            "humedad": 50.0
        }
    }
]
```

### Registrar un nuevo dispositivo

**Definición**

`POST /dispositivos`

**Argumentos**
- `"identificador":string`, identificador globalmente único para este dispositivo
- `"nombre":string`, un nombre amigable para este dispositivo
- `"tipo_dispositivo":string`, el tipo de dispositivo entendido por el cliente
- `"pin_dispositivo":string`, número de pin en microcontrolador (Uso sugerido: Arduino)
- `"parametros":json`, objeto JSON con parámetros e información del dispositivo

Si el dispositivo con el identificador asignado ya existe, será sobre-escrito.

**Response**
- `201 Created` on success
```json
{
    "identificador": "luz-habitacion",
    "nombre": "Luz de habitacion",
    "tipo_dispositivo": "led",
    "pin_dispositivo": "10",
    "parametros": {
        "encendido": false
    }
}
```

### Ver detalles de dispositivos registrados

`GET /dispositivo/<identificador>`

**Response**
- `404 Not Found` si el dispositivo no existe
- `200 OK` on success

```json
{
    "identificador": "luz-habitacion",
    "nombre": "Luz de habitacion",
    "tipo_dispositivo": "led",
    "pin_dispositivo": "10",
    "parametros": {
        "encendido": false
    }
}
```

### Eliminar un dispositivo

**Definición**

`DELETE /dispositivo/<identificador>`

**Response**
- `404 Not Found` si el dispositivo no existe
- `204 No Content` on success

## Dispositivos a utilizar en el proyecto

### Iluminación - Ver las luces disponibles

**Definición**

`GET /dispositivo/luz-<sala>`

**Response**
- `200 OK` on success
- `404 Not Found` si el identificador no existe
```json
[
    {
        "identificador": "luz-habitacion",
        "nombre": "Luz de habitacion",
        "tipo_dispositivo": "led",
        "pin_dispositivo": "2",
        "parametros": {
            "encendido": false
        }
    },

    {
        "identificador": "luz-estancia",
        "nombre": "Luz de estancia",
        "tipo_dispositivo": "led",
        "pin_dispositivo": "3",
        "parametros": {
            "encendido": false
        }
    },

    {
        "identificador": "luz-baño",
        "nombre": "Luz de baño",
        "tipo_dispositivo": "led",
        "pin_dispositivo": "4",
        "parametros": {
            "encendido": false
        }
    },

    {
        "identificador": "luz-cocina",
        "nombre": "Luz de cocina",
        "tipo_dispositivo": "led",
        "pin_dispositivo": "5",
        "parametros": {
            "encendido": false
        }
    },

    {
        "identificador": "luz-entrada",
        "nombre": "Luz de entrada",
        "tipo_dispositivo": "led",
        "pin_dispositivo": "6",
        "parametros": {
            "encendido": false
        }
    },

    {
        "identificador": "luz-comedor",
        "nombre": "Luz de comedor",
        "tipo_dispositivo": "led",
        "pin_dispositivo": "7",
        "parametros": {
            "encendido": false
        }
    }
]
```

### Iluminación - Encender o apagar un led

**Definición**

`PUT /dispositivo/<identificador>`

**Argumentos**
- `"encendido":boolean`, indicar si el led del identificador estará encendido o apagado

**Response**
- `200 OK` on success
- `404 Not Found` si el identificador no existe

```json
[
    {
        "identificador": "luz-comedor",
        "nombre": "Luz de comedor",
        "tipo_dispositivo": "led",
        "pin_dispositivo": "7",
        "parametros": {
            "encendido": true
        }
    }
]
```


### Sensores - Temperatura y humedad

**Definición**

`GET /dispositivos/sensores/temp-y-humedad`

**Response**
- `200 OK` on success
- `404 Not Found` si el identificador no existe

```json
[
    {
        "identificador": "temp-y-humedad",
        "nombre": "Temperatura y humedad",
        "tipo_dispositivo": "sensor",
        "pin_dispositivo": "A0",
        "parametros": {
            "temperatura": 23.4,
            "humedad": 50.0
        }
    }
]
```

### Sensores - Ultrasónico

**Definición**

`GET /dispositivo/ultrasonico`

**Response**
- `200 OK` on success
- `404 Not Found` si el identificador no existe

```json
[
    {
        "identificador": "ultrasonico",
        "nombre": "Sensor ultrasónico",
        "tipo_dispositivo": "sensor",
        "pin_dispositivo": ["10", "11"],
        "parametros": {
            "distancia": 23.43,
        }
    }
]
```

### Servomotores - Ver estado

**Definición**

`GET /dispositivo/puertas`

**Response**
- `200 OK` on success
- `404 Not Found` si el identificador no existe

```json
[
    {
        "identificador": "puertas",
        "nombre": "Puertas principales",
        "tipo_dispositivo": "motor",
        "pin_dispositivo": "8",
        "parametros": {
            "dato_serial": "S",
            "abierto": false
        }
    }
]
```

### Servomotores - Abrir o cerrar

**Definición**

`PUT /dispositivo/puertas`

**Argumentos**
- `"abierto":boolean`, indica si el servomotor está abierto o cerrado. Estos motores están encargados de abrir y cerrar la casa, y ambos deben estar siempre en el mismo estado.
- `"parametros": {"dato_serial": "A"}`, gira los servomotores para abrir las puertas de la casa.
- `"parametros": {"dato_serial": "S"}`, gira los servomotores para cerrar las puertas de la casa.

**Response**
- `200 OK` on success
- `404 Not Found` si el identificador no existe

```json
[
    {
        "identificador": "puertas",
        "nombre": "Puertas principales",
        "tipo_dispositivo": "motor",
        "pin_dispositivo": "8",
        "parametros": {
            "dato_serial": "S",
            "abierto": false
        }
    }
]
```