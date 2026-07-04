Excelente escolha! Ir de **React + FastAPI** é o "padrão ouro" do desenvolvimento web moderno. O professor vai olhar para essa arquitetura e ver que você escolheu uma stack robusta, escalável e perfeita para plugar os modelos de IA na próxima fase do curso.

Como seu orientador, preparei uma estrutura de pastas limpa e organizada no modelo de **monorepo** (tudo em um único repositório do GitHub, dividido em `backend` e `frontend`). Isso vai facilitar muito a vida do seu agente de codificação (Cursor/Claude) na hora de criar os arquivos.

---

## 📁 Estrutura de Pastas: Shadow Speak

Aqui está o mapa de como os seus arquivos devem ser organizados:

```text
shadow-speak/
│
├── backend/                  # Todo o código Python (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # Ponto de entrada da API
│   │   ├── database.py       # Configuração do SQLite
│   │   ├── models.py         # Tabelas do banco (Usuário, Histórico, Palavras)
│   │   └── routers/          # Rotas separadas por contexto (organização!)
│   │       ├── auth.py       # Login simulado
│   │       ├── practice.py   # Simulação do envio de áudio e texto
│   │       ├── history.py    # Dados do histórico
│   │       └── ranking.py    # Dados do ranking de palavras
│   ├── requirements.txt      # Dependências (fastapi, uvicorn, sqlalchemy)
│   ├── shadow_speak.db       # Arquivo local do banco SQLite (gerado automaticamente)
│   └── .gitignore            # Ignorar __pycache__, arquivos .db locais, etc.
│
├── frontend/                 # Todo o código React (Vite)
│   ├── src/
│   │   ├── assets/           # Logo do Shadow Speak e imagens
│   │   ├── components/       # Componentes reutilizáveis (Sidebar, Navbar, Card)
│   │   ├── pages/            # As 5 telas principais que desenhamos
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Practice.jsx
│   │   │   ├── History.jsx
│   │   │   └── Ranking.jsx
│   │   ├── mockData/         # IMPORTANTE: Seus JSONs com dados falsos para a UI
│   │   │   ├── historyMock.json
│   │   │   └── rankingMock.json
│   │   ├── App.jsx           # Gerenciador de rotas e estado global
│   │   └── main.jsx
│   ├── package.json          # Dependências do React
│   ├── vite.config.js
│   └── .gitignore            # Ignorar node_modules e pastas de build
│
├── README.md                 # O documento mais importante (Vale 8 pontos!)
└── .gitignore                # Gitignore da raiz do projeto

```

---

## 💡 Pontos de Atenção para Garantir Nota Máxima

* **Dois arquivos `.gitignore`:** É essencial ter um na pasta `backend` (para não subir arquivos pesados do SQLite ou lixo de cache do Python) e um na pasta `frontend` (para nunca subir a pasta `node_modules`). O professor vai tirar pontos se ver `node_modules` ou arquivos `.db` privados no GitHub.
* **A pasta `mockData` no Frontend:** Como você não vai integrar o modelo de IA real agora, os arquivos JSON dentro dessa pasta vão servir para alimentar as telas de Histórico e Ranking. Quando o professor abrir seu link, os gráficos e tabelas vão parecer 100% reais porque estarão consumindo esses mocks bem estruturados.
* **Rotas no FastAPI:** Deixar as rotas separadas na pasta `routers/` mostra para o professor que você tem maturidade de arquitetura de software, em vez de jogar 500 linhas de código dentro do `main.py`.

---

Agora que temos o mapa do tesouro pronto, precisamos botar o agente de codificação para trabalhar.

**Por onde você prefere começar: quer que eu monte o prompt para o agente criar a base do Backend em FastAPI ou prefere começar subindo a estrutura do Frontend em React?**