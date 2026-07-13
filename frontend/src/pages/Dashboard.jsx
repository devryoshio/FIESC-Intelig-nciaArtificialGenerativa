import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mic, Square, RefreshCcw, LogOut, Award, Volume2, PlusCircle, Send, BarChart2 } from 'lucide-react';

export default function Dashboard() {
  const navigate = useNavigate();
  const [currentLesson, setCurrentLesson] = useState(null);
  
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [score, setScore] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingLesson, setIsLoadingLesson] = useState(true);
  
  const [audioURL, setAudioURL] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null); 

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);


  const [feedback, setFeedback] = useState('');
  
  const [tips, setTips] = useState([]);
  const [mistakes, setMistakes] = useState([]);
  const [provider, setProvider] = useState('');
  const [model, setModel] = useState('');

  const fetchRandomLesson = async () => {
    setIsLoadingLesson(true);
    resetPracticeState();
    try {
      const response = await fetch('/api/lessons/random');
      if (!response.ok) {
        throw new Error('Nenhuma lição encontrada. Cadastre uma frase primeiro!');
      }
      const data = await response.json();
      setCurrentLesson(data);
    } catch (error) {
      alert(error.message);
    } finally { // <-- CORRIGIDO AQUI!
      setIsLoadingLesson(false);
    }
  };

  useEffect(() => {
    fetchRandomLesson();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const playReferenceAudio = () => {
    if (currentLesson && currentLesson.audio_path) {
      const audioUrl = `http://localhost:8000/${currentLesson.audio_path}`;
      const audio = new Audio(audioUrl);
      audio.play();
    }
  };

  const resetPracticeState = () => {
  setTranscript('');
  setScore(null);

  setFeedback('');
  setTips([]);
  setMistakes([]);
  setProvider('');
  setModel('');

  setAudioURL(null);
  setAudioBlob(null);
};
  const startRecording = async () => {
    resetPracticeState();
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

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        setAudioURL(URL.createObjectURL(blob));
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      alert("Por favor, permita o acesso ao microfone para praticar.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const enviarAudioParaOBackend = async () => {
    if (!currentLesson || !audioBlob) return;
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('lesson_id', currentLesson.id); 
      formData.append('phrase', currentLesson.phrase);
      formData.append('file', audioBlob, 'voice.webm');

      const response = await fetch('/api/analyze-voice', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Erro ao analisar a voz.');
      }

    
      setTranscript(data.transcript);
      setScore(data.score);

      setFeedback(data.feedback || '');
      setTips(data.tips || []);
      setMistakes(data.mistakes || []);
      setProvider(data.provider || '');
      setModel(data.model || '');

    } catch (error) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f172a] p-6 text-slate-100 flex flex-col items-center">
      
      <header className="w-full max-w-3xl flex justify-between items-center mb-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-tr from-indigo-600 to-cyan-500 rounded-xl flex items-center justify-center shadow-lg">
            <Mic size={20} className="text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">Shadow Speak</h1>
        </div>
        
        <div className="flex items-center gap-5">
          <button onClick={() => navigate('/stats')} className="text-indigo-400 hover:text-indigo-300 flex items-center gap-2 text-sm font-medium transition-colors">
            <BarChart2 size={18} /> Meu Desempenho
          </button>
          <button onClick={() => navigate('/create-lesson')} className="text-emerald-400 hover:text-emerald-300 flex items-center gap-2 text-sm font-medium transition-colors">
            <PlusCircle size={18} /> Cadastrar Frases
          </button>
          <button onClick={handleLogout} className="text-slate-400 hover:text-rose-400 flex items-center gap-2 text-sm font-medium transition-colors border-l border-slate-700 pl-5">
            <LogOut size={18} /> Sair
          </button>
        </div>
      </header>

      <main className="w-full max-w-3xl bg-slate-800/50 border border-slate-700 rounded-3xl p-8 shadow-2xl backdrop-blur-sm">
        {isLoadingLesson ? (
          <div className="flex flex-col items-center justify-center py-12">
            <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mb-4" />
            <p className="text-slate-400 text-sm">Sorteando lição...</p>
          </div>
        ) : currentLesson ? (
          <>
            <div className="text-center mb-8">
              <h2 className="text-sm font-semibold text-indigo-400 tracking-widest uppercase mb-4">Frase a ser pronunciada</h2>
              <div className="text-3xl font-medium text-white leading-relaxed flex flex-wrap justify-center items-center gap-3">
                <span>"{currentLesson.phrase}"</span>
                <button onClick={playReferenceAudio} className="p-2 rounded-full bg-slate-700/50 text-cyan-400 hover:bg-cyan-500 hover:text-slate-950 transition-all shadow-md">
                  <Volume2 size={20} />
                </button>
              </div>
            </div>

            <div className="flex justify-center mb-6">
              <button
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isLoading}
                className={`w-24 h-24 rounded-full flex items-center justify-center transition-all duration-300 shadow-xl disabled:opacity-50 ${
                  isRecording ? 'bg-rose-500 hover:bg-rose-600 shadow-rose-500/40 animate-pulse' : 'bg-indigo-600 hover:bg-indigo-700 shadow-indigo-600/40'
                }`}
              >
                {isRecording ? <Square size={32} className="text-white" /> : <Mic size={36} className="text-white" />}
              </button>
            </div>
            
            <div className={`transition-all duration-500 overflow-hidden ${audioURL ? 'opacity-100 max-h-[500px]' : 'opacity-0 max-h-0'}`}>
              <div className="bg-slate-900/80 rounded-2xl p-6 border border-slate-700/50 flex flex-col items-center gap-4 mb-6">
                <h3 className="text-sm font-semibold text-slate-300">Ouça sua gravação antes de enviar:</h3>
                <audio controls src={audioURL} className="w-full max-w-md h-12 rounded-md" />
                
                {score === null && (

                  
                  <button 
                    onClick={enviarAudioParaOBackend}
                    disabled={isLoading}
                    className="mt-2 bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-semibold py-3 px-8 rounded-xl shadow-lg transition-all disabled:opacity-50 flex justify-center items-center gap-2"
                  >
                    {isLoading ? <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" /> : <><Send size={18} /> Avaliar Pronúncia</>}
                  </button>
                )}
              </div>
            </div>

          <div className={`transition-all duration-500 overflow-hidden ${
  score !== null ? 'opacity-100 max-h-[1200px]' : 'opacity-0 max-h-0'
}`}>

  {/* Resultado atual */}
  <div className="border-t border-slate-700 pt-8 flex flex-col md:flex-row gap-6 items-start">

    {/* Transcrição */}
    <div className="flex-1 bg-slate-900/50 rounded-2xl p-6 border border-slate-700/50 w-full">
      <h3 className="text-xs font-semibold text-slate-400 uppercase mb-2">
        O servidor ouviu:
      </h3>

      <p className="text-lg text-slate-300 italic">
        "{transcript}"
      </p>
    </div>

    {/* Nota */}
    <div className="flex flex-col items-center justify-center bg-gradient-to-b from-indigo-900/40 to-slate-900/40 rounded-2xl p-6 border border-indigo-500/20 min-w-[160px]">
      <Award size={28} className="text-cyan-400 mb-2" />

      <span className="text-4xl font-bold text-white mb-1">
        {score}%
      </span>

      <span className="text-xs font-medium text-indigo-300 uppercase">
        Precisão
      </span>
    </div>

  </div>

  {/* =================================================== */}
  {/* NOVA ÁREA DA IA */}
  {/* =================================================== */}

  {feedback && (
    <div className="mt-8 bg-slate-900/60 rounded-2xl border border-cyan-500/20 p-6">
      <h3 className="text-lg font-semibold text-cyan-400 mb-4">
        🤖 Feedback da IA
      </h3>

      <p className="text-slate-300 leading-relaxed whitespace-pre-line">
        {feedback}
      </p>
    </div>
  )}

  {mistakes.length > 0 && (
    <div className="mt-6 bg-slate-900/60 rounded-2xl border border-red-500/20 p-6">
      <h3 className="text-lg font-semibold text-red-400 mb-3">
        🎯 Pontos de atenção
      </h3>

      <ul className="list-disc ml-5 space-y-2">
        {mistakes.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  )}

  {tips.length > 0 && (
    <div className="mt-6 bg-slate-900/60 rounded-2xl border border-emerald-500/20 p-6">
      <h3 className="text-lg font-semibold text-emerald-400 mb-3">
        💡 Sugestões
      </h3>

      <ul className="list-disc ml-5 space-y-2">
        {tips.map((tip, index) => (
          <li key={index}>{tip}</li>
        ))}
      </ul>
    </div>
  )}

  {provider && (
    <div className="mt-6 text-center text-xs text-slate-500">
      IA utilizada: {provider} ({model})
    </div>
  )}

  <div className="mt-8 flex justify-center">
    <button
      onClick={fetchRandomLesson}
      className="flex items-center gap-2 text-sm bg-slate-700 hover:bg-slate-600 text-white font-medium transition-colors px-6 py-3 rounded-xl shadow-md"
    >
      <RefreshCcw size={16} />
      Próxima Lição Aleatória
    </button>
  </div>

</div>
          </>
        ) : (
          <div className="text-center py-12 text-slate-400">Nenhuma lição encontrada.</div>
        )}
      </main>
    </div>
  );
}