# Importando bibliotecas essenciais para o funcionamento do script
import os
import streamlit as st # Importando a biblioteca Streamlit para criação de aplicações web
from langchain_community.document_loaders import YoutubeLoader

from langchain.llms import OpenAI # Importando o modelo de linguagem da OpenAI
from langchain.prompts import PromptTemplate # Importando a classe para templates de prompt
from langchain.chains import LLMChain, SequentialChain # Importando classes para criar cadeias de LLM
from langchain_openai import ChatOpenAI
import requests # Importando a biblioteca para realizar requisições HTTP

# Configurando a chave de API da OpenAI no ambiente
os.environ['OPENAI_API_KEY'] = st.secrets["openai_api_key"]

headers = {
    'Authorization': 'Bearer ' + st.secrets["jina_api_key"] 
}

# Adicionar a imagem no cabeçalho
image_url = "https://www.seccoattuy.com.br/wp-content/uploads/2022/10/logo.png"
st.image(image_url, width=300)

# Adicionar o nome do aplicativo
st.subheader("Youtube transcripts - Wordpress Blog generator")
link = st.text_input('🔗 Digite o link do Youtube para transcrição...') # Campo de entrada para o usuário escrever o tema
link_ref_artigo = st.text_input('🔗 Digite o link de um post para referência de tom de voz...')
run_button = st.button("Run!")

# Definindo templates de prompt para o título do vídeo e o roteiro
blog_template = PromptTemplate(
    input_variables = ['transcription', 'article'], 
    template = """
    Atue como redador especializado em Copywriting, Escreva um post para um blog Wordpress resumindo a transcrição... {transcription}
    
    Utilize como referência de tom de voz o artigo... {article}
    <regras>
     - O texto deve ter pelo menos 3000 caracteres
     - Não invente dados, utilize a transcrição como fonte de conhecimento
     - Termine o texto sempre provocando o leitor a interagir nos comentários com base em sua opinião.
    <regras>
    """
)

# Mostrando os resultados na tela se houver um prompt
if run_button and link and link_ref_artigo:

    loader = YoutubeLoader.from_youtube_url(
        link,
        add_video_info=False,
        language=["pt"]
    )
    result = loader.load()
    # Verifica se o primeiro item é um objeto do tipo Document
    if hasattr(result[0], 'page_content'):
        page_content = result[0].page_content  # Acessa o atributo diretamente

        st.write('Aqui está a transcrição do vídeo')
        with st.expander('Transcrição'): 
            st.info(page_content)

        st.write('Agora estamos gerando o texto do Blog, aguarde...')

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
        # Configurando a cadeia de LLM para gerar títulos
        blog_chain = LLMChain(llm=llm, prompt=blog_template, verbose=True, output_key='post')
        article = requests.get('https://r.jina.ai/'+link_ref_artigo, headers=headers)
        post = blog_chain.run(transcription=page_content, article=article.text)

        with st.expander('post para Blog'): 
            st.info(post)
    else:
        st.write("O atributo 'page_content' não está disponível no objeto.")
