Analisei parte do backend. A arquitetura está boa para um projeto acadêmico (FastAPI + SQLAlchemy + SQLite), mas há algumas vulnerabilidades que podem ser corrigidas rapidamente. São mudanças pequenas que deixam o projeto muito mais profissional.

## 1. Nunca armazene senhas em texto puro (prioridade máxima)

Atualmente você faz:

```python
password=user.password
```

e no login:

```python
db_user.password != user.password
```

Isso é a maior vulnerabilidade do projeto.

Utilize `passlib` com bcrypt.

```bash
pip install passlib[bcrypt]
```

Crie um arquivo `security.py`

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
   schemes=["bcrypt"],
   deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)
```

Registro:

```python
password=hash_password(user.password)
```

Login:

```python
if not verify_password(user.password, db_user.password):
    raise HTTPException(...)
```

Isso sozinho já muda completamente o nível de segurança.

---

# 2. O token atual não é um token

Hoje:

```python
token = f"token-real-user-{db_user.id}"
```

Qualquer pessoa consegue descobrir.

O correto é usar JWT.

```bash
pip install python-jose[cryptography]
```

Depois gerar algo como

```python
access_token = create_access_token(
    data={"sub": str(db_user.id)}
)
```

Mesmo que você ainda não implemente autenticação completa.

---

# 3. CORS está totalmente aberto

Hoje:

```python
allow_origins=["*"]
```

Para desenvolvimento tudo bem.

Mas para entregar:

```python
allow_origins=[
    "http://localhost:5173",
    "https://meuprojeto.streamlit.app",
]
```

Isso impede sites externos de fazer chamadas.

---

# 4. Validar senha

Hoje qualquer senha é aceita.

No schema:

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=64
    )
```

Pode exigir

* maiúscula
* minúscula
* número

---

# 5. Validar e-mail

Se ainda estiver usando

```python
email: str
```

troque para

```python
EmailStr
```

Assim o FastAPI já rejeita

```
abc
```

---

# 6. Nunca revelar se o e-mail existe

Hoje:

```python
"Este e-mail já está cadastrado"
```

Isso facilita enumeração de usuários.

Melhor:

```python
"Não foi possível realizar o cadastro."
```

Embora para projeto acadêmico isso não seja tão crítico.

---

# 7. Rate limiting

Hoje alguém pode tentar milhares de senhas.

Pode usar

```
slowapi
```

Exemplo:

```python
5 logins por minuto
```

---

# 8. SQLAlchemy

Você usa

```python
.filter(...)
```

Não vi SQL montado manualmente.

Então já está protegido contra SQL Injection.

Esse ponto está correto.

---

# 9. Upload de arquivos

Você possui

```
uploads/
```

Se houver upload de áudio, valide:

* extensão

```python
.wav
.mp3
.ogg
```

* tamanho

por exemplo

```
10 MB
```

* nome do arquivo

Nunca use

```python
file.filename
```

Gere

```python
uuid4().hex
```

---

# 10. Esconder mensagens internas

Nunca retorne

```python
Exception
```

ao usuário.

Sempre

```python
HTTPException(
    status_code=500,
    detail="Erro interno."
)
```

---

# 11. Secrets

Nunca coloque

```python
SECRET_KEY = "123456"
```

no código.

Use

```
.env
```

com

```python
from dotenv import load_dotenv
```

---

# 12. Headers de segurança

Adicione um middleware

```python
@app.middleware("http")
async def security_headers(request, call_next):

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["Referrer-Policy"] = "same-origin"

    return response
```

---

# 13. HTTPS

Se publicar na internet,

* HTTPS obrigatório.

Nunca exponha

```
http://
```

---

# 14. Banco

SQLite está ótimo para a disciplina.

Mas coloque no `.gitignore`

```
shadow_speak.db
```

senão você publica usuários reais.

---

# 15. node_modules

Percebi algo importante no ZIP.

Seu projeto contém

```
frontend/node_modules/
```

Isso **não deve ir para o GitHub**.

Também remova

```
__pycache__/
```

e crie um `.gitignore` adequado.

---

## Prioridade das melhorias

Se eu tivesse apenas uma tarde para melhorar o projeto, faria nesta ordem:

1. Senhas com **bcrypt**.
2. JWT para autenticação.
3. Remover `allow_origins=["*"]`.
4. Validar e-mails (`EmailStr`) e senhas (`Field(min_length=8)`).
5. Usar `.env` para chaves secretas.
6. Adicionar validação de uploads.
7. Configurar `.gitignore` para excluir `node_modules`, `__pycache__`, `.db`, `.env` e arquivos temporários.

Essas alterações não mudam a interface do projeto, mas elevam significativamente a qualidade técnica e demonstram preocupação com boas práticas de segurança.
