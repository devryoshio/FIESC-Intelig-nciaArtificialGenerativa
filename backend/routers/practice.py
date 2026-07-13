from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from pydub import AudioSegment
import speech_recognition as sr
import io
import logging

import models
from llm.llm import get_llm

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Prática de Voz"]
)


def calcular_porcentagem_acerto(
    frase_original: str,
    frase_dita: str,
) -> int:

    orig = "".join(
        c for c in frase_original.lower()
        if c.isalnum() or c.isspace()
    ).split()

    dita = "".join(
        c for c in frase_dita.lower()
        if c.isalnum() or c.isspace()
    ).split()

    if not orig:
        return 0

    acertos = 0

    for i, palavra in enumerate(orig):
        if i < len(dita) and palavra == dita[i]:
            acertos += 1

    return int((acertos / len(orig)) * 100)


@router.post("/analyze-voice")
async def analyze_voice(
    lesson_id: int = Form(...),
    phrase: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    try:

        audio_bytes = await file.read()

        audio_segment = AudioSegment.from_file(
            io.BytesIO(audio_bytes)
        )

        wav_io = io.BytesIO()

        audio_segment.export(
            wav_io,
            format="wav"
        )

        wav_io.seek(0)

        recognizer = sr.Recognizer()

        with sr.AudioFile(wav_io) as source:

            audio_data = recognizer.record(source)

        try:

            texto_transcrito = await run_in_threadpool(
                recognizer.recognize_google,
                audio_data,
                language="en-US"
            )

        except sr.UnknownValueError:

            texto_transcrito = ""

        except sr.RequestError:

            raise HTTPException(
                status_code=503,
                detail="Serviço de reconhecimento indisponível."
            )

        nota = calcular_porcentagem_acerto(
            phrase,
            texto_transcrito
        )

        transcript_final = (
            texto_transcrito
            if texto_transcrito
            else "(Áudio não compreendido)"
        )

        llm = get_llm()

        logger.info(
            "Gerando feedback usando %s...",
            llm.__class__.__name__
        )

        feedback = await run_in_threadpool(
            llm.generate_feedback,
            phrase,
            transcript_final,
            nota,
        )

        tentativa = models.AttemptModel(
            lesson_id=lesson_id,
            score=nota,
            transcript=transcript_final,

            # Estes campos precisam existir no AttemptModel
            feedback=feedback.feedback,
            llm_provider=feedback.provider,
            llm_model=feedback.model,
        )

        db.add(tentativa)

        db.commit()

        db.refresh(tentativa)

        return {

            "status": "success",

            "attempt_id": tentativa.id,

            "transcript": transcript_final,

            "score": nota,

            "feedback": feedback.feedback,

            "provider": feedback.provider,

            "model": feedback.model,

            "tips": feedback.tips,

            "mistakes": feedback.mistakes,
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.exception(e)

        raise HTTPException(
            status_code=500,
            detail="Erro interno ao analisar o áudio."
        )


@router.get("/attempts/summary")
def get_attempts_summary(
    db: Session = Depends(get_db)
):

    total = (
        db.query(
            func.count(models.AttemptModel.id)
        ).scalar()
        or 0
    )

    media = (
        db.query(
            func.avg(models.AttemptModel.score)
        ).scalar()
        or 0
    )

    attempts = (
        db.query(models.AttemptModel)
        .order_by(
            models.AttemptModel.created_at.desc()
        )
        .limit(5)
        .all()
    )

    history = []

    for att in attempts:

        lesson = (
            db.query(models.LessonModel)
            .filter(
                models.LessonModel.id == att.lesson_id
            )
            .first()
        )

        history.append({

            "id": att.id,

            "phrase": (
                lesson.phrase
                if lesson
                else "Frase removida"
            ),

            "score": att.score,

            "feedback": att.feedback,

            "date": att.created_at.strftime(
                "%H:%M - %d/%m"
            ),
        })

    return {

        "total_attempts": total,

        "average_score": int(media),

        "history": history
    }