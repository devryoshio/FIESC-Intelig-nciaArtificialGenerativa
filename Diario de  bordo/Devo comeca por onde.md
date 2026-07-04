Como seu orientador, a minha recomendação é categórica: **nunca comece a desenvolver os dois ao mesmo tempo.** Tentar construir o Frontend e o Backend em paralelo, especialmente sozinho, é uma armadilha que aumenta a probabilidade de erros, mistura conceitos na sua cabeça e torna a depuração (*debugging*) um pesadelo.

Para o seu cenário (onde o foco atual é entregar um protótipo funcional de alta complexidade visual para o professor), existem duas estratégias inteligentes. Escolha a que melhor se adapta ao seu estilo:

---

### Estratégia 1: Funcionalidade por Funcionalidade (Fatias Verticais) — *A MAIS RECOMENDADA* 🏆

Em vez de dividir o trabalho por "tecnologia" (Back vs. Front), você divide por **funcionalidade**. Você escolhe uma tela, faz o Frontend dela e, logo em seguida, faz o Backend correspondente.

* **Como fazer:**
1. Cria a tela de **Login no React** ➔ Cria a rota de **Login no FastAPI** ➔ Junta as duas e testa.
2. Cria o **Dashboard no React** (com dados mockados) ➔ Cria a rota do **Dashboard no FastAPI** ➔ Substitui os mocks pelos dados da API.


* **Por que é a melhor?** O seu projeto estará **sempre a funcionar**. Se o prazo apertar ou se você tiver um problema na fase final, você já tem várias partes do sistema 100% concluídas e integradas para mostrar ao professor. Além disso, os agentes de IA (Cursor/Claude) trabalham muito melhor quando focam num fluxo fechado de cada vez.

---

### Estratégia 2: Frontend Primeiro (Foco na Interface)

Como o professor vai avaliar severamente a usabilidade e a complexidade das telas, você pode focar em construir **toda a interface no React primeiro**, usando apenas os arquivos de `mockData.json` que estruturámos.

* **Como fazer:** Você cria o Login, o Dashboard, a Sala de Shadowing, o Histórico e o Ranking. Deixa tudo lindo, navegável e com os dados falsos a aparecer na perfeição. Só depois de o Frontend estar totalmente pronto é que abre a pasta do FastAPI para criar as rotas e substituir esses dados falsos por dados reais.
* **Por que é boa?** Dá-lhe uma sensação rápida de progresso (você vê a aplicação acontecer visualmente) e garante que a parte que vale mais pontos (a interface e a documentação do README) fica garantida logo de início.

---

### 🛑 O que NÃO fazer: Backend Primeiro

Muitos programadores começam pelo Backend (banco de dados, tabelas, rotas). Para este trabalho de faculdade, **não faça isso**. Se gastar muito tempo a configurar o SQLite e as rotas do FastAPI, pode chegar perto da data de entrega com um Backend perfeito, mas sem tempo para deixar o Frontend bonito. E lembre-se: o professor avalia o que ele consegue ver e clicar!

### O Próximo Passo

Seguindo a **Estratégia 1 (Fatias Verticais)**, o nosso primeiro objetivo é a **Tela de Login**.

Quer que eu gere o prompt exato para você passar para o seu agente de codificação criar a **página de Login no React com Tailwind CSS**, ou prefere começar logo pela estrutura inicial do projeto?