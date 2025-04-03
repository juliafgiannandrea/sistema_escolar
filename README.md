# Sistema Escolar

Este é um sistema simples para o cadastro, atualização, deleção e consulta de informações relacionadas a alunos, endereços, disciplinas e notas. O front-end é feito com **Streamlit** e interage com um banco de dados **MySQL**.

### Criação e conexão do Banco de Dados: 
O banco de dados já com os relacionamentos entre as tabelas é criado pelo arquivo *create_db_escola.sql* e basta executá-lo no seu sistema de gerenciamento de banco de dados de preferência. Neste projeto, foi usado o MySQL e a conexão com o banco foi feita utilizando a biblioteca Python **sql alchemy**. 

Lembrando que para se fazer a conexão com o banco de dados é necessário fornecer: 
  1. HOST
  2. PORT
  3. USER
  4. PASSWORD 


A geração da interface gráfica para inserção, consulta, deleção e atualização de dados foi feita usando a biblioteca Python **Streamlit** e conta com 5 abas: "Cadastro endereço", "Cadastro aluno", "Cadastro nota", "Edição alunos", "Gerar pdf. 

## Funcionalidades: 
Foram feitas através das funções (no script *funcoes.py*).

As funções de cadastro e edição, exceto a de edição de alunos, recebem como parâmetro de entrada um dicionário. Na função de edição de alunos foi escolhido passar os parâmetros como variáveis para permitir que elas assumam valor *"None"* e possa ser feita a edição de 1 categoria por vez. 
- **Cadastro de Endereço**: Permite cadastrar um endereço > CEP, endereço, cidade e estado.
- **Cadastro de Aluno**: Permite cadastrar alunos > nome, email, cep e carro.
- **Cadastro de Nota**: Permite cadastrar notas para alunos em disciplinas.
- **Cadastro via upload de arquivo**: Permite o cadastro de informações na tabela do banco de dados via arquivo (.csv, .xlsx ou .json). 
- **Edição de Aluno**: Permite editar os dados (nome, email, cep e carro) de um aluno já cadastrado.
- **Geração de PDF**: Gera um PDF com a lista de notas dos alunos nas disciplinas. Para isso foi utilizada a biblioteca Python **FPDF**. 

## Tecnologias Utilizadas

- **Python**: Linguagem de programação.
- **Streamlit**: Framework para o desenvolvimento de front-end interativo.
- **SQLAlchemy**: Biblioteca para interação com o banco de dados MySQL.
- **FPDF**: Biblioteca para geração de PDFs.
- **MySQL**: Sistema de gerenciamento de banco de dados relacional.
- **Dotenv**: Carrega variáveis de ambiente a partir de um arquivo `.env` para configurar a conexão com o banco de dados.

## Pré-requisitos 

1. Python 3.x
2. MySQL (ou outro banco de dados compatível)
3. Bibliotecas necessárias (veja no Requirements.txt)
4. Criação de banco de dados db_escola

