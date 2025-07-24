# TerraYCafe 🌱

Sistema completo para gestão de pedidos em uma cafeteria, utilizando FastAPI, SQLite e React.

## Funcionalidades
- Cadastro e autenticação de clientes
- Cardápio dinâmico 
- Personalização de bebidas
- Criação, alteração, cancelamento e acompanhamento de pedidos
- Atualização em tempo real do status do pedido
- Sistema de fidelidade e descontos

## Como rodar o projeto

### Backend (API)
1. Instale o Rye seguindo as instruções em [https://rye-up.com/](https://rye-up.com/)
2. Instale as dependências do projeto:
   ```bash
   rye sync
   ```
3. Execute o servidor:
   ```bash
   uvicorn backend.main:app --reload  ou
   fastapi dev main.py
   ```
4. Acesse a documentação Swagger em [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend (React)
1. Entre na pasta do frontend:
   ```bash
   cd frontend
   ```
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Execute o frontend:
   ```bash
   npm run dev
   ```

## Principais Tecnologias
- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- React
- WebSocket

## Padrões de Projeto Utilizados
 - Factory: Criação dinâmica de bebidas
 - Decorator: Personalização de bebidas
 - Command: Operações de pedido
 - Observer: Notificações em tempo real
 - Strategy: Cálculo de descontos e formas de pagamento
 - State: Gerenciamento do ciclo de vida e status do pedido

---
Projeto acadêmico desenvolvido para a disciplina de padões de projeto.
