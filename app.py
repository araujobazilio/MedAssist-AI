import streamlit as st
from main import main_crew, process_medical_condition

# Load environment variables
# load_dotenv()

# Configure page
st.set_page_config(
    page_title="MedAssist AI",
    page_icon="🩺",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .output-container {
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title and description
    st.title("🩺 MedAssist AI")
    st.markdown("""
    Bem-vindo ao **MedAssist AI**, seu assistente inteligente de análise médica. 
    Este aplicativo utiliza Inteligência Artificial para realizar uma análise médica completa 
    de uma condição ou doença, com agentes especializados que trabalham em conjunto 
    para fornecer uma visão abrangente e detalhada do caso.
    """)

    # Input section
    with st.container():
        st.subheader("📝 Entrada de Dados")
        condition = st.text_input(
            "Digite a condição médica que deseja analisar:",
            placeholder="Ex: diabetes tipo 2, hipertensão, asma..."
        )

    # Process button
    if st.button("🔍 Realizar Análise", type="primary"):
        if condition:
            # Chama a função de processamento
            results = process_medical_condition(condition)
            
            # Verifica se há resultados
            if results and "Erro" not in results:
                # Cria abas para cada etapa
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📋 Anamnese", 
                    "🔬 Exames", 
                    "🩺 Diagnóstico", 
                    "💊 Tratamento"
                ])
                
                with tab1:
                    st.subheader("Relatório de Anamnese")
                    st.write(results.get("Anamnese", "Sem informações"))
                
                with tab2:
                    st.subheader("Exames Recomendados")
                    st.write(results.get("Exames", "Sem recomendações"))
                
                with tab3:
                    st.subheader("Análise Diagnóstica")
                    st.write(results.get("Diagnóstico", "Sem diagnóstico"))
                
                with tab4:
                    st.subheader("Plano de Tratamento")
                    st.write(results.get("Tratamento", "Sem plano de tratamento"))
            
            else:
                st.error("Não foi possível processar a condição médica.")
        else:
            st.warning("Por favor, insira uma condição médica.")

    # Rodapé
    st.markdown("""
---
🤖 Desenvolvido com CrewAI e OpenAI | Uso exclusivo para pesquisa médica
""")

if __name__ == "__main__":
    main()
