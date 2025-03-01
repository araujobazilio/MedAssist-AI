from dotenv import load_dotenv
from agents import (
    create_anamnesis_agent,
    create_exam_agent,
    create_diagnosis_agent,
    create_treatment_agent
)
from typing import Dict
import os
import streamlit as st
import time
import re

# Load environment variables
load_dotenv()

def process_medical_condition(condition: str) -> Dict[str, str]:
    """
    Process a medical condition using a chain of specialized medical agents.
    
    Args:
        condition (str): The medical condition to analyze
        
    Returns:
        Dict[str, str]: Results from each specialist
    """
    # Criar contêineres para progresso e resultados
    progress_bar = st.progress(0, text="Iniciando análise médica...")
    status_container = st.empty()
    results_container = st.empty()

    try:
        # Initialize agents
        status_container.info(" Preparando agentes especializados...")
        time.sleep(1)
        progress_bar.progress(10, text="Carregando agentes especializados")

        anamnesis_agent = create_anamnesis_agent()
        exam_agent = create_exam_agent()
        diagnosis_agent = create_diagnosis_agent()
        treatment_agent = create_treatment_agent()

        # 1. Anamnesis
        status_container.info(" Agente de Anamnese iniciando análise...")
        progress_bar.progress(25, text="Realizando anamnese")
        time.sleep(1)

        anamnesis_prompt = f"""
        Você deve pesquisar especificamente sobre a condição: {condition}

        Sua tarefa é:
        1. Realizar uma busca no PubMed sobre "{condition}" focando em:
           - Sinais e sintomas principais
           - Manifestações clínicas
           - Progressão da doença

        2. Desenvolver um roteiro de anamnese específico para {condition} incluindo:
           - História da doença atual
           - Antecedentes pessoais e familiares relevantes
           - Hábitos e estilo de vida
           - Medicamentos em uso

        3. IMPORTANTE:
           - Use APENAS informações relacionadas a {condition}
           - Apresente o resultado em português
           - Organize de forma estruturada
           - INCLUA OS IDS DOS ARTIGOS DO PUBMED UTILIZADOS
        """

        anamnesis_result = anamnesis_agent.invoke({"input": anamnesis_prompt})

        # 2. Exams
        status_container.info(" Agente de Exames iniciando análise...")
        progress_bar.progress(50, text="Solicitando exames complementares")
        time.sleep(1)

        exam_prompt = f"""
        Com base na anamnese de {condition}, determine:
        1. Exames laboratoriais necessários
        2. Exames de imagem relevantes
        3. Outros exames complementares específicos
        4. INCLUA OS IDS DOS ARTIGOS DO PUBMED UTILIZADOS
        """

        exam_result = exam_agent.invoke({"input": exam_prompt})

        # 3. Diagnosis
        status_container.info(" Agente de Diagnóstico analisando resultados...")
        progress_bar.progress(75, text="Formulando diagnóstico")
        time.sleep(1)

        diagnosis_prompt = f"""
        Analise os resultados da anamnese e exames para {condition}:
        1. Confirmar ou refinar o diagnóstico
        2. Identificar possíveis diagnósticos diferenciais
        3. Avaliar estágio ou gravidade da condição
        4. INCLUA OS IDS DOS ARTIGOS DO PUBMED UTILIZADOS
        """

        diagnosis_result = diagnosis_agent.invoke({"input": diagnosis_prompt})

        # 4. Treatment
        status_container.info(" Agente de Tratamento elaborando plano...")
        progress_bar.progress(90, text="Desenvolvendo plano de tratamento")
        time.sleep(1)

        treatment_prompt = f"""
Com base no diagnóstico de {condition}, desenvolva um plano de tratamento DETALHADO com PRESCRIÇÃO MÉDICA:

1. FARMACOTERAPIA (Prescrição Médica Detalhada):
   a) Lista de medicamentos com:
      - Nome do princípio ativo
      - Nome comercial
      - DOSE EXATA (mg/kg ou mg)
      - FREQUÊNCIA de administração
      - VIA de administração
      - DURAÇÃO do tratamento
   
   b) Para cada medicamento, incluir:
      - Indicação precisa
      - Posologia detalhada
      - Faixa etária/peso
      - Ajustes de dose conforme necessário

2. ESQUEMA POSOLÓGICO COMPLETO:
   - Tabela de dosagem por:
     * Peso do paciente
     * Faixa etária
     * Condições específicas (rim, fígado)

3. INTERAÇÕES MEDICAMENTOSAS:
   - Listar potenciais interações
   - Medicamentos contraindicados
   - Ajustes necessários

4. EFEITOS COLATERAIS:
   - Efeitos esperados
   - Efeitos raros
   - Sinais de alerta para interromper medicação

5. MONITORAMENTO:
   - Exames de acompanhamento
   - Periodicidade de consultas
   - Sinais para buscar atendimento médico

6. TRATAMENTOS COMPLEMENTARES:
   - Terapias não farmacológicas
   - Mudanças no estilo de vida
   - Suporte nutricional/psicológico

IMPORTANTE:
- Baseie-se em PROTOCOLOS CLÍNICOS atualizados
- Considere VARIAÇÕES individuais
- Apresente em PORTUGUÊS CLARO
- Use LINGUAGEM TÉCNICA PRECISA
- FORMATAÇÃO em lista ou tabela para clareza

CONTEXTO ADICIONAL:
Diagnóstico prévio: {diagnosis_result["output"]}
- INCLUA OS IDS DOS ARTIGOS DO PUBMED UTILIZADOS
"""

        treatment_result = treatment_agent.invoke({"input": treatment_prompt})

        # Finalização
        status_container.success(" Análise médica concluída com sucesso!")
        progress_bar.progress(100, text="Análise completa")
        time.sleep(1)

        # Limpar contêineres temporários
        status_container.empty()

        # Retornar resultados
        return {
            "Anamnese": anamnesis_result["output"] + "\n\n" + extract_references(anamnesis_result),
            "Exames": exam_result["output"] + "\n\n" + extract_references(exam_result),
            "Diagnóstico": diagnosis_result["output"] + "\n\n" + extract_references(diagnosis_result),
            "Tratamento": format_treatment_result(treatment_result) + "\n\n" + extract_references(treatment_result)
        }

    except Exception as e:
        status_container.error(f"Erro durante a análise: {e}")
        progress_bar.progress(0)
        return {"Erro": str(e)}

