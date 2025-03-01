import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage

# Carrega as variáveis do .env
load_dotenv()

class MyLLM:
    """Classe para gerenciar a instância do LLM de forma abstrata."""

    @staticmethod
    def GPT4():
        return ChatOpenAI(
            model_name="gpt-4o-mini",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.3,
            system_message=SystemMessage(content="""
            Você é um assistente de IA especializado em análise médica, 
            capaz de processar e interpretar informações médicas de forma precisa e detalhada.
            """)
        )
