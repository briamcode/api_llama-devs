from fastapi import FastAPI
from app.routers import upload, query, files
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Agregar el middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por los dominios específicos permitidos, si es necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Registrar enrutadores
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(files.router, prefix="/files", tags=["Files"])

@app.get("/", summary="Verificar el estado", description="Endpoint base para verificar el estado de la API.")
async def root():
    return {"message": "API de RAG lista para solicitudes."}