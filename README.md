# Sistema Escolar

Este é um sistema simples para o cadastro, atualização, deleção e consulta de informações relacionadas a alunos, endereços, disciplinas e notas. O front-end é feito com **Streamlit** e interage com um banco de dados MySQL. Ele permite fazer upload de arquivos para inserir dados nas tabelas, editar registros e gerar um PDF com as informações de notas dos alunos.

## Funcionalidades

- **Cadastro de Endereço**: Permite cadastrar um endereço com informações como CEP, endereço, cidade e estado.
- **Cadastro de Aluno**: Permite cadastrar alunos com informações como seu nome, email, cep e carro.
- **Cadastro de Nota**: Permite cadastrar notas para alunos e disciplinas.
- **Cadastro via upload de arquivo**:
- **Edição de Aluno**: Permite editar os dados (nome, email, cep e carro) de um aluno já cadastrado.
- **Geração de PDF**: Gera um PDF com a lista de notas dos alunos nas disciplinas.

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