def extract_references(agent_result):
    """
    Extrai referências de artigos científicos do resultado do agente
    
    Args:
        agent_result (dict): Resultado do agente com saída
    
    Returns:
        str: Referências formatadas
    """
    try:
        # Padrão para identificar referências de PubMed
        result_text = agent_result["output"]
        
        # Expressão para encontrar IDs de artigos PubMed
        import re
        pubmed_ids = re.findall(r'PubMed ID: (\d+)', result_text)
        
        # Se encontrou IDs, formata as referências
        if pubmed_ids:
            references = "###  Referências Científicas\n\n"
            for pmid in pubmed_ids[:5]:  # Limita a 5 referências
                references += f"- [PubMed ID: {pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)\n"
            return references
        
        return "###  Referências\nNenhuma referência científica identificada."
    
    except Exception as e:
        return f"Erro ao extrair referências: {str(e)}"

def format_treatment_result(treatment_result):
    """
    Formata o resultado do tratamento para melhor legibilidade
    
    Args:
        treatment_result (dict): Resultado do agente de tratamento
    
    Returns:
        str: Resultado formatado
    """
    try:
        # Parseie o resultado do tratamento
        result_text = treatment_result["output"]
        
        # Seções para destacar
        sections = [
            "1. FARMACOTERAPIA",
            "2. ESQUEMA POSOLÓGICO",
            "3. INTERAÇÕES MEDICAMENTOSAS", 
            "4. EFEITOS COLATERAIS",
            "5. MONITORAMENTO",
            "6. TRATAMENTOS COMPLEMENTARES"
        ]
        
        # Formatar resultado
        formatted_result = "##  Plano de Tratamento Detalhado\n\n"
        
        for section in sections:
            # Encontrar conteúdo de cada seção
            section_start = result_text.find(section)
            if section_start != -1:
                # Encontrar próxima seção ou fim do texto
                next_section_index = len(result_text)
                for next_section in sections[sections.index(section)+1:]:
                    next_index = result_text.find(next_section)
                    if next_index != -1:
                        next_section_index = min(next_section_index, next_index)
                
                # Extrair conteúdo da seção
                section_content = result_text[section_start:next_section_index].strip()
                
                # Adicionar ao resultado formatado
                formatted_result += f"### {section}\n"
                formatted_result += f"{section_content}\n\n"
        
        return formatted_result
    
    except Exception as e:
        return f"Erro ao formatar tratamento: {str(e)}"

def main_crew(condition: str) -> str:
    """
    Função principal para processar uma condição médica e retornar resultados formatados.
    """
    results = process_medical_condition(condition)
    
    if "Erro" in results:
        return results["Erro"]
    
    formatted_result = f"""
# Análise Médica - MedAssist AI

## 1. Anamnese e Avaliação Inicial
{results['Anamnese']}

## 2. Plano de Exames
{results['Exames']}

## 3. Análise Diagnóstica
{results['Diagnóstico']}

## 4. Plano Terapêutico
{results['Tratamento']}
"""
    
    return formatted_result

def main():
    st.title(" Assistente Médico com IA - MedAssist AI")
    
    condition = st.text_input("Digite a condição médica que deseja analisar:")
    
    if st.button("Analisar"):
        if condition:
            with st.spinner('Analisando a condição médica...'):
                results = main_crew(condition)
                st.markdown(results)
        else:
            st.warning("Por favor, digite uma condição médica para analisar.")

if __name__ == "__main__":
    main()
