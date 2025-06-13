# CRUD Task API

Projeto desenvolvido em Python, responsável por fornecer a API Restful para gerenciamento de tarefas com operações CRUD e integração com banco de dados SQL server

## 📌 Tecnologias Utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-RESTx (Swagger UI)
- MySQL

## 📖 Funcionalidades

- Criar nova tarefa
- Listar todas as tarefas
- Consultar tarefa por ID
- Atualizar tarefa existente
- Deletar tarefa

## 📦 Como Executar

### 📑 Pré-requisitos:
- Python 3
- Flask
- SQL Server

### 📥 Clone o projeto

git clone https://github.com/brianbessa/CrudTaskAPI.git cd CrudTaskAPI

### ⚙️ Configure o appconfig, alterando o USUARIO, SENHA e nome_DB:

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://USUARIO:SENHA}@localhost/nome_DB"

### ▶️ Rode o projeto

python app.py

Acesse via Swagger localhost: http://127.0.0.1:5000/

![Image](https://github.com/user-attachments/assets/e5a9c59a-b669-43ab-aa44-65a911f378cc)
