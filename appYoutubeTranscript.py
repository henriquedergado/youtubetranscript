# Importando bibliotecas essenciais para o funcionamento do script
import streamlit as st # Importando a biblioteca Streamlit para criação de aplicações web
from langchain_community.document_loaders import YoutubeLoader

from langchain.llms import OpenAI # Importando o modelo de linguagem da OpenAI
from langchain.prompts import PromptTemplate # Importando a classe para templates de prompt
from langchain.chains import LLMChain, SequentialChain # Importando classes para criar cadeias de LLM
from langchain_openai import ChatOpenAI

# Configurando a chave de API da OpenAI no ambiente
os.environ['OPENAI_API_KEY'] = st.secrets["openai_api_key"]

# Adicionar a imagem no cabeçalho
image_url = "https://www.seccoattuy.com.br/wp-content/uploads/2022/10/logo.png"
st.image(image_url, width=300)

# Adicionar o nome do aplicativo
st.subheader("Youtube transcripts - Secco Attui")
link = st.text_input('🔗 Digite o link do vídeo...') # Campo de entrada para o usuário escrever o tema

# Definindo templates de prompt para o título do vídeo e o roteiro
blog_template = PromptTemplate(
    input_variables = ['transcription'], 
    template = """
    Atue como redador especializado em Copywriting, Escreva um post para um blog Wordpress resumindo a transcrição... {transcription}
    
    <regras>
     - O texto deve ter pelo menos 3000 caracteres
     - Termine o texto sempre provocando o leitor a interagir nos comentários com base em sua opinião.
    <regras>
    """
)

# Mostrando os resultados na tela se houver um prompt
if link:

    loader = YoutubeLoader.from_youtube_url(
        link,
        add_video_info=False,
        language=["pt"]
    )
    result = loader.load()
    # Verifica se o primeiro item é um objeto do tipo Document
    if hasattr(result[0], 'page_content'):
        page_content = result[0].page_content  # Acessa o atributo diretamente
        with st.expander('Transcrição'): 
            st.info(page_content)

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
        # Configurando a cadeia de LLM para gerar títulos
        blog_chain = LLMChain(llm=llm, prompt=blog_template, verbose=True, output_key='post')
        post = blog_chain.run(transcription=page_content)

        with st.expander('post para Blog'): 
            st.info(post)
    else:
        st.write("O atributo 'page_content' não está disponível no objeto.")
