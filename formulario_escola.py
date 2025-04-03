import streamlit as st 
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from fpdf import FPDF  
from dotenv import load_dotenv
import os
from funcoes import subir_arquivo, cadastrar_endereco, cadastro_aluno, editar_aluno, cadastrar_nota, editar_nota, gerar_pdf


load_dotenv() #infos para a conexão com o banco de dados
host = os.getenv("HOST")
port = os.getenv("PORT")
user = os.getenv("USER")
senha = os.getenv("PASSWORD")
database_name = os.getenv("DATABASE")


BASE_DIR = Path(__file__).parent 
DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)

#A partir das tabelas no banco de dados, crio dataframes 
with engine.connect() as conn: 
    df_alunos = pd.read_sql("SELECT * FROM tb_alunos", con=conn) #a partir da tb_alunos, crio um df_alunos 
    df_disciplinas = pd.read_sql("SELECT * FROM tb_disciplinas", con=conn) #crio df a partir de tb_disciplinas
    df_notas = pd.read_sql("SELECT * FROM tb_notas", con = conn)


#Interface gráfica, onde vou chamar as funções: 
st.title("Meu sistema escolar")
menu = st.sidebar.selectbox("Selecione", ["Cadastro endereço", "Cadastro aluno", "Cadastro nota", "Edição alunos", "Gerar pdf"])


if menu == "Cadastro endereço":
    st.subheader("Cadastro de Endereço")
    cep = st.text_input("Cadastre o cep:")
    endereco = st.text_input("Cadastre o endereço:")
    cidade = st.text_input("Cadastre a cidade:")
    estado = st.text_input("Cadastre o estado:")
    tabela = "tb_endereco"

    params = {
        'cep': cep,
        'endereco':endereco,
        'cidade':cidade,
        'estado':estado,

    }

    if st.button("Cadastrar"):
        cadastrar_endereco(params)
        st.success("Endereço cadastrado com sucesso")

    ## Inserção via arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["csv", "xlsx", "json"])
    subir_arquivo(uploaded_file,tabela)
    
        
elif menu == "Cadastro aluno":
    st.subheader("Cadastro de Aluno")
    nome_aluno = st.text_input("Cadastre o nome_aluno:")
    email = st.text_input("Cadastre o email:")
    cep = st.text_input("Cadastre a cep:")
    carro_id = st.text_input("Cadastre o carro:")
    tabela = "tb_alunos"

    params = {
        'nome_aluno': nome_aluno,
        'email': email,
        'cep':cep,
        'carro_id': carro_id,

    }
    if st.button("Cadastrar"):
        cadastro_aluno(params)
        st.success("Aluno(a) cadastrado(a) com sucesso")
    ## Inserção via arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["csv", "xlsx", "json"])
    subir_arquivo(uploaded_file,tabela)


### fazer a mesma coisa que eu fiz para a edição nota  (selecionar o aluno e não mostrar o df no streamlit??)
elif menu == "Edição alunos":
    st.subheader("Edição alunos")
    st.dataframe(df_alunos)
    id = st.text_input("Digite o id do aluno que você quer editar:")
    nome = st.text_input("Digite o novo nome do aluno: ")
    email = st.text_input("Digite o novo email do aluno:")
    cep = st.text_input("Digite o cep")
    carro_id = st.text_input("Digite o carro: ")
    if st.button("Editar"):
        editar_aluno(id, nome, email, cep, carro_id) 
        st.success("Informações do aluno atualizadas")

   
elif menu == "Cadastro nota": 
    st.subheader("Cadastro de notas")
    
      
    nome_aluno = st.selectbox("Selecione o nome do aluno", df_alunos["nome_aluno"])
    id_aluno = df_alunos.loc[df_alunos['nome_aluno'] == nome_aluno, 'id'].values[0]  # Identificador do aluno

    nome_disciplina = st.selectbox("Selecione a disciplina", df_disciplinas["nome_disciplina"])
    id_disciplina = df_disciplinas.loc[df_disciplinas['nome_disciplina'] == nome_disciplina, 'id'].values[0] #identificador da disciplina
    #id_aluno e disciplina_id são chaves estrangeiras - pego seu correspondente nas tabelas correspondentes, que no caso eu transformei em data frames 

    input_nota = st.number_input("Digite a nota do aluno", min_value=0, max_value=10, value=7)


    params = {
        "aluno_id": id_aluno,
        "disciplina_id": id_disciplina,
        "nota": input_nota
    }

    tabela = "tb_notas"

    nota_existe = ((df_notas['aluno_id'] == id_aluno) & (df_notas['disciplina_id'] == id_disciplina)).any() #any me retorna um boolean; 
    # & realiza a operação elemento a elemento gerando 1 única série booleana (para cada linha do df)
    if nota_existe:
        st.warning("Já existe uma nota cadastrada para este aluno nesta disciplina.")        
        if st.button("Editar nota"):
            editar_nota(params)
            st.success("Nota editada com sucesso")

    else:
        if st.button("Cadastrar nota"):
                cadastrar_nota(params)
                st.success("Nota cadastrada com sucesso")

    
    ## Inserção via arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["csv", "xlsx", "json"])
    subir_arquivo(uploaded_file,tabela)


#Geração de pdf notas: 
elif menu == "Gerar pdf":
    st.subheader("Geração de pdf de notas")
    with engine.begin() as conn:
        conn.execute(text("DROP VIEW IF EXISTS notas_disciplinas_alunos"))

    sql = text(
            """
    CREATE VIEW notas_disciplinas_alunos AS SELECT tb_notas.aluno_id, tb_alunos.nome_aluno, tb_disciplinas.nome_disciplina,
    tb_notas.nota
    FROM tb_notas 
    INNER JOIN tb_alunos on tb_notas.aluno_id=tb_alunos.id
    INNER JOIN tb_disciplinas on tb_notas.disciplina_id = tb_disciplinas.id;
    """) 

    with engine.begin() as conn:
        conn.execute(sql)
        

    with engine.connect() as conn:
        df_pdf = pd.read_sql("SELECT * from notas_disciplinas_alunos", con=conn)
    st.dataframe(df_pdf) #exibição do df 
    pdf_bytes = gerar_pdf(df_pdf)

    st.download_button(
        label="Baixar PDF",
        data=pdf_bytes,
        file_name="notas_alunos.pdf",
        mime="application/pdf"
    )



###FALTA: 

#valor standard de nota cadastrada (o que está exibindo no streamlit como padrão) - fazer com que seja a nota atual
#fazer sumir o "já existe nota cadastrada" após apertar botão de editar nota 
 
#comentar as funções - boas práticas de programação --> doc string 
#tipo de variável do parâmetro de cada função 

#edição de aluno -- pegar o id de outra forma? (que nem eu fix para cadastro de notas)

#ajustes no pdf para formatação/ centralizar

#fazer link com a tabela carros, para o usuário inserir o nome do carro, mas pegar o id desse carro para inserir/ editar na tabela alunos
#fazer função de cadastro de carros 

#ajustes no front (visualmente, deixar mais user friendly)

#Read me 
#criação de banco de dados - passo a passo no readme 