import streamlit as st

# Página inicial
def page_home():
    st.title('Página Inicial')
    # Adicione widgets, gráficos, etc.

# Página de configurações
def page_settings():
    st.title('Configurações')
    # Adicione widgets para configurações

# Defina a sessão atual com base em algum estado ou variável
current_page = st.sidebar.radio('Navegação', ['Página Inicial', 'Configurações'])

# Renderize a página atual
if current_page == 'Página Inicial':
    page_home()
elif current_page == 'Configurações':
    page_settings()
