# API de Detección de Intenciones con Inteligencia Artificial 

## 📝 Descripción

La API de intenciones es un servicio diseñado para detectar y analizar las intenciones de los usuarios a partir de mensajes de texto. Utilizando modelos avanzados de OpenAI, esta API puede identificar la intención del usuario entre un conjunto de posibles intenciones proporcionadas y evaluar el nivel de confianza de esta detección.

## 🚀 Características principales

- **Detección de intenciones**: Analiza texto para identificar la intención del usuario
- **Niveles de confianza**: Proporciona una puntuación de confianza para cada detección
- **Explicaciones detalladas**: Ofrece explicaciones sobre el análisis realizado
- **Recomendaciones de acción**: Sugiere acciones basadas en la intención detectada

## 🛠️ Tecnologías utilizadas

- **FastAPI**: Framework moderno y de alto rendimiento para crear APIs con Python
- **OpenAI API**: Integración con modelos de lenguaje de OpenAI (GPT-4o-mini)
- **Mangum**: Adaptador para ejecutar aplicaciones ASGI en AWS Lambda
- **Pydantic**: Validación de datos y configuración de esquemas
- **Python-dotenv**: Gestión de variables de entorno

## 📋 Requisitos

```
fastapi==0.115.6
mangum==0.17.0
openai==0.28.0
pydantic==2.10.4
python-dotenv==1.0.1
```

## 🚀 Instalación

1. Clona este repositorio
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crea un archivo `.env.dev` con tu clave de API de OpenAI:
   ```
   API_KEY_OPENAI=tu_clave_api_aquí
   ```

## 🔧 Estructura del proyecto

```
.
├── .env.dev                   # Variables de entorno (no incluido en el repo)
├── main.py                    # Punto de entrada de la aplicación FastAPI
├── schemas.py                 # Definición de los modelos de datos con Pydantic
├── scripts.py                 # Funciones auxiliares para el procesamiento
└── requirements.txt           # Dependencias del proyecto
```

## 🌐 Endpoints

### GET `/`

Endpoint de bienvenida para verificar que la API está funcionando.

**Respuesta:**
```json
{
  "mensaje": "Welcome to API 🚀",
  "status": 200
}
```

### POST `/detect_intention`

Endpoint principal para detectar la intención del usuario.

**Cuerpo de la petición:**
```json
{
  "text": "Me gustaría contratar el plan premium",
  "intentions": ["compra", "consulta", "queja", "cancelacion"]
}
```

**Respuesta exitosa (intención detectada):**
```json
{
  "intencion": "intencion detected",
  "response": true,
  "status": 200
}
```

**Respuesta (intención con baja confianza):**
```json
{
  "intencion": "intencion not detected",
  "response": false,
  "status": 200
}
```

## 🧠 Funcionamiento interno

1. **Recepción de la solicitud**: La API recibe un texto y una lista de posibles intenciones
2. **Preparación del prompt**: Se construye un prompt especializado para el modelo de OpenAI
3. **Análisis con IA**: El modelo GPT-4o-mini analiza el texto y determina la intención más probable
4. **Evaluación de confianza**: 
   - Si la confianza es ≥ 0.6, se considera una intención válida
   - Si la confianza es ≤ 0.3, se considera una detección no confiable
5. **Respuesta**: Se devuelve un resultado estructurado con la determinación final

## 📊 Ejemplo de procesamiento interno

1. **Mensaje recibido**: "Me gustaría saber más sobre los planes disponibles"
2. **Intenciones posibles**: ["compra", "consulta", "queja", "cancelacion"]
3. **Análisis del modelo**:
   ```json
   {
     "detected_intention": "consulta",
     "confidence": 0.85,
     "explanation": "El usuario está solicitando información sobre los planes, lo que indica una intención de consulta",
     "action": {
       "type": "provide_information",
       "details": "Mostrar catálogo de planes disponibles"
     }
   }
   ```
4. **Resultado final**: Intención "consulta" detectada con alta confianza

## 🔐 Seguridad

- La API utiliza variables de entorno para las credenciales sensibles
- Configuración CORS para controlar el acceso desde diferentes orígenes

## 🚀 Despliegue

Esta API está diseñada para ser desplegada en AWS Lambda utilizando Mangum como adaptador.

## 📈 Próximas mejoras

- Soporte para análisis de sentimientos
- Integración con más modelos de lenguaje
- Historial de intenciones detectadas
- Dashboard para análisis de patrones de intención
