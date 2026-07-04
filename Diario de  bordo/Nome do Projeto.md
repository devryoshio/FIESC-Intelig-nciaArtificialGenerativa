Eu sou um cara sem criativo no nome, então pedi para Gemini dá algumas dicas de nome, ainda por cima pedi para minha esposa escolher entre a  opções, foi escolhido **ShadownSpeak**






A técnica de *shadowing* (onde o aluno escuta e repete logo em seguida para praticar entonação e ritmo) é fantástica, e usar vídeos do YouTube traz um contexto do mundo real que enriquece muito a aplicação. Essa adição cria o fluxo complexo perfeito que o professor está pedindo.

Aqui estão algumas sugestões de nomes curtos, modernos e que combinam bem com a ideia de "sombra" (repetição) e fluência:

### Sugestões de Nomes

* **ShadowSpeak** (Direto ao ponto, focado na técnica e na fala)
* **EchoLingo** (Brinca com a ideia de eco/repetição e idiomas)
* **FluentShadow** (Foca no objetivo final: fluência através do shadowing)
* **VoxMirror** (A ideia de ser um "espelho vocal" para a pronúncia)
* **ShadowCast** (Faz uma brincadeira com "broadcast" e shadowing)
* **LingoEcho** (Sonoridade amigável e moderna)

---

### Como estruturar essa ideia na UI (Lembrete do Mock)

Sua arquitetura de telas (o fluxo do usuário) ficaria incrível assim:

1. **Tela de Entrada/Dashboard:** Onde o usuário vê suas estatísticas simuladas.
2. **Tela de Importação:** Um campo de input onde o usuário cola o link do YouTube.
3. **Tela de Prática (Shadowing):** * De um lado (ou no topo), o player do YouTube (você pode usar um *iframe* nativo do HTML).
* Do outro lado, a transcrição do vídeo rodando.
* Um botão grande de "Gravar Áudio" (Microfone).


4. **Tela de Resultados:** Aquela que já desenhamos, mostrando a porcentagem de acerto e o texto colorido (verde, amarelo e vermelho) mostrando onde ele errou a pronúncia, além das dicas fonéticas.

**⚠️ Alerta de Candura do Orientador:** Lembre-se da regra de ouro da sua avaliação. Você **não vai** criar um backend que realmente baixa o áudio do YouTube, transcreve e compara com o áudio do usuário agora.
Na sua UI de protótipo, quando o usuário colar *qualquer* link do YouTube, o sistema vai carregar um vídeo fixo (ex: um trecho de um TED Talk), mostrar uma transcrição pré-escrita no código e, ao "enviar" o áudio, vai devolver um resultado falso (ex: "85% de acerto"), sempre destacando as mesmas palavras em vermelho. O foco é mostrar que a **interface** está pronta para receber a IA no futuro.

Pensando nessa nova tela que vai incluir o player de vídeo e a transcrição, qual ferramenta (ex: React, Streamlit, Gradio) você pretende pedir para o seu agente de codificação usar?