import os
import json
from openai import OpenAI
# Importa o FeedbackResult lá do seu arquivo de schemas
from schemas import FeedbackResult 

class LLMService:
    def __init__(self):
        # Configuração simplificada focada exclusivamente na OpenAI
        self.provider = "openai"
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=os.getenv("LLM_API_KEY"))

    def generate_feedback(self, phrase_original: str, frase_aluno: str, nota_matematica: int) -> FeedbackResult:
        # 1. Carrega o System Prompt estruturado
        with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        user_content = f"Frase Correta: {phrase_original}\nO que o aluno falou: {frase_aluno}\nNota Inicial: {nota_matematica}%"

        # 2. Chamada usando o cliente oficial da OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}, # Força o modelo a responder em JSON puro
            max_tokens=500,
            temperature=1
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
        
        print(data_ia)
        # 4. Retorna o objeto Dataclass exatamente como o seu Router espera receber!
        return FeedbackResult(
            feedback=data_ia.get("feedback", ""),
            score=nota_matematica,
            provider=self.provider,
            model=self.model,
            mistakes=data_ia.get("mistakes", []),
            phonetics=data_ia.get("phonetics", {}),
            tips=data_ia.get("tips", [])
        )

# A função de fábrica (Factory) que o seu router consome
def get_llm():
    return LLMService()