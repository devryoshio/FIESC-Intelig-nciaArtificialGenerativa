from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
import datetime

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class LessonModel(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, index=True)
    audio_path = Column(String, nullable=True)

# NOVA TABELA: Registra cada gravação que o usuário faz
class AttemptModel(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id")) # Liga a tentativa com a lição
    score = Column(Integer)                               # A nota (0 a 100)
    transcript = Column(String)                           # O que o servidor entendeu que ele falou
    created_at = Column(DateTime, default=datetime.datetime.utcnow) # Data e hora automática