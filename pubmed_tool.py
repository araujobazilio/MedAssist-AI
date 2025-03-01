from typing import Optional, Type
from langchain.tools import BaseTool
from Bio import Entrez
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

class PubMedSearchTool(BaseTool):
    """
    Ferramenta personalizada para buscar artigos no PubMed através das e-Utilities.
    Segue as recomendações do livro do CrewAI para integração de ferramentas.
    """
    name: str = "pubmed_search"
    description: str = """
    Useful for searching medical and scientific articles on PubMed.
    Input should be a search query string.
    Returns relevant articles with their titles, abstracts, and publication details.
    """
    
    api_key: str = os.getenv('PUBMED_API_KEY')
    email: str = os.getenv('PUBMED_EMAIL')
    Entrez.api_key = api_key
    Entrez.email = email

    def __init__(self):
        super().__init__()

    def _run(self, query: str, **kwargs) -> str:
        """
        Método interno para busca no PubMed.
        Retorna uma string formatada com os resultados da pesquisa.
        
        Args:
            query (str): Termo de busca para pesquisa no PubMed
            **kwargs: Argumentos adicionais (ignorados)
        
        Returns:
            str: Resultados formatados da pesquisa
        """
        try:
            # Melhora a query para resultados mais relevantes, mas menos restritiva
            enhanced_query = f"{query} AND (Review[ptyp] OR Clinical Trial[ptyp] OR Guideline[ptyp] OR Journal Article[ptyp])"
            
            # Search for articles
            handle = Entrez.esearch(db="pubmed", term=enhanced_query, retmax=5)
            record = Entrez.read(handle)
            handle.close()

            if not record['IdList']:
                return "No articles found for the given query."

            results = []
            # Fetch details for each article
            for article_id in record['IdList']:
                handle = Entrez.efetch(db="pubmed", id=article_id, rettype="abstract", retmode="text")
                article_text = handle.read()
                handle.close()
                
                # Adiciona uma linha em branco entre artigos para melhor legibilidade
                results.append(f"\n--- Artigo PubMed ID: {article_id} ---\n{article_text}\n")

            return "\n".join(results)

        except Exception as e:
            return f"Error searching PubMed: {str(e)}"

    def _arun(self, query: str):
        # For async operations - we'll use the sync version for now
        raise NotImplementedError("Async version not implemented")

    def run(self, query: str, **kwargs) -> str:
        """
        Método padrão do LangChain para execução da ferramenta.
        
        Args:
            query (str): Termo de busca para pesquisa no PubMed
            **kwargs: Argumentos adicionais (ignorados)
        
        Returns:
            str: Resultados formatados da pesquisa
        """
        return self._run(query, **kwargs)
