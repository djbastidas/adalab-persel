# Prueba _escrita_ – Laboratorio de Ciencia de Datos - Proceso de Selección de un Técnico de Investigación 

## Objetivo

El objetivo de esta evaluación es analizar la capacidad del postulante para desarrollar un flujo completo de trabajo en ciencia de datos, desde el procesamiento de datos hasta el despliegue de un modelo como servicio.

Se evaluarán competencias en:

- Procesamiento y análisis de datos
- Modelado de Machine Learning
- Desarrollo de software
- Despliegue de servicios (API)
- Documentación y reproducibilidad

---

## Dataset

El dataset proporcionado corresponde a información de alquileres de bienes inmuebles en Ecuador.

El objetivo es predecir el precio de alquiler de un inmueble a partir de las siguientes variables:

- Provincia
- Número de dormitorios
- Número de baños
- Área
- Número de garajes

El dataset se encuentra en la carpeta `/data`.

---

## Tareas a realizar

### 1. Procesamiento y análisis de datos

- Cargar el dataset
- Realizar limpieza y normalización de datos para la columna `Lugar`
- Manejar valores faltantes
- Realizar análisis descriptivo:
  - Total de propiedades, por Provincia, y por Lugar 
  - Cálculo de mediana y promedio de precio de alquiler (General y por Lugar)
  - Análisis de la relación entre Área y Precio
  - Análisis de Premium por Habitación Adicional: Diferencia del precio promedio entre
propiedades de 1 habitación vs. 2 habitaciones; 2 habitaciones vs. 3, 3 vs. 4, etc.
  - Otros análisis que se consideren relevantes
- Crear una nueva columna: Tipo de Precio **por Lugar** 
  - Si precio < Q1 (Cuartil 1) -> "Económico"
  - Si precio > Q3 (Cuartil 3) -> "Lujo"
  - Resto -> "Medio"

#### Entregable:
- Un notebook (`.ipynb`) **publicado en Github** que contenga el análisis exploratorio

---

### 2. Modelado de Machine Learning

- Construir un modelo de regresión para predecir el precio de alquiler
- Utilizar como variables de entrada:
  - Provincia
  - Lugar
  - Número de dormitorios
  - Número de baños
  - Área
  - Número de garajes
- Justificar la elección del modelo
- Evaluar su desempeño utilizando métricas adecuadas

#### Entregable:
- Un notebook (`.ipynb`) **publicado en Github** que contenga la construcción del modelo de regresión
- Modelo serializado **publicado en Github**

---

### 3. Desarrollo y Despliegue de API

El modelo de regresión debe ser expuesto mediante una API REST.

#### Requisitos mínimos

**Endpoint:**

POST /predict

**Entrada (JSON):**
```json
{
  "provincia": "Pichincha",
  "lugar": "Quito",
  "num_dormitorios": 3,
  "num_banos": 2,
  "area": 120,
  "num_garages": 1
}
```

**Salida (JSON):**
```json
{
  "prediction": 750.0
}
```

#### Despliegue

La API debe estar desplegada y accesible públicamente.

#### Requisitos:

* Debe poder ser consumida desde herramientas como Postman o `curl` a través de internet mediante una URL pública funcional

#### Nota:
Puede utilizar cualquier plataforma de despliegue (Render, Railway, Fly.io, etc.).

---

## Entregables

El postulante deberá entregar:

Repositorio GitHub con:

* Notebook de análisis de datos (1. Procesamiento y análisis de datos)
* Notebook de modelado de regresión (2. Modelado de Machine Learning)
* URL pública de la API
* README con:
  * Instrucciones de uso de la API 
  * Descripción de la solución 
  * Ejemplo de request

---

### Opcional (Bonus)

* Implementación de una interfaz (frontend o dashboard)
* Uso de Docker
* Configuración avanzada del despliegue
* Buenas prácticas de ingeniería (testing, modularidad, etc.)

---

## Criterios de evaluación

| Criterio                                | Peso |
|-----------------------------------------|------|
| Administración del entorno / despliegue | 30%  |
| Modelado de Machine Learning            | 20%  |
| Desarrollo de software (API)            | 20%  |
| Procesamiento de datos                  | 10%  |
| Calidad del código                      | 10%  |
| Documentación y claridad                | 10%  |

---
## Consideraciones

* Se evaluará la capacidad de resolver problemas de forma autónoma
* Se valorará la claridad y organización del código
* El sistema debe poder ser ejecutado por un tercero siguiendo las instrucciones del README

---
## Entrega

Se deberá enviar la URL del repositorio Github a la dirección de email del Laboratorio de Ciencia de Datos hasta las **23:55 del miércoles 18 de marzo**.

---
¡Mucho éxito!