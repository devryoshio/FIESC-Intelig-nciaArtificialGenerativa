from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from security import hash_password, verify_password


router = APIRouter(prefix="/api", tags=["Autenticação"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Verifica se o e-mail já existe no banco de dados
    db_user = db.query(models.UserModel).filter(models.UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")

    # 2. Se não existir, cria o novo usuário
    

    new_user = models.UserModel(
    name=user.name,
    email=user.email,
    password=hash_password(user.password)
)
    
    # 3. Salva permanentemente no SQLite
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Atualiza o objeto para pegar o ID gerado pelo banco
    return new_user

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # 1. Busca o usuário pelo e-mail
    db_user = db.query(models.UserModel).filter(models.UserModel.email == user.email).first()
    
    # 2. Verifica se o usuário existe e se a senha bate
    

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )
            

    # 3. Retorna o sucesso com os dados reais do banco
    return {
        "status": "success",
        "token": f"token-real-user-{db_user.id}",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }