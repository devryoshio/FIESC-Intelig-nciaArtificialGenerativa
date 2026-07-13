from abc import ABC, abstractmethod

from .schemas import FeedbackResult


class LLMService(ABC):
    """
    Interface base para qualquer provedor de LLM.

    Toda implementação (Ollama, OpenAI, Gemini...)
    deve implementar este contrato.
    """

    @abstractmethod
    def generate_feedback(
        self,
        original: str,
        spoken: str,
        score: int,
    ) -> FeedbackResult:
        """
        Gera um feedback de pronúncia.

        Parameters
        ----------
        original : str
            Frase original.

        spoken : str
            Frase reconhecida.

        score : int
            Pontuação calculada pelo sistema.

        Returns
        -------
        FeedbackResult
            Estrutura padronizada com a resposta do LLM.
        """
        pass