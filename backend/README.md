# TerraYCafe Backend

Backend do sistema TerraYCafe - Sistema de gerenciamento de cafeteria.

## Descrição

Este é o backend da aplicação TerraYCafe, desenvolvido com Python e FastAPI, que gerencia:

- Clientes e autenticação
- Cardápio de bebidas e ingredientes
- Pedidos e personalizações
- Sistema de fidelidade

## Tecnologias

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Uvicorn** - Servidor ASGI
- **Pytest** - Testes unitários

## Estrutura do Projeto

```
backend/
├── src/
│   └── terraycafe/
│       ├── model/
│       │   └── sqlite/
│       │       ├── BO/          # Business Objects
│       │       ├── DAO/         # Data Access Objects
│       │       ├── entity/      # Entidades do banco
│       │       └── settings/    # Configurações
│       ├── controller/          # Controladores da API
│       └── view/               # Rotas e endpoints
├── test_cliente.py             # Testes
└── pyproject.toml              # Configuração do projeto
```
