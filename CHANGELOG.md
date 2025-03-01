# Changelog - Projeto Análise Médica com IA

## [2025-02-23] - Migração de CrewAI para LangChain

### Alterações Principais
- Removida dependência do CrewAI
- Implementada nova arquitetura usando LangChain
- Otimizado uso de tokens e recursos

### Detalhes das Modificações

#### 1. Dependências (`requirements.txt`)
- Removido: `crewai[tools]>=0.100.0`
- Adicionado:
  - `langchain>=0.1.4`
  - `langchain-openai>=0.0.5`
  - `langchain-community>=0.0.16`
  - `langchain-core>=0.1.17`

#### 2. Ferramentas
- Criado novo arquivo `agents.py` com implementação dos agentes usando LangChain
- Atualizado `pubmed_tool.py` para usar o formato de ferramentas do LangChain
- Implementados limites de uso para controle de tokens e recursos

#### 3. Agentes Implementados
- Especialista em Anamnese
- Especialista em Exames
- Especialista em Diagnóstico
- Especialista em Tratamento

Cada agente agora utiliza:
- Limite máximo de tokens: 2000
- Temperatura: 0.3 (para respostas mais focadas)
- Máximo de 5 iterações
- Tempo máximo de execução: 60 segundos

#### 4. Interface (`app.py`)
- Melhorada a interface do usuário com Streamlit
- Adicionado tratamento de erros mais robusto
- Implementado feedback visual durante o processamento

### Como Executar o Projeto
1. Ative o ambiente virtual:
```bash
cd "c:\Users\arauj\Documents\CURSOS E PROJETOS\PROJETOS PYTHON COM CHATGPT\crewai_med-streamlit 2"
.\venv_new\Scripts\activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente no arquivo `.env`:
```
OPENAI_API_KEY=sua_chave_aqui
PUBMED_API_KEY=sua_chave_aqui
PUBMED_EMAIL=seu_email_aqui
```

4. Execute o aplicativo:
```bash
streamlit run app.py
```

### Próximos Passos
- [ ] Implementar cache para resultados frequentes
- [ ] Adicionar mais fontes de dados médicos
- [ ] Melhorar a formatação dos resultados
- [ ] Implementar sistema de feedback do usuário
