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
prompt = st.text_area("Caso queira, direcione o agente com suas preferências", height=160)
run_button = st.button("Run!")


# Definindo templates de prompt para o título do vídeo e o roteiro
blog_template = PromptTemplate(
    input_variables = ['transcription', 'article', 'prompt'], 
    template = """
    Atue como redador especializado em Copywriting, Escreva um post para um blog Wordpress resumindo a transcrição... {transcription}
    
    Utilize como referência de tom de voz o artigo... {article}

    Considere as observações do gerente de conteúdo na hora de gerar o conteúdo... {prompt}
    <regras>
     - O texto deve ter pelo menos 3000 caracteres
     - Não invente dados, utilize a transcrição como fonte de conhecimento
     - Termine o texto sempre provocando o leitor a interagir nos comentários com base em sua opinião.
    <regras>
    """
)

# Inicializa o estado do botão para clique automático
if "retry" not in st.session_state:
    st.session_state.retry = False

# Usando Session State para limpar resultados
if "generated" not in st.session_state:
    st.session_state.generated = None
    

# Quando o botão é clicado
if run_button or st.session_state.retry:
    # Limpa os resultados anteriores
    st.session_state.retry = False
    st.session_state.generated = None

    if link and link_ref_artigo:

        st.write('Gerando a transcrição do vídeo')
        loader = YoutubeLoader.from_youtube_url(
            link,
            add_video_info=False,
            language=["pt"]
        )
        result = loader.load()
        
        # Verifica se o primeiro item é um objeto do tipo Document
        if result and hasattr(result[0], 'page_content'):
            page_content = result[0].page_content  # Acessa o atributo diretamente

            st.write('Agora estamos gerando o texto do Blog, aguarde...')

            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
            # Configurando a cadeia de LLM para gerar títulos
            blog_chain = LLMChain(llm=llm, prompt=blog_template, verbose=True, output_key='post')
            st.write('Acessando referência para entender o tom de voz...')
            article = requests.get('https://r.jina.ai/'+link_ref_artigo, headers=headers)
            st.write('Preparando o conteúdo...')
            post = blog_chain.run(transcription=page_content, article=article.text, prompt=prompt)

            # Salva os resultados gerados no estado
            st.session_state.generated = {
                "page_content": page_content,
                "post": post
            }
        else:
            st.write("Não consegui acessar o link, vou tentar novamente...")
            st.session_state.retry = True
    else:
        st.write("Preencha os links corretamente...")

        # Exibe os resultados se estiverem no estado
    if "generated" in st.session_state and st.session_state.generated:
        with st.expander('Transcrição'):
            st.info(st.session_state.generated["page_content"])

        with st.expander('Post para Blog'):
            st.info(st.session_state.generated["post"])
