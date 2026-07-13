from ollama import chat

from .base import LLMService


class OllamaService(LLMService):

    def __init__(self):

        self.model = "llama3.1:8b"

    def generate_feedback(
        self,
        original,
        spoken,
        score,
    ):

        prompt = f"""
Frase original:

{original}

Aluno:

{spoken}

Nota:

{score}

Explique os erros de pronúncia,
dê sugestões de melhoria
e motive o aluno.
"""

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um professor de inglês."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content