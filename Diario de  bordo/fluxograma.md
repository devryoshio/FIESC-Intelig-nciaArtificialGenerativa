Excelente adição! Incluir uma tela de login e um sistema de ranking de palavras (uma espécie de *leaderboard* do próprio aluno) traz uma camada de gamificação e personalização fantástica para o **Shadow Speak**. Isso consolida ainda mais a complexidade do seu projeto para garantir a nota máxima.

Aqui está a estrutura em formato de fluxograma e o detalhamento de como essa primeira parte vai funcionar.

---

## Fluxograma da Jornada do Usuário

Abaixo está o caminho lógico que o usuário fará ao abrir a sua aplicação:

**[ Tela de Login ]** ➔ Autenticação bem-sucedida ➔ **[ Dashboard Principal ]**

A partir do **[ Dashboard Principal ]**, o usuário pode navegar para três áreas distintas:

1. **[ Dashboard Principal ]** ➔ **[ Área de Prática (Shadowing) ]**
2. **[ Dashboard Principal ]** ➔ **[ Histórico de Frases ]**
3. **[ Dashboard Principal ]** ➔ **[ Ranking de Palavras ]**

---

## Detalhamento da Estrutura das Telas

Para orientar o seu agente de codificação (Claude, Cursor, etc.), você pode pedir para ele construir as seguintes interfaces:

### 1. Tela de Login (Ponto de Entrada)

* **Objetivo:** Simular o controle de acesso do aluno.
* **Componentes visuais:** Logo do *Shadow Speak*, campo de e-mail, campo de senha e botão "Entrar".
* **Comportamento Mockado:** Qualquer e-mail e senha digitados devem liberar o acesso e redirecionar para o Dashboard.

### 2. Dashboard Principal (Visão Geral)

* **Objetivo:** Ser a central de comando do aluno logo após o login.
* **Componentes visuais:** Um menu lateral ou superior (Navbar) para navegar pelas outras telas.
* **Métricas rápidas:** Cards mostrando "Total de horas praticadas" e "Média geral de acertos".

### 3. Tela de Histórico de Frases

* **Objetivo:** Mostrar tudo o que o usuário já enviou de áudio no passado.
* **Componentes visuais:** Uma lista ou tabela contendo a data, a frase praticada e a nota obtida naquela gravação específica.
* **Interação:** Um botão de "Ouvir gravação" ao lado de cada frase (que, por enquanto, pode tocar um áudio genérico de teste).

### 4. Tela de Ranking de Palavras (Estatísticas Detalhadas)

* **Objetivo:** Mostrar as palavras que o aluno mais domina e as que mais precisa treinar.
* **Componentes visuais:** Uma tabela estilizada dividida entre "Palavras Fortes" (verde) e "Palavras a Melhorar" (vermelho).

### Exemplo de Estrutura da Tabela de Ranking

| Palavra Falada | Vezes Praticadas | Porcentagem de Acerto | Status |
| --- | --- | --- | --- |
| *Although* | 12 | 95% | 🟢 Excelente |
| *Through* | 8 | 88% | 🟢 Bom |
| *Rhythm* | 15 | 60% | 🟡 Atenção |
| *Worcestershire* | 5 | 30% | 🔴 Praticar |

---

> **Dica de Ouro do Orientador:** Quando for passar essa estrutura para a IA gerar o código, peça para ela criar um arquivo `mockData.json` (ou um dicionário fixo em Python) com dados falsos de histórico e ranking. Assim, quando a aplicação carregar, a tabela de ranking e o histórico já aparecerão preenchidos e bonitos na tela, prontos para a avaliação do professor, sem você precisar digitar nada na hora.