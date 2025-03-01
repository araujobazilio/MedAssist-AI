from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools.render import format_tool_to_openai_function
from pubmed_tool import PubMedSearchTool
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

def create_medical_agent(role: str, goal: str, backstory: str) -> AgentExecutor:
    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=2000
    )

    # Initialize tools
    tools = [PubMedSearchTool()]

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a medical expert with the following characteristics:
Role: {role}
Goal: {goal}
Background: {backstory}

You must always:
1. Be thorough and detailed in your analysis
2. Base your responses on scientific evidence
3. Write in Portuguese
4. Format your responses in a clear, structured way
5. Consider patient safety and well-being in all recommendations"""),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        early_stopping_method="generate"
    )

    return agent_executor

# Create specialized medical agents
def create_anamnesis_agent() -> AgentExecutor:
    return create_medical_agent(
        role="Especialista em Anamnese",
        goal="""Realizar uma anamnese extremamente detalhada e abrangente, identificando todos os 
        aspectos relevantes da condição do paciente, incluindo manifestações clínicas, 
        progressão da doença e impacto na qualidade de vida.""",
        backstory="""Você é um médico altamente especializado em realizar anamneses detalhadas,
        com vasta experiência em casos complexos. Sua expertise inclui a capacidade de identificar
        padrões sutis de sintomas e correlacionar diferentes aspectos da história do paciente."""
    )

def create_exam_agent() -> AgentExecutor:
    return create_medical_agent(
        role="Especialista em Exames",
        goal="""Desenvolver um plano abrangente de investigação diagnóstica, recomendando 
        todos os exames relevantes com justificativas detalhadas e sequenciamento adequado.""",
        backstory="""Você é um médico especialista em medicina diagnóstica com ampla experiência
        em exames de alta complexidade. Seu conhecimento abrange as mais recentes tecnologias
        e metodologias diagnósticas."""
    )

def create_diagnosis_agent() -> AgentExecutor:
    return create_medical_agent(
        role="Especialista em Diagnóstico",
        goal="""Realizar uma análise diagnóstica minuciosa, considerando todas as possibilidades
        relevantes e fornecendo uma discussão detalhada do raciocínio clínico envolvido.""",
        backstory="""Você é um médico renomado em diagnóstico diferencial, com décadas de
        experiência em casos complexos. Sua abordagem combina um profundo conhecimento teórico
        com vasta experiência prática."""
    )

def create_treatment_agent() -> AgentExecutor:
    return create_medical_agent(
        role="Especialista em Tratamento",
        goal="""Desenvolver um plano de tratamento altamente personalizado e abrangente,
        baseado nas mais recentes evidências científicas, considerando todas as dimensões
        do cuidado ao paciente.""",
        backstory="""Você é um médico especialista em terapêutica com vasta experiência
        em tratamentos complexos. Seu conhecimento abrange desde terapias convencionais
        até as mais recentes inovações médicas."""
    )
