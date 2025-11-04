# 🚗 Sistema de Aluguel de Veículos — Projeto Tóquio Final

Este projeto foi desenvolvido por **Gilberto Duarte Djacari** como parte do desafio final da formação. A aplicação é um sistema completo de aluguel de veículos com autenticação de usuários, controle de categorias e cadastro de aluguéis, utilizando o framework **Django**.

---

## 🧠 Objetivo do Sistema

O objetivo principal é permitir que clientes se cadastrem, façam login e aluguem veículos disponíveis conforme sua categoria de acesso (**Gold**, **Silver**, ou **Econômico**). O sistema gerencia veículos, clientes, aluguéis e cálculo de preços finais com base na quantidade de dias alugados.

---

## 🗂️ Modelagem de Dados

Abaixo estão os principais modelos utilizados no banco de dados:

### 🧑‍🤝‍🧑 Cliente

| Campo       | Tipo           | Descrição                                      |
|-------------|----------------|------------------------------------------------|
| `id`        | PK (int)       | Identificador único do cliente                |
| `nome`      | CharField      | Nome completo do cliente                      |
| `email`     | EmailField     | E-mail único para autenticação                |
| `senha`     | CharField      | Senha (armazenada com hashing)                |
| `categoria` | CharField      | Categoria do cliente (`gold`, `silver`, `econômico`) |

### 🚘 Veículo

| Campo          | Tipo           | Descrição                                      |
|----------------|----------------|------------------------------------------------|
| `id`           | PK (int)       | Identificador único do veículo                |
| `marca`        | CharField      | Fabricante do veículo                         |
| `modelo`       | CharField      | Modelo específico                             |
| `ano`          | IntegerField   | Ano de fabricação                             |
| `preco_diario` | DecimalField   | Valor do aluguel por dia                      |
| `disponivel`   | BooleanField   | Disponibilidade (`True`/`False`)              |

### 📄 Aluguel

| Campo          | Tipo           | Descrição                                      |
|----------------|----------------|------------------------------------------------|
| `id`           | PK (int)       | Identificador único do aluguel                |
| `cliente_id`   | FK (Cliente)   | Cliente que está realizando o aluguel         |
| `veiculo_id`   | FK (Veículo)   | Veículo selecionado                           |
| `data_inicio`  | DateField      | Data de início do aluguel                     |
| `data_fim`     | DateField      | Data de término do aluguel                    |
| `preco_total`  | DecimalField   | Valor total calculado                         |

---

## 🔐 Autenticação e Categorias

- O projeto utiliza o sistema de autenticação embutido do Django.
- Página de cadastro para novos clientes e login com credenciais.
- Clientes podem ser categorizados em **Gold**, **Silver** ou **Econômico**.
- O sistema restringe a visualização de veículos de acordo com a categoria do cliente.

---

## 🔁 Fluxo de Aluguel

1. Cliente faz login.
2. Sistema verifica a categoria e exibe os veículos disponíveis.
3. Cliente escolhe um veículo e seleciona as datas de início e fim.
4. O sistema calcula o valor total do aluguel com base nas datas e no valor diário do veículo.
5. O aluguel é registrado no banco de dados.
6. O veículo fica indisponível até o término do aluguel.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Django 4.x
- SQLite (padrão) ou outro banco compatível
- HTML, CSS e Bootstrap5 para o frontend

---

## 🚀 Como executar o projeto

### Requisitos:

- Python 3.8+
- Virtualenv (recomendado)

### Passos:

```bash
# Clonar o repositório
git clone https://github.com/gilbertodjacari/projeto-tokio-final.git
cd projeto-tokio-final

# Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações ao banco
python manage.py migrate

# Iniciar o servidor Django
python manage.py runserver
