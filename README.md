# Projeto de Tratamento Médico com CrewAI

## Descrição
Este projeto utiliza CrewAI para criar um sistema de análise médica que ajuda a conduzir uma investigação clínica completa, desde a anamnese até o plano de tratamento.

## Histórico de Modificações

### 06/02/2025 (Segunda Revisão)
- Substituído WebsearchTool por SerplyWebSearchTool
- Adicionada configuração de API do Serply
- Mantido o modelo DeepSeek via Groq

### 06/02/2025 (Primeira Revisão)
- Revertido para o modelo DeepSeek via Groq
- Removidas dependências do OpenAI
- Mantido WebsearchTool para busca de evidências

### 06/02/2025
- Substituído PubMedTool por WebsearchTool do crewai_tools
- Migrado para OpenAI ChatGPT como modelo de linguagem
- Removido PubMedTool personalizado
- Adicionado suporte para busca web em tempo real

### 05/02/2025
- Criado `pubmed_tool.py` para buscar artigos científicos no PubMed
- Atualizado `main.py` para usar a nova ferramenta personalizada
- Adicionado suporte para busca de evidências científicas antes da análise dos agentes
- Removido `PubMedTool` do `crewai_tools`

## Configuração do Ambiente

### Requisitos
- Python 3.8+
- Bibliotecas listadas em `requirements.txt`

### Instalação
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Variáveis de Ambiente
Crie um arquivo `.env` com as seguintes variáveis:
- `GROQ_API_KEY`: Sua chave de API do Groq para DeepSeek
- `SERPLY_API_KEY`: Sua chave de API do Serply para busca web

## Execução
```bash
python main.py
```

## Estrutura do Projeto
- `main.py`: Script principal com a definição dos agentes e fluxo de trabalho
- `my_llm.py`: Configuração do modelo de linguagem DeepSeek
- `requirements.txt`: Dependências do projeto

## Contribuição
Por favor, leia as diretrizes de contribuição antes de submeter pull requests.

## Licença
[Especificar a licença]
