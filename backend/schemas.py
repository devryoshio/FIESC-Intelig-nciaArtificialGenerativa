from pydantic import BaseModel, EmailStr
from typing import Optional



# O que é comum para o Usuário
class UserBase(BaseModel):
    email: EmailStr

# Dados necessários para Criar um Usuário
class UserCreate(UserBase):
    name: str
    password: str

# Dados necessários para Logar
class UserLogin(UserBase):
    password: str

# Como a API vai devolver o usuário (Esconde a senha por segurança)
class UserResponse(UserBase):
    id: int
    name: str

    class Config:
        from_attributes = True




# ... (Mantenha todo o código de UserBase, UserCreate, etc. que já estava aí) ...

# =====================================
# SCHEMAS DAS LIÇÕES (NOVO)
# =====================================
class LessonBase(BaseModel):
    phrase: str

class LessonResponse(LessonBase):
    id: int
    audio_path: Optional[str] = None

    class Config:
        from_attributes = True


from dataclasses import dataclass
from typing import List

@dataclass
class FeedbackResult:
    """
    Resposta padronizada retornada por qualquer LLM.
    """
    feedback: str
    score: int
    provider: str
    model: str
    mistakes: List[str]
    tips: List[str]