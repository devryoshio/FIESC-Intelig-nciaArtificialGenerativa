from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import auth, practice, lessons
import os

# Cria as tabelas automaticamente no SQLite assim que o servidor liga
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shadow Speak API 🚀", 
    description="Backend profissional organizado em módulos e integrado com SQLite real."
)


# Libera a pasta de 'uploads' para o navegador acessar os áudios criados
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configuração do CORS para o Frontend conversar com o Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas do arquivo routers/auth.py
app.include_router(auth.router)
app.include_router(practice.router)
app.include_router(lessons.router)

@app.get("/")
def read_root():
    return {"status": "online", "database": "SQLite Conectado com sucesso!"}