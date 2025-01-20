# Importando bibliotecas essenciais para o funcionamento do script
import os
import streamlit as st # Importando a biblioteca Streamlit para criação de aplicações web
from langchain_community.document_loaders import YoutubeLoader
import requests # Importando a biblioteca para realizar requisições HTTP

# Adicionar a imagem no cabeçalho
image_url = "https://www.seccoattuy.com.br/wp-content/uploads/2022/10/logo.png"
st.image(image_url, width=300)

# Adicionar o nome do aplicativo
st.subheader("Youtube transcript")
link = st.text_input('🔗 Digite o link do Youtube para transcrição...') # Campo de entrada para o usuário escrever o tema

# Campo de seleção de idioma
language_options = {
    "Português": "pt",
    "Inglês": "en",
    "Espanhol": "es",
}
language = st.selectbox(
    "🌐 Escolha o idioma do vídeo:",
    options=list(language_options.keys()),
    index=0  # Padrão: Português
)

run_button = st.button("Run!")

# Quando o botão é clicado
if run_button and link:
    st.write('Gerando a transcrição do vídeo')
    selected_language = language_options[language]
    loader = YoutubeLoader.from_youtube_url(
        link,
        add_video_info=False,
        language=[selected_language]
    )
    result = loader.load()

    while not result:
        result = loader.load()
        
    # Verifica se o primeiro item é um objeto do tipo Document
    if result and hasattr(result[0], 'page_content'):
        page_content = result[0].page_content  # Acessa o atributo diretamente
        with st.expander('Transcrição'):
            st.info(page_content)
        
    else:
        st.write("Preencha os links corretamente...")
