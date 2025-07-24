from typing import List
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio

class GerenciadorWebSocket:
    def __init__(self):
        # Lista de conexões ativas
        self.conexoes_ativas: List[WebSocket] = []
        # Dicionário para conexões por cliente
        self.conexoes_cliente: dict[int, List[WebSocket]] = {}
        # Conexões da cozinha/admin
        self.conexoes_cozinha: List[WebSocket] = []

    async def conectar(self, websocket: WebSocket, id_cliente: int = None, e_cozinha: bool = False):
        """Conecta um novo WebSocket"""
        await websocket.accept()
        self.conexoes_ativas.append(websocket)
        
        if e_cozinha:
            self.conexoes_cozinha.append(websocket)
        elif id_cliente:
            if id_cliente not in self.conexoes_cliente:
                self.conexoes_cliente[id_cliente] = []
            self.conexoes_cliente[id_cliente].append(websocket)

    def desconectar(self, websocket: WebSocket, id_cliente: int = None, e_cozinha: bool = False):
        """Desconecta um WebSocket"""
        if websocket in self.conexoes_ativas:
            self.conexoes_ativas.remove(websocket)
        
        if e_cozinha and websocket in self.conexoes_cozinha:
            self.conexoes_cozinha.remove(websocket)
        elif id_cliente and id_cliente in self.conexoes_cliente:
            if websocket in self.conexoes_cliente[id_cliente]:
                self.conexoes_cliente[id_cliente].remove(websocket)
            if not self.conexoes_cliente[id_cliente]:
                del self.conexoes_cliente[id_cliente]

    async def enviar_mensagem_pessoal(self, mensagem: str, websocket: WebSocket):
        """Envia mensagem para um WebSocket específico"""
        try:
            await websocket.send_text(mensagem)
        except:
            # Remove conexão se falhar
            if websocket in self.conexoes_ativas:
                self.conexoes_ativas.remove(websocket)

    async def enviar_para_cliente(self, mensagem: dict, id_cliente: int):
        """Envia mensagem para todas as conexões de um cliente específico"""
        if id_cliente in self.conexoes_cliente:
            mensagem_str = json.dumps(mensagem)
            desconectados = []
            
            for websocket in self.conexoes_cliente[id_cliente]:
                try:
                    await websocket.send_text(mensagem_str)
                except:
                    desconectados.append(websocket)
            
            # Remove conexões mortas
            for ws in desconectados:
                self.conexoes_cliente[id_cliente].remove(ws)

    async def enviar_para_cozinha(self, mensagem: dict):
        """Envia mensagem para a cozinha"""
        mensagem_str = json.dumps(mensagem)
        desconectados = []
        
        for websocket in self.conexoes_cozinha:
            try:
                await websocket.send_text(mensagem_str)
            except:
                desconectados.append(websocket)
        
        # Remove conexões mortas
        for ws in desconectados:
            self.conexoes_cozinha.remove(ws)

    async def transmitir_para_todos(self, mensagem: dict):
        """Envia mensagem para todas as conexões ativas"""
        mensagem_str = json.dumps(mensagem)
        desconectados = []
        
        for websocket in self.conexoes_ativas:
            try:
                await websocket.send_text(mensagem_str)
            except:
                desconectados.append(websocket)
        
        # Remove conexões mortas
        for ws in desconectados:
            self.conexoes_ativas.remove(ws)

# Instância global do gerenciador
gerenciador_websocket = GerenciadorWebSocket()