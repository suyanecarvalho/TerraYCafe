from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
from terraycafe.controllers.rota_cliente import SECRET_KEY, ALGORITHM
from terraycafe.websocket.conexao import gerenciador_websocket
import json

router = APIRouter(prefix="/ws", tags=["WebSocket"])

# @router.websocket("/")
# async def websocket_endpoint(websocket: WebSocket):
#     await gerenciador_websocket.conectar(websocket)
#     try:  
#         while True:
#             await websocket.receive_text()  # Mantém conexão viva
#     except WebSocketDisconnect:
#         gerenciador_websocket.desconectar(websocket)

@router.websocket("/cliente/{id_cliente}")
async def websocket_cliente(websocket: WebSocket, id_cliente: int, token: str = Query(None)):
    # Validação do token JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        valor_sub = payload.get("sub")
        if not valor_sub or int(valor_sub) != id_cliente:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return
    await gerenciador_websocket.conectar(websocket, id_cliente=id_cliente)
    try:
        while True:
            dados = await websocket.receive_text()
            await websocket.send_text(json.dumps({"tipo": "pong", "mensagem": "Conectado como cliente"}))
    except WebSocketDisconnect:
        gerenciador_websocket.desconectar(websocket, id_cliente=id_cliente)

@router.websocket("/cozinha")
async def websocket_cozinha(websocket: WebSocket):
    await gerenciador_websocket.conectar(websocket, e_cozinha=True)
    try:
        while True:
            dados = await websocket.receive_text()
            await websocket.send_text(json.dumps({"tipo": "pong", "mensagem": "Conectado como cozinha"}))
    except WebSocketDisconnect:
        gerenciador_websocket.desconectar(websocket, e_cozinha=True)