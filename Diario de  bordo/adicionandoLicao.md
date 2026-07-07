Perfeito! Vamos atualizar o **`Dashboard.jsx`** para transformar o aplicativo em uma plataforma dinâmica.

Agora, assim que o aluno entra na tela, o React vai fazer um `fetch` para a rota `/api/lessons/random`, buscar uma frase aleatória direto do banco de dados e carregar o áudio nativo em inglês que o Python gerou com a IA (`gTTS`).

Aqui está o código completo do seu **`src/pages/Dashboard.jsx`** atualizado. Substitua todo o conteúdo do arquivo por este:

```jsx
import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mic, Square, RefreshCcw, LogOut, Award, Volume2, PlusCircle } from 'lucide-react';

export default function Dashboard() {
  const navigate = useNavigate();
  const [currentLesson, setCurrentLesson] = useState(null); // Guarda a lição vinda do banco
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [score, setScore] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingLesson, setIsLoadingLesson] = useState(true); // Status de carregamento da lição
  const [audioURL, setAudioURL] = useState(null); // Áudio gravado pelo usuário

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // Função para buscar uma lição aleatória no Backend
  const fetchRandomLesson = async () => {
    setIsLoadingLesson(true);
    setTranscript('');
    setScore(null);
    setAudioURL(null);
    try {
      const response = await fetch('http://localhost:8000/api/lessons/random');
      if (!response.ok) {
        throw new Error('Nenhuma lição encontrada. Cadastre uma frase primeiro!');
      }
      const data = await response.json();
      setCurrentLesson(data);
    } catch (error) {
      alert(error.message);
    } finally {
      setIsLoadingLesson(false);
    }
  };

  // Carrega a primeira lição assim que a tela abre
  useEffect(() => {
    fetchRandomLesson();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  // Função para tocar o áudio de referência (gerado pela IA do Python gTTS)
  const playReferenceAudio = () => {
    if (currentLesson && currentLesson.audio_path) {
      // O FastAPI serve a pasta uploads em http://localhost:8000/uploads/
      const audioUrl = `http://localhost:8000/${currentLesson.audio_path}`;
      const audio = new Audio(audioUrl);
      audio.play();
    }
  };

  const startRecording = async () => {
    setTranscript('');
    setScore(null);
    setAudioURL(null);
    audioChunksRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(audioBlob);
        setAudioURL(url);

        await enviarAudioParaOBackend(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      alert("Por favor, permita o acesso ao microfone para praticar.");
      console.error(err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const enviarAudioParaOBackend = async (audioBlob) => {
    if (!currentLesson) return;
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('phrase', currentLesson.phrase); // Envia a frase atual dinâmica
      formData.append('file', audioBlob, 'voice.webm');

      const response = await fetch('http://localhost:8000/api/analyze-voice', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Erro ao analisar a voz.');
      }

      setTranscript(data.transcript);
      setScore(data.score);

    } catch (error) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f172a] p-6 text-slate-100 flex flex-col items-center">
      
      {/* Header com botões de navegação */}
      <header className="w-full max-w-3xl flex justify-between items-center mb-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-tr from-indigo-600 to-cyan-500 rounded-xl flex items-center justify-center shadow-lg">
            <Mic size={20} className="text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">Shadow Speak</h1>
        </div>
        
        <div className="flex items-center gap-6">
          <button 
            onClick={() => navigate('/create-lesson')}
            className="text-emerald-400 hover:text-emerald-300 flex items-center gap-2 text-sm font-medium transition-colors"
          >
            <PlusCircle size={18} /> Cadastrar Frases
          </button>
          <button 
            onClick={handleLogout} 
            className="text-slate-400 hover:text-rose-400 flex items-center gap-2 text-sm font-medium transition-colors"
          >
            <LogOut size={18} /> Sair
          </button>
        </div>
      </header>

      <main className="w-full max-w-3xl bg-slate-800/50 border border-slate-700 rounded-3xl p-8 shadow-2xl backdrop-blur-sm">
        
        {isLoadingLesson ? (
          <div className="flex flex-col items-center justify-center py-12">
            <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mb-4" />
            <p className="text-slate-400 text-sm">Sorteando uma lição do banco...</p>
          </div>
        ) : currentLesson ? (
          <>
            {/* Bloco da Frase do Banco */}
            <div className="text-center mb-8">
              <h2 className="text-sm font-semibold text-indigo-400 tracking-widest uppercase mb-4">Frase do Banco de Dados</h2>
              <div className="text-3xl font-medium text-white leading-relaxed flex flex-wrap justify-center items-center gap-3">
                <span>"{currentLesson.phrase}"</span>
                <button 
                  onClick={playReferenceAudio}
                  className="p-2 rounded-full bg-slate-700/50 text-cyan-400 hover:bg-cyan-500 hover:text-slate-950 transition-all shadow-md"
                  title="Ouvir pronúncia original da IA"
                >
                  <Volume2 size={20} />
                </button>
              </div>
            </div>

            {/* Botão de Gravação */}
            <div className="flex justify-center mb-10">
              <button
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isLoading}
                className={`w-24 h-24 rounded-full flex items-center justify-center transition-all duration-300 shadow-xl disabled:opacity-50 ${
                  isRecording 
                    ? 'bg-rose-500 hover:bg-rose-600 shadow-rose-500/40 animate-pulse' 
                    : 'bg-indigo-600 hover:bg-indigo-700 shadow-indigo-600/40'
                }`}
              >
                {isLoading ? (
                  <div className="w-8 h-8 border-4 border-white border-t-transparent rounded-full animate-spin" />
                ) : isRecording ? (
                  <Square size={32} className="text-white" />
                ) : (
                  <Mic size={36} className="text-white" />
                )}
              </button>
            </div>

            {/* Resultados */}
            <div className={`transition-all duration-500 overflow-hidden ${transcript ? 'opacity-100 max-h-96' : 'opacity-0 max-h-0'}`}>
              <div className="border-t border-slate-700 pt-8 flex flex-col md:flex-row gap-6 items-start">
                
                <div className="flex-1 bg-slate-900/50 rounded-2xl p-6 border border-slate-700/50 w-full">
                  <h3 className="text-xs font-semibold text-slate-400 uppercase mb-2">O servidor ouviu:</h3>
                  <p className="text-lg text-slate-300 italic mb-6">
                    "{transcript}"
                  </p>

                  {audioURL && (
                    <div className="border-t border-slate-800 pt-4">
                      <h3 className="text-xs font-semibold text-slate-400 uppercase mb-2">Sua Gravação:</h3>
                      <audio controls src={audioURL} className="h-10 w-full rounded-md opacity-80" />
                    </div>
                  )}
                </div>

                {score !== null && (
                  <div className="flex flex-col items-center justify-center bg-gradient-to-b from-indigo-900/40 to-slate-900/40 rounded-2xl p-6 border border-indigo-500/20 min-w-[160px]">
                    <Award size={28} className="text-cyan-400 mb-2" />
                    <span className="text-4xl font-bold text-white mb-1">{score}%</span>
                    <span className="text-xs font-medium text-indigo-300 uppercase">Precisão</span>
                  </div>
                )}
              </div>

              {/* Botão de Próxima Lição */}
              <div className="mt-8 flex justify-center">
                <button 
                  onClick={fetchRandomLesson}
                  className="flex items-center gap-2 text-sm bg-slate-700 hover:bg-slate-600 text-white font-medium transition-colors px-6 py-3 rounded-xl shadow-md"
                >
                  <RefreshCcw size={16} /> Próxima Lição Aleatória
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="text-center py-12 text-slate-400">
            Nenhuma lição encontrada no banco de dados. Use o botão acima para cadastrar!
          </div>
        )}
      </main>
    </div>
  );
}

```

### O que mudou e como funciona agora:

1. **Puxa do Banco:** Assim que a página abre, ela faz a chamada no backend e o SQLite sorteia uma frase.
2. **Botão de Auto-Falante (`Volume2`):** Adicionei uma função (`playReferenceAudio`). Quando clicado, ele busca o caminho do arquivo gerado pelo Python (`uploads/generated_audio_xxx.mp3`) lá no endereço do servidor e toca o áudio nativo perfeito gerado pelo Google TTS para o aluno escutar antes de gravar.
3. **Botão de Atalho no Topo:** Adicionei um link *"Cadastrar Frases"* do lado esquerdo do botão de Sair. Assim você pode pular rapidamente para a tela de criação, adicionar 5 novas frases, voltar para o Dashboard e já começar a praticá-las.
4. **Próxima Lição:** O botão inferior agora limpa a tela e faz um novo sorteio no banco de dados para trazer a próxima lição para você.

Vá em frente, salve o arquivo, cadastre algumas frases e faça o teste completo! Ficou um sistema super dinâmico e profissional. Me conta o que achou!