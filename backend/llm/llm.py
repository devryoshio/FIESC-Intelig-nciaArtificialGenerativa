import os
import json
from openai import OpenAI
# Importa o FeedbackResult lá do seu arquivo de schemas
from schemas import FeedbackResult 

class LLMService:
    def __init__(self):
        # Configuração agnóstica via variáveis de ambiente (.env)
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        
        if self.provider == "ollama":
            self.client = OpenAI(
                base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
                api_key="ollama-local"
            )
        else:
            self.client = OpenAI(api_key=os.getenv("LLM_API_KEY", "sua-chave-da-openai"))

    def generate_feedback(self, phrase_original: str, frase_aluno: str, nota_matematica: int) -> FeedbackResult:
        # 1. Carrega o System Prompt estruturado
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        # Adiciona uma instrução extra para garantir que a IA responda no JSON correto
        json_instruction = """
        Você DEVE responder EXCLUSIVAMENTE com um objeto JSON no seguinte formato:
        {
            "feedback": "Sua avaliação em português aqui",
            "mistakes": ["palavra1", "palavra2"],
            "tips": ["Dica de pronúncia 1", "Dica de pronúncia 2"]
        }
        """

        user_content = f"Frase Correta: {phrase_original}\nO que o aluno falou: {frase_aluno}\nNota Inicial: {nota_matematica}%"

        # 2. Chamada universal (Funciona na OpenAI e no Ollama)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt + json_instruction},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}, # Força o modelo a responder em JSON puro
            temperature=0.3
        )

        # 3. Faz o PARSE da resposta de forma segura
        try:
            raw_content = response.choices[0].message.content
            data_ia = json.loads(raw_content)
        except Exception:
            # Fallback caso a IA falhe em gerar o JSON (raro, mas protege o código)
            data_ia = {
                "feedback": response.choices[0].message.content,
                "mistakes": [],
                "tips": ["Pratique a frase pausadamente."]
            }

        # 4. Retorna o objeto Dataclass exatamente como o seu Router espera receber!
        return FeedbackResult(
            feedback=data_ia.get("feedback", ""),
            score=nota_matematica, # Mantém a nota calculada pelo seu algoritmo
            provider=self.provider,
            model=self.model,
            mistakes=data_ia.get("mistakes", []),
            tips=data_ia.get("tips", [])
        )

# A função de fábrica (Factory) que o seu router consome
def get_llm():
    return LLMService()