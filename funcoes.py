
#Front end para inserção, consulta, deleção e atualização de dados no db_escola: 

import streamlit as st 
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from fpdf import FPDF  
from dotenv import load_dotenv
import os


load_dotenv() #infos para a conexão com o banco de dados: host, port, user, senha e database_name

host = os.getenv("HOST")
port = os.getenv("PORT")
user = os.getenv("USER")
senha = os.getenv("PASSWORD")
database_name = os.getenv("DATABASE")


BASE_DIR = Path(__file__).parent 
DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)

with engine.connect() as conn: 
    df_alunos = pd.read_sql("SELECT * FROM tb_alunos", con=conn) # a partir da tb_alunos, crio um df_alunos 
    df_disciplinas = pd.read_sql("SELECT * FROM tb_disciplinas", con=conn) #crio df a partir de tb_disciplinas
    df_notas = pd.read_sql("SELECT * FROM tb_notas", con = conn)



#FUNÇÕES PARA CADA AÇÃO -->  interagindo com o banco de dados: 

#Upload de arquivo para cadastro: 
def subir_arquivo(uploaded_file,tabela):
    if uploaded_file is not None:  # Verifica se o arquivo foi carregado
        if uploaded_file.name.endswith('.csv'):
            tb = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            tb = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            tb = pd.read_json(uploaded_file)
        else:
                st.warning("O formato do arquivo é inválido")

        tb.to_sql(tabela, con=engine, if_exists='append', index=False)
        st.success(f"Dados inseridos na tabela {tabela} com sucesso!")

#1. cadastro de endereço (tb_endereco):
def cadastrar_endereco(params:dict):
    sql = text(
        """
INSERT INTO tb_enderecos (cep,endereco,cidade,estado)
VALUES (:cep, :endereco,:cidade, :estado) 
"""
    )
    with engine.begin() as conn:
        conn.execute(sql, params)

#2. cadastro de alunos (tb_alunos)
def cadastro_aluno(params:dict):
    sql = text(
        """
INSERT INTO tb_alunos (nome_aluno, email, cep, carro_id)
VALUES (:nome_aluno, :email, :cep, :carro_id)
""" 
    ) 
    with engine.begin() as conn:
        conn.execute(sql, params)

######fazer link com a tabela carros, para o usuário inserir o nome do carro, mas pegar o id desse carro para inserir/ editar na tabela alunos


#3. Edição de alunos: (atualização)
def editar_aluno(id_aluno, nome_aluno = None, email = None, cep = None, carro_id = None):
    #none para não ter que fornecer todos os parametros(no caso quando eu quero editar só 1 valor)

    with engine.begin() as conn: #conecta ao banco de dados 
        campos_atualizacao = [] #lista dos campos que serão atualizados (nomes das colunas das tabelas)
        params = {"id": id_aluno} #valores que serão passados para a query SQL 

        #if para ele entrar nos 4 campos e atualizar todos. Se fosse elif, a primeira condição a ser atendida seria a única. 
        if nome_aluno: #verifica se cada campo (parâmetros da função) foi passado 
            campos_atualizacao.append("nome_aluno = :nome_aluno")
            params["nome_aluno"] = nome_aluno  #adiciona ao dicionário params a chave "nome_aluno" e o valor nome_aluno (que é o que o usuário inseriu)
        if email:
            campos_atualizacao.append("email = :email")
            params["email"] = email
        if cep:
            campos_atualizacao.append("cep = :cep")
            params["cep"] = cep
        if carro_id:
            campos_atualizacao.append("carro_id = :carro_id")
            params["carro_id"] = carro_id 

        query = text(f"UPDATE tb_alunos  SET {','.join(campos_atualizacao)} WHERE id = :id")
        #join vai juntar os elementos de uma lista numa única string separando estes elementos com uma vírgula
        #usamos ele aqui para criar o comando com a sintaxe do SQL e executar a query. 
        result = conn.execute(query, params) #execução no banco 


#4. Cadastro de notas: 
def cadastrar_nota(params:dict):

    sql = text(
        """
INSERT INTO tb_notas (aluno_id, disciplina_id, nota)
VALUES (:aluno_id, :disciplina_id, :nota) 
"""
    )
    #os ":" são para formato dicionário. Ele se acha lá. Esses placeholders também são importantes para a prevenção contra SQL injection
    with engine.begin() as conn:        
        conn.execute(sql, params)


#5 Edição de notas (caso já exista uma nota cadastrada)
def editar_nota(params:dict):
    sql = text(
        """
UPDATE tb_notas  
SET nota = :nota
WHERE aluno_id = :aluno_id AND disciplina_id = :disciplina_id
"""
    )
    with engine.begin() as conn: #conecta ao banco de dados
        conn.execute(sql, params) #execução no banco 



#6 Gerar pdf com aluno, disciplina e nota: GPT 
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)

    pdf.cell(200, 10, "Notas dos Alunos", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 10)

    colunas = dados.columns.tolist()
    larguras = []

    for col in colunas:
        pdf.cell(60, 10, col, 1)
    pdf.ln()
    pdf.set_font("Arial", "", 8)
    for _, row in dados.iterrows():
        for item in row:
            pdf.cell(60, 10, str(item), 1)
        pdf.ln()
    return pdf.output(dest="S").encode("latin1")
