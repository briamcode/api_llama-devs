from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.vectorstore import get_vectorstore
from app.config import qdrant_client, COLLECTION_NAME
import logging
from openai import OpenAI

# Configuración del cliente OpenAI
API_BASE_URL = "https://api.aimlapi.com/v1"
API_KEY = ""  # Reemplaza con tu clave API
MODEL_NAME = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"
TEMPERATURE = 0.7
MAX_TOKENS = 256

# Crear instancia del cliente
api = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)

router = APIRouter()

class QueryRequest(BaseModel):
    name: str
    age: int
    learning_style: str
    question: str

@router.post("/", summary="Realizar una consulta personalizada")
async def query_document(request: QueryRequest):
    """
    Realizar una consulta personalizada basada en los datos del usuario y los documentos vectorizados.
    """
    # Verificar si la colección existe
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        if collection_info.points_count == 0:
            return {
                "answer": "No hay embeddings en la colección. Por favor, suba documentos antes de realizar consultas.",
                "sources": []
            }
    except Exception as e:
        logging.error(f"Error al verificar la colección en Qdrant: {str(e)}")
        return {
            "answer": "No se pudo conectar con la base de datos de embeddings. Intente más tarde.",
            "sources": []
        }

    try:
        # Obtener el vectorstore
        vectorstore = get_vectorstore()

        # Crear un retriever y realizar la consulta
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        related_docs = retriever.invoke(request.question)

        # Si no se encuentran documentos relevantes
        if not related_docs:
            fallback_response = (
                f"Hola {request.name}, parece que no encontré información específica sobre tu pregunta: "
                f"'{request.question}'. Sin embargo, puedo ayudarte a aprender algo interesante relacionado con "
                f"tu estilo de aprendizaje {request.learning_style}."
            )
            return {
                "answer": fallback_response,
                "sources": []
            }

        # Concatenar el contenido relevante para el contexto
        MAX_CONTEXT_LENGTH = 2000
        context = "\n".join([doc.page_content for doc in related_docs])[:MAX_CONTEXT_LENGTH]

        if not context.strip():
            return {
                "answer": "No se encontró contenido relevante en los documentos.",
                "sources": []
            }

        # Generar el prompt según el estilo de aprendizaje
        learning_prompts = {
            "visual": "Explica este tema usando imágenes mentales y gráficos simples.",
            "auditivo": "Responde de manera detallada usando ejemplos que puedan explicarse como una historia oral.",
            "kinestésico": "Crea una explicación que involucre actividades prácticas o ejemplos interactivos.",
            "lecto-escritura": "Responde usando explicaciones textuales claras y listas organizadas.",
            "juego/exploración": "Genera una explicación que motive al aprendizaje a través de un juego o exploración interactiva."
        }

        # Elegir el prompt según el estilo de aprendizaje
        prompt_instruction = learning_prompts.get(
            request.learning_style.lower(),
            "Responde de forma clara y simple adaptada a niños."
        )

        # Generar el contexto personalizado
        user_context = (
            f"Hola {request.name}, como tienes {request.age} años y prefieres aprender con un estilo "
            f"{request.learning_style}, aquí tienes una enseñanza personalizada.\n"
        )

        # Generar la respuesta con el modelo en línea
        try:
            completion = api.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un tutor experto en AI y machine learning que enseña a niños de 5 a 10 años para que ellos entiendan de forma divertida."
                    },
                    {
                        "role": "user",
                        "content": f"{user_context}{prompt_instruction}\n\nContexto: {context}\n\nPregunta: {request.question}"
                    },
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )

            response = completion.choices[0].message.content

            return {
                "answer": response,
                "sources": [
                    doc.metadata.get("source", "desconocido") if doc.metadata else "desconocido"
                    for doc in related_docs
                ]
            }
        except Exception as e:
            logging.error(f"Error al generar respuesta del modelo LLM: {str(e)}")
            return {
                "answer": "Ocurrió un error al generar la respuesta. Intente más tarde.",
                "sources": []
            }
    except Exception as e:
        logging.error(f"Error al realizar la consulta: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al procesar la consulta.")
