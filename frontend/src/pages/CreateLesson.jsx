import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Plus, ArrowLeft } from 'lucide-react';

export default function CreateLesson() {
  const navigate = useNavigate();
  const [phrase, setPhrase] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!phrase.trim()) return;
    
    setIsLoading(true);

    try {
      // Como o backend usa Form(...), precisamos mandar como FormData
      const formData = new FormData();
      formData.append('phrase', phrase);

      const response = await fetch('http://localhost:8000/api/lessons/create', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Erro ao criar a lição');
      }

      alert('Lição criada com sucesso! O áudio foi gerado.');
      setPhrase(''); // Limpa o campo para a próxima frase

    } catch (error) {
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0f172a] p-6 text-slate-100 flex flex-col items-center justify-center">
      
      <div className="w-full max-w-lg bg-slate-800/50 border border-slate-700 rounded-3xl p-8 shadow-2xl backdrop-blur-sm">
        
        <button 
          onClick={() => navigate('/dashboard')}
          className="text-slate-400 hover:text-white flex items-center gap-2 mb-6 transition-colors text-sm"
        >
          <ArrowLeft size={16} /> Voltar para o Dashboard
        </button>

        <div className="flex items-center gap-3 mb-8">
          <div className="w-12 h-12 bg-gradient-to-tr from-emerald-500 to-teal-400 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <BookOpen size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Nova Lição</h1>
            <p className="text-sm text-slate-400">Adicione uma frase em inglês para o banco de dados.</p>
          </div>
        </div>

        <form onSubmit={handleCreate} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">Frase em Inglês</label>
            <textarea 
              required
              value={phrase}
              onChange={(e) => setPhrase(e.target.value)}
              placeholder="Ex: I would like a cup of coffee, please."
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all resize-none h-32"
            />
          </div>

          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-semibold py-3 px-4 rounded-xl shadow-lg transition-all disabled:opacity-50 flex justify-center items-center gap-2"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Plus size={20} /> Salvar e Gerar Áudio
              </>
            )}
          </button>
        </form>
      </div>
      
    </div>
  );
}