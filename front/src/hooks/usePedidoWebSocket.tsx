// src/hooks/usePedidoWebSocket.tsx
import { useEffect, useRef } from "react";

export function usePedidoWebSocket(idCliente: number, onMessage: (msg: any) => void) {
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Exemplo de conexão WebSocket
    const token = localStorage.getItem('token');
    const userId = idCliente;
    ws.current = new WebSocket(`ws://localhost:8000/ws/cliente/${userId}?token=${token}`);
   
    ws.current.onopen = () => {
      console.log("WebSocket conectado!");
      ws.current?.send("ping");
    };

    ws.current.onmessage = (event) => {
      const dados = JSON.parse(event.data);
      onMessage(dados);
    };

    ws.current.onclose = () => {
      console.log("WebSocket desconectado!");
    };

    ws.current.onerror = (err) => {
      console.error("WebSocket erro:", err);
    };

    return () => {
      ws.current?.close();
    };
  }, [idCliente, onMessage]);
}