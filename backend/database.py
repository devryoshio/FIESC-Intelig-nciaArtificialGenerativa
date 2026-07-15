from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# Isso vai salvar o banco exatamente na mesma pasta deste arquivo de configuração
DATABASE_PATH = os.path.join(BASE_DIR, "shadowspeak.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# Mude para usar 4 barras (caminho absoluto no Linux/Docker):
# SQLALCHEMY_DATABASE_URL = "sqlite:////app/shadowspeak.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função utilitária para abrir e fechar a conexão com o banco automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()