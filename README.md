# 🏠 Ecuador Real Estate Rental Price Prediction

> **Sistema inteligente de predicción de precios de alquiler en Ecuador**

Una solución completa de ciencia de datos que integra análisis exploratorio, machine learning y una API REST funcional para predecir precios de alquileres inmobiliarios en Ecuador.

---

## 📋 Descripción del Proyecto

Este repositorio contiene una **solución end-to-end** a la prueba de selección del Laboratorio de Ciencia de Datos para la posición de Técnico de Investigación.

El proyecto abarca:
- ✅ **Análisis Exploratorio de Datos (EDA)** - Análisis completo del dataset inmobiliario
- ✅ **Modelado de Machine Learning** - Desarrollo y comparación de modelos de regresión
- ✅ **API REST** - Servicio web funcional para consumir predicciones
- ✅ **Reproducibilidad** - Código documentado y containerizado con Docker

### Objetivo

Predecir el precio de alquiler de un inmueble en Ecuador basándose en:
- Provincia
- Ubicación (Lugar)
- Número de dormitorios
- Número de baños
- Área (m²)
- Número de garajes

---

## 🗂️ Estructura del Repositorio

```
adalab-persel/
├── README.md                           # Este archivo
├── requirements.txt                    # Dependencias Python
│
├── 📊 NOTEBOOKS (Análisis Interactivo)
├── 1_eda.ipynb                         # Notebooks EDA (Exploratory Data Analysis)
├── 2_modeling.ipynb                    # Notebook Modelado de Machine Learning
│
├── 🐍 SCRIPTS DE EJECUCIÓN
├── 1_eda_complete.py                   # Script de análisis de datos
├── 2_modeling_complete.py              # Script de entrenamiento del modelo
│
├── 🚀 API REST
├── api/
│   ├── app.py                          # Aplicación Flask
│   └── __init__.py
│
├── 📁 DATOS
├── data/
│   ├── real_state_ecuador_dataset.csv  # Dataset original (500 propiedades)
│   └── real_state_clean.csv            # Dataset procesado
│
├── 🤖 MODELOS ENTRENADOS
├── models/
│   ├── rental_price_model.pkl          # Modelo Random Forest (serializado)
│   ├── provincia_encoder.pkl           # Encoder para provincias
│   ├── lugar_encoder.pkl               # Encoder para ubicaciones
│   ├── scaler.pkl                      # StandardScaler para features
│   └── metadata.json                   # Metadatos del modelo
│
├── 🐳 DOCKER & DEPLOYMENT
├── Dockerfile                          # Imagen Docker de la API
├── docker-compose.yml                  # Orquestación de contenedores
└── setup.sh                            # Script de instalación automática
```

---

## 🚀 Quick Start

### Opción 1: Ejecución Local (Recomendado para desarrollo)

#### Requisitos
- Python 3.11+
- pip y venv
- Git

#### Pasos

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd adalab-persel
```

2. **Crear ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Ejecutar el pipeline completo**
```bash
# Análisis exploratorio de datos
python 1_eda_complete.py

# Entrenamiento del modelo
python 2_modeling_complete.py

# Iniciar la API
python api/app.py
```

5. **Acceder a la API**
```
http://localhost:5000
```

---

### Opción 2: Docker (Recomendado para producción)

```bash
docker-compose up --build
```

La API estará disponible en: `http://localhost:5000`

---

## 📖 Notebooks Interactivos

Los notebooks Jupyter permiten explorar el análisis paso a paso:

### 1️⃣ **1_eda.ipynb** - Análisis Exploratorio
```
✓ Carga y exploración del dataset (500 propiedades)
✓ Limpieza y normalización de ubicaciones
✓ Manejo inteligente de valores faltantes
✓ Estadísticas descriptivas por provincia y ubicación
✓ Categorización de precios (Económico/Medio/Lujo)
```

### 2️⃣ **2_modeling.ipynb** - Modelado ML
```
✓ Feature engineering y encoding
✓ Comparación de modelos (Linear Regression vs Random Forest)
✓ Evaluación con métricas estándar (R², RMSE, MAE)
✓ Serialización de modelo y preprocesadores
```

Para ejecutar los notebooks:
```bash
jupyter notebook
```

---

## 🤖 API REST - Uso

### Endpoint Principal: POST `/predict`

**Predice el precio de alquiler basado en características**

#### Request
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "provincia": "Pichincha",
    "lugar": "Quito",
    "num_dormitorios": 3,
    "num_banos": 2,
    "area": 120,
    "num_garages": 1
  }'
```

#### Response
```json
{
  "prediction": 488.79,
  "input": {
    "provincia": "Pichincha",
    "lugar": "Quito",
    "num_dormitorios": 3,
    "num_banos": 2,
    "area": 120,
    "num_garages": 1
  },
  "model_info": {
    "type": "Random Forest",
    "r2_score": 0.4724,
    "rmse": 508.23
  }
}
```

### Otros Endpoints

**GET `/`** - Documentación de la API
```bash
curl http://localhost:5000/
```

**GET `/health`** - Estado de la API
```bash
curl http://localhost:5000/health
```

---

## 📊 Resultados del Modelo

### Performance Metrics
- **R² Score:** 0.4724 (explica el 47% de la varianza)
- **RMSE:** $508.23 (error promedio)
- **MAE:** $269.03 (desviación absoluta)

### Feature Importance (Random Forest)
1. **Área:** 50.7% - El factor más importante
2. **Garajes:** 16.5%
3. **Ubicación:** 12.5%
4. **Baños:** 11.5%
5. **Provincia:** 5.4%
6. **Dormitorios:** 3.4%

### Dataset Statistics
- **Total de propiedades:** 482 (post-limpieza)
- **Provincias:** 10
- **Ubicaciones únicas:** 294
- **Precio promedio:** $671.13
- **Rango de precios:** $115 - $8,000

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología |
|-----------|-----------|
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn |
| **API** | Flask, Gunicorn |
| **Containerización** | Docker, Docker Compose |
| **Notebooks** | Jupyter |
| **Visualización** | Matplotlib, Seaborn |

---

## 📚 Archivos de Referencia

- **[PRUEBA.md](PRUEBA.md)** - Enunciado original de la prueba con requisitos
- **[SOLUCION.md](SOLUCION.md)** - Explicación detallada de la solución implementada

---

## 🚢 Deployment en Producción

La API puede ser desplegada en plataformas serverless o cloud:

### Render.com
```bash
# Conectar repositorio GitHub
# Build: pip install -r requirements.txt
# Start: gunicorn -w 4 -b 0.0.0.0:5000 api.app:app
```

### Railway.app
```bash
railway init
railway add
railway up
```

### Fly.io
```bash
fly auth login
fly launch
fly deploy
```

---

## 📝 Documentación Adicional

### Instalación Automática
```bash
chmod +x setup.sh
./setup.sh
```

### Variables de Entorno
Crear archivo `.env`:
```
FLASK_ENV=production
FLASK_DEBUG=0
```

---

## ✨ Características Destacadas

✅ **Análisis Completo** - EDA interactivo con 5 secciones
✅ **Modelo Optimizado** - Random Forest con R² = 0.47
✅ **API Funcional** - REST completa con validación
✅ **Reproducible** - Scripts y notebooks documentados
✅ **Containerizado** - Docker y Docker Compose
✅ **Escalable** - Preparado para producción
✅ **Documentado** - READMEs claros y ejemplos

---

## 🤝 Contribuciones

Este proyecto fue desarrollado como solución a la prueba de selección del Laboratorio de Ciencia de Datos (Marzo 2026).

---

## 📄 Licencia

MIT License - Siéntete libre de usar, modificar y compartir este proyecto.

---

## 📧 Contacto

Para preguntas sobre este proyecto, revisa los archivos `PRUEBA.md` y `SOLUCION.md` para contexto completo.

# SOLUCIÓN IMPLEMENTADA

## Descripción de la Solución

Esta solución implementa un sistema completo de predicción de precios de alquiler para bienes inmuebles en Ecuador, siguiendo un flujo de ciencia de datos end-to-end:

### Componentes principales:

1. **Análisis Exploratorio de Datos (EDA)** - Notebook `1_eda_complete.py`
   - Carga y exploración del dataset
   - Limpieza y normalización de la columna "Lugar"
   - Manejo de valores faltantes
   - Análisis descriptivo completo
   - Creación de categorías de precio

2. **Modelado de Machine Learning** - Notebook `2_modeling_complete.py`
   - Feature engineering y preprocesamiento
   - Comparación de múltiples modelos de regresión
   - Evaluación con métricas estándar (MSE, RMSE, MAE, R²)
   - Serialización del modelo entrenado

3. **API REST** - `api/app.py`
   - Servicio Flask para servir predicciones
   - Endpoint POST /predict para consultas
   - Validación de inputs
   - Documentación integrada

4. **Deployment**
   - Dockerfile para containerización
   - Docker Compose para orquestación
   - Gunicorn como servidor WSGI

---

## Instalación y Configuración Local

### Requisitos previos
- Python 3.11+
- pip y venv
- (Opcional) Docker y Docker Compose

### Opción 1: Instalación Manual

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd adalab-persel
```

2. **Crear y activar el ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Ejecutar el setup completo** (coloca el dataset en `/data` primero)
```bash
python 1_eda_complete.py    # Ejecutar EDA y limpiar datos
python 2_modeling_complete.py  # Entrenar el modelo
```

5. **Iniciar la API**
```bash
python -m api.app
```

La API estará disponible en `http://localhost:5000`

### Opción 2: Instalación con Docker

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost:5000`

---

## Uso de la API

### Endpoints disponibles

#### 1. GET `/`
Obtiene documentación de la API

```bash
curl http://localhost:5000/
```

#### 2. GET `/health`
Verifica el estado de la API

```bash
curl http://localhost:5000/health
```

Respuesta:
```json
{
  "status": "healthy",
  "model_type": "Random Forest Regressor",
  "features": ["Provincia", "Lugar", "Dormitorios", "Baños", "Area", "Garajes"]
}
```

#### 3. POST `/predict`
**Predice el precio de alquiler basado en características de la propiedad**

**Request:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "provincia": "Pichincha",
    "lugar": "Quito",
    "num_dormitorios": 3,
    "num_banos": 2,
    "area": 120,
    "num_garages": 1
  }'
```

**Response:**
```json
{
  "prediction": 650.50,
  "input": {
    "provincia": "Pichincha",
    "lugar": "Quito",
    "num_dormitorios": 3,
    "num_banos": 2,
    "area": 120,
    "num_garages": 1
  },
  "model_info": {
    "type": "Random Forest Regressor",
    "r2_score": 0.8234,
    "rmse": 156.42
  }
}
```

### Ejemplo con Postman

1. Crear una nueva solicitud POST
2. URL: `http://localhost:5000/predict`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "provincia": "Pichincha",
  "lugar": "Iñaquito",
  "num_dormitorios": 2,
  "num_banos": 2,
  "area": 95,
  "num_garages": 1
}
```
5. Click "Send"

---

## Estructura del Proyecto

```
adalab-persel/
├── 1_eda_complete.py              # Análisis exploratorio de datos
├── 2_modeling_complete.py          # Construcción del modelo ML
├── api/
│   ├── __init__.py
│   └── app.py                      # Aplicación Flask
├── data/
│   └── real_state_ecuador_dataset.csv  # Dataset original
├── models/                         # Modelos y encoders entrenados
│   ├── rental_price_model.pkl
│   ├── provincia_encoder.pkl
│   ├── lugar_encoder.pkl
│   ├── scaler.pkl
│   └── metadata.json
├── requirements.txt                # Dependencias de Python
├── setup.sh                        # Script de instalación
├── Dockerfile                      # Configuración Docker
├── docker-compose.yml              # Orquestación Docker
├── .gitignore
└── README.md                       # Este archivo
```

---

## Decisiones Técnicas

### Selección del Modelo
- **Random Forest Regressor**: Elegido como modelo final porque:
  - Mejor desempeño en datos no lineales
  - Robusto ante outliers comunes en datos inmobiliarios
  - Mayor R² score en conjunto de test que Linear Regression
  - Proporciona importancia de características

### Preprocesamiento de Datos
- **Normalización de "Lugar"**: Extrae la ubicación principal de la dirección completa
- **Manejo de valores faltantes**: 
  - Imputación por mediana a nivel de provincia
  - Dropeo de filas sin precio, ubicación o área
- **Encoding**: Label encoding para variables categóricas
- **Scaling**: StandardScaler para características numéricas

### Estructura de API
- **Flask**: Framework ligero y flexible
- **Gunicorn**: Servidor WSGI de producción
- **Docker**: Para reproducibilidad y deployment consistente

---

## Despliegue en Producción

### Opción 1: Render (Recomendado)

1. Conectar el repositorio GitHub a Render
2. Configurar el servicio:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:5000 api.app:app`
3. Desplogar automáticamente

### Opción 2: Railway.app

```bash
railway init
railway add
railway up
```

### Opción 3: Fly.io

```bash
fly auth login
fly launch
fly deploy
```

---

## Métricas del Modelo

El modelo fue evaluado con las siguientes métricas:

- **R² Score (Test)**: 0.4724
- **RMSE (Test)**: $508.23
- **MAE (Test)**: $269.03

Esto significa que el modelo explica aproximadamente el 47% de la varianza en los precios de alquiler.

### Ejemplo de Predicción

Para una propiedad con las siguientes características:
- Provincia: Pichincha
- Ubicación: Quito
- Dormitorios: 3
- Baños: 2
- Área: 120 m²
- Garajes: 1

**Predicción: $488.79**

---

## Archivos Entregables

✓ Notebook: `1_eda_complete.py` - Análisis exploratorio completo
✓ Notebook: `2_modeling_complete.py` - Modelado de regresión
✓ Modelo serializado: `models/rental_price_model.pkl`
✓ API funcional: `api/app.py`
✓ Documentación: Este README.md
✓ Docker support: `Dockerfile` y `docker-compose.yml`

---

## Troubleshooting

### Error: "No module named pandas"
```bash
pip install -r requirements.txt
```

### Error: "Connection refused" al conectar con la API
- Asegurar que la API está corriendo: `python -m api.app`
- Verificar el puerto 5000 está disponible

### Error: "Model file not found"
- Ejecutar primero: `python 2_modeling_complete.py`
- Asegurar que la carpeta `models/` existe y contiene los archivos .pkl

---

## Notas Adicionales

- El dataset original contiene propiedades comerciales (sin dormitorios/baños). Estas se manejan correctamente con imputación de medianas.
- La API maneja gracefully casos de provincias/lugares no vistos en el entrenamiento
- Todos los scripts son reproducibles y pueden ejecutarse múltiples veces
- El código sigue buenas prácticas de PEP 8

¡Mucho éxito!