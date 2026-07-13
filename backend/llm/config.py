import os
from openai import OpenAI

# ==========================================================
# CONFIGURAÇÃO GENÉRICA DE IA (OpenAI vs. Ollama)
# ==========================================================
# Busca as variáveis do ambiente ou usa padrões seguros
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # 'openai' ou 'ollama'
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")    # Ex: 'gpt-4o-mini' ou 'llama3'
LLM_API_KEY = os.getenv("LLM_API_KEY", "sua-chave-aqui")

# Define a URL de destino da API
if LLM_PROVIDER == "ollama":
    # Se for Ollama, aponta para o servidor local padrão do Ollama
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    # O Ollama exige uma API Key preenchida por causa do SDK, mesmo que seja um texto qualquer
    LLM_API_KEY = "ollama-local" 
else:
    # Se for OpenAI, usa a URL padrão da nuvem deles (None ativa o padrão do SDK)
    LLM_BASE_URL = None

# Inicializa o cliente de forma agnóstica (genérica)
client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL
)