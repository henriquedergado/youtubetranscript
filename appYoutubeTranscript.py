# Importando bibliotecas essenciais para o funcionamento do script
import streamlit as st # Importando a biblioteca Streamlit para criação de aplicações web
from langchain_community.document_loaders import YoutubeLoader

# Adicionar a imagem no cabeçalho
image_url = "https://www.seccoattuy.com.br/wp-content/uploads/2022/10/logo.png"
st.image(image_url, use_container_width=True)

# Adicionar o nome do aplicativo
st.subheader("Youtube transcripts - Secco Attui")
link = st.text_input('🔗 Digite o link do vídeo...') # Campo de entrada para o usuário escrever o tema

# Mostrando os resultados na tela se houver um prompt
if link:

    loader = YoutubeLoader.from_youtube_url(
        link, add_video_info=False
    )
    result = loader.load()

    st.write(result) # Exibe a transcrição gerada
