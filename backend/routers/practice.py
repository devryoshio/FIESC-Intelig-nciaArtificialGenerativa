from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import speech_recognition as sr
from pydub import AudioSegment
import io
import models

router = APIRouter(prefix="/api", tags=["Prática de Voz"])

def calcular_porcentagem_acerto(frase_original: str, frase_dita: str) -> int:
    orig = "".join(c for c in frase_original.lower() if c.isalnum() or c.isspace()).split()
    dita = "".join(c for c in frase_dita.lower() if c.isalnum() or c.isspace()).split()
    
    if not orig:
        return 0
        
    acertos = 0
    for i, palavra in enumerate(orig):
        if i < len(dita) and palavra == dita[i]:
            acertos += 1
            
    porcentagem = int((acertos / len(orig)) * 100)
    return porcentagem

@router.post("/analyze-voice")
async def analyze_voice(
    lesson_id: int = Form(...), # NOVO: Recebe o ID da lição
    phrase: str = Form(...), 
    file: UploadFile = File(...),
    db: Session = Depends(get_db) # NOVO: Conexão com o banco de dados
):
    try:
        audio_bytes = await file.read()
        
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            
        try:
            texto_transcrito = recognizer.recognize_google(audio_data, language="en-US")
        except sr.UnknownValueError:
            texto_transcrito = ""
        except sr.RequestError:
            raise HTTPException(status_code=503, detail="Serviço de reconhecimento indisponível")

        nota = calcular_porcentagem_acerto(phrase, texto_transcrito)
        transcript_final = texto_transcrito if texto_transcrito else "(Áudio não compreendido)"
        
        # NOVO: Salva o resultado no banco de dados!
        nova_tentativa = models.AttemptModel(
            lesson_id=lesson_id,
            score=nota,
            transcript=transcript_final
        )
        db.add(nova_tentativa)
        db.commit()
        
        return {
            "status": "success",
            "transcript": transcript_final,
            "score": nota
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar áudio: {str(e)}")