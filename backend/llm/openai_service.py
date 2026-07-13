from openai import OpenAI

from .base import LLMService


class OpenAIService(LLMService):

    def __init__(self):

        self.client = OpenAI()

    def generate_feedback(
        self,
        original,
        spoken,
        score,
    ):

        response = self.client.responses.create(
            model="gpt-5-mini",
            input=f"""
Frase original:

{original}

Aluno:

{spoken}

Nota:

{score}
"""
        )

        return response.output_text