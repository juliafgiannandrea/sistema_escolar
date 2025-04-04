
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
    df_alunos = pd.read_sql("SELECT * FROM tb_alunos", con=conn) #a partir da tb_alunos, crio um df_alunos 
    df_disciplinas = pd.read_sql("SELECT * FROM tb_disciplinas", con=conn) #crio df a partir de tb_disciplinas
    df_notas = pd.read_sql("SELECT * FROM tb_notas", con = conn)



#FUNÇÕES PARA CADA AÇÃO -->  interagindo com o banco de dados: 

#0. Upload de arquivo para cadastro: 
def subir_arquivo(uploaded_file,tabela):

    """
    Faz o upload de um arquivo CSV, XLSX ou JSON para uma tabela SQL.

    Parâmetros:
    - uploaded_file: Arquivo carregado pelo usuário.
    - tabela (str): Nome da tabela no banco de dados.

    A função lê o arquivo, insere os dados no banco e exibe mensagens de status.

    """

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
    """
    Insere um novo endereço na tabela 'tb_enderecos'.

    Parâmetros:
    - params (dict): Dicionário com 'cep', 'endereco', 'cidade' e 'estado'.

    Executa um comando SQL para adicionar o endereço ao banco de dados.

    """


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
    """
    Insere um novo aluno na tabela 'tb_alunos'.

    Parâmetros:
    - params (dict): Dicionário com 'nome_aluno', 'email', 'cep' e 'carro_id'.

    Executa um comando SQL para adicionar o aluno ao banco de dados.
    """

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


    """
    Atualiza os dados de um aluno na tabela 'tb_alunos'.

    Parâmetros:
    - id_aluno (int): ID do aluno a ser atualizado.
    - nome_aluno (str, opcional): Novo nome do aluno.
    - email (str, opcional): Novo e-mail do aluno.
    - cep (str, opcional): Novo CEP do aluno.
    - carro_id (int, opcional): Novo ID do carro do aluno.

    Apenas os campos fornecidos serão atualizados no banco de dados.
    """

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
    """
    Insere uma nova nota na tabela 'tb_notas'.

    Parâmetros:
    - params (dict): Dicionário com 'aluno_id', 'disciplina_id' e 'nota'.

    Executa um comando SQL para registrar a nota no banco de dados.
    """

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
    """
    Atualiza a nota de um aluno em uma disciplina na tabela 'tb_notas'.

    Parâmetros:
    - params (dict): Dicionário com 'aluno_id', 'disciplina_id' e 'nota'.

    Modifica a nota existente no banco de dados para os IDs especificados.
    """

    sql = text(
        """
UPDATE tb_notas  
SET nota = :nota
WHERE aluno_id = :aluno_id AND disciplina_id = :disciplina_id
"""
    )
    with engine.begin() as conn: #conecta ao banco de dados
        conn.execute(sql, params) #execução no banco 



#6 Gerar pdf com aluno, disciplina e nota: 
def gerar_pdf(dados:pd.DataFrame):
    """
    Gera um PDF com as notas dos alunos.

    Parâmetros:
    - dados (DataFrame): DataFrame contendo as notas dos alunos.

    Retorna:
    - PDF gerado em formato de bytes (codificação 'latin1').

    O PDF contém um cabeçalho e uma tabela com os dados fornecidos.
    """

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)

    pdf.cell(190, 10, "Notas dos Alunos", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "B", 10)

    colunas = dados.columns.tolist()
    largura_total = 190  # Largura máxima da página (A4)
    larguras = {
        "aluno_id": 20,
        "nome_aluno": 60,  
        "nome_disciplina": 60,  
        "nota": 20,
    }

    pdf.set_fill_color(200, 200, 200)

    for col in colunas:
        pdf.cell(larguras.get(col, 40), 8, col, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Arial", "", 9)

    for _, row in dados.iterrows():
        for col in dados.columns:
            texto = str(row[col])

            # Truncar texto longo para caber na célula
            if pdf.get_string_width(texto) > larguras[col] - 2:  
                texto = texto[:int(larguras[col] / 3)] + "..."  # Cortar texto e adicionar "..."

            pdf.cell(larguras[col], 8, texto, border=1, align="C")
        
        pdf.ln()
    return pdf.output(dest="S").encode("latin1")
