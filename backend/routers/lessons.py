from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from database import get_db
import models, schemas
import os
import time
from gtts import gTTS

router = APIRouter(prefix="/api/lessons", tags=["Lições"])

# Garante que a pasta existe
os.makedirs("uploads", exist_ok=True)

@router.post("/create", response_model=schemas.LessonResponse)
async def create_lesson(
    phrase: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # A Mágica do Python: Transforma o texto recebido em voz de nativo!
        tts = gTTS(text=phrase, lang='en')
        
        # Cria um nome único e salva o MP3
        filename = f"generated_audio_{int(time.time())}.mp3"
        file_location = f"uploads/{filename}"
        tts.save(file_location)
        
        # Salva a lição no Banco de Dados SQLite
        new_lesson = models.LessonModel(phrase=phrase, audio_path=file_location)
        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)
        
        return new_lesson
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar áudio: {str(e)}")

@router.get("/random", response_model=schemas.LessonResponse)
def get_random_lesson(db: Session = Depends(get_db)):
    # Pega uma frase aleatória do banco para o aluno treinar
    lesson = db.query(models.LessonModel).order_by(func.random()).first()
    
    if not lesson:
        raise HTTPException(status_code=404, detail="Nenhuma lição cadastrada ainda.")
        
    return lesson