# API Llama-Devs
Una API basada en **RAG (Retrieval-Augmented Generation)** para enseñar inteligencia artificial de forma personalizada a niños, adaptándose a sus estilos de aprendizaje.

---

## 🚀 Características
- Enseñanza personalizada de IA para niños de 5 a 10 años.
- Respuestas adaptadas según estilos de aprendizaje:
  - **Visual**, **Auditivo**, **Kinestésico**, **Lecto-escritura**, y **Juego/Exploración**.
- Uso de una base de datos vectorial para recuperar contenido relevante.
- Generación de respuestas mediante el modelo **Llama-3.2 Vision-Instruct-Turbo**.

---

## 🛠 Requisitos
Antes de instalar, asegúrate de tener lo siguiente:
1. **Python** (versión 3.8 o superior).
2. **PIP** (Administrador de paquetes de Python).
3. **Docker** (Para la base de datos vectorial Qdrant).
4. Una **API Key** de [AIMLAPI](https://aimlapi.com/).

---

## 📦 Instalación

### 1. Configuración de la Base de Datos Vectorial (Qdrant)
Primero, ejecuta un contenedor Docker con Qdrant:

```bash
docker run -d --name qdrant -p 6333:6333 -v qdrant_data:/qdrant_storage qdrant/qdrant
```

Si el contenedor se detiene, puedes reiniciarlo con:
```
docker start qdrant
```

2. Instalar FastAPI

Instala FastAPI con el siguiente comando:
```

pip install "fastapi[standard]"

```
3. Instalar Dependencias del Proyecto

Dentro de la carpeta app, instala las dependencias listadas en requirements.txt:
```

pip install -r requirements.txt
```

4. Configurar Variables de Entorno

Crea un archivo .env en la raíz del proyecto con las siguientes variables:

API_KEY=tu_api_key_de_aimlapi
QDRANT_URL=http://localhost:6333
COLLECTION_NAME=nombre_de_la_coleccion

5. Ejecutar la Aplicación

Inicia la aplicación con:

```
fastapi dev main.py
```

La API estará disponible en: http://localhost:8000 
💻 Uso de la API
Endpoint Principal

    POST /query: Realiza consultas personalizadas adaptadas al estilo de aprendizaje del usuario.

Ejemplo de Cuerpo de Solicitud:

{
  "name": "Juan",
  "age": 8,
  "learning_style": "visual",
  "question": "¿Qué es una red neuronal?"
}

Ejemplo de Respuesta:

{
  "answer": "Hola Juan, aquí tienes una explicación visual: Imagina una red neuronal como una serie de puntos conectados por líneas...",
  "sources": ["source1.pdf", "source2.pdf"]
}



📖 Documentación Interactiva

FastAPI genera automáticamente documentación para los endpoints:

    Swagger UI: http://localhost:8000/docs
    ReDoc: http://localhost:8000/redoc









