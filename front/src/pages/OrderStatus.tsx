import { useEffect, useCallback, useState } from "react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { ShoppingCart, User, History, CircleUserRound, ChevronDown, LogOut, ArrowLeft, List } from "lucide-react";
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { useAuth } from "@/hooks/useAuth";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Table, TableHeader, TableCell, TableHead, TableBody, TableRow } from "@/components/ui/table";
import { usePedidoWebSocket } from "@/hooks/usePedidoWebSocket"; // "W" maiúsculo

interface Order {
    id: string;
    item: string;
    customizations: string;
    quantity: number;
    status: string;
}

const OrderStatus = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const [orders, setOrders] = useState<Order[]>([]);

    // Buscar pedidos do backend ao carregar a página
    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await fetch(`http://localhost:8000/pedidos/cliente/${user?.id ?? 1}`);
                const data = await response.json();
                console.log("Pedidos recebidos do backend:", data);

                // Transforma cada pedido e seus itens em linhas para a tabela
                const pedidosArray = data.pedidos || [];
                const pedidos: Order[] = [];
                pedidosArray.forEach((pedido: any) => {
                    pedido.itens.forEach((item: any, idx: number) => {
                        pedidos.push({
                            id: String(pedido.id) + "-" + idx,
                            item: item.bebida,
                            customizations: Array.isArray(item.ingredientes) && item.ingredientes.length > 0
                                ? item.ingredientes.join(", ")
                                : "Nenhuma",
                            quantity: 1, // ajuste se houver campo de quantidade
                            status: pedido.status
                        });
                    });
                });
                setOrders(pedidos);
            } catch (error) {
                console.error("Erro ao buscar pedidos:", error);
            }
        };
        fetchOrders();
    }, [user?.id]);

    // Função para atualizar o status do pedido ao receber mensagem do WebSocket
    const handleWebSocketMessage = useCallback((msg: any) => {
        if (msg.tipo === "atualizacao_pedido") {
            setOrders((prevOrders) =>
                prevOrders.map((order) =>
                    order.id === String(msg.id_pedido)
                        ? { ...order, status: msg.status }
                        : order
                )
            );
        }
    }, []);

    // Conecta ao WebSocket usando o id do usuário logado
    usePedidoWebSocket(user?.id ?? 1, handleWebSocketMessage);

    const handleLogout = () => {
        logout();
        window.location.reload();
    };

    return (
        <div className="flex flex-col min-h-screen bg-[#fff9f3]">
            <header className="bg-[#fff8e0]">
                <div className="max-w-6xl mx-auto px-2 sm:px-4 py-2 flex justify-between items-center">
                    <div className="logo-colorido flex items-center gap-3">
                        <img 
                        src="public/logo-bege.png"  
                        className="h-12"
                        alt="Logo Terra&Café" 
                        />
                    </div>
                    <div className="flex items-center gap-2">
                        <Button
                        variant="outline"
                        onClick={() => navigate("/order-status")}
                        className="hover:bg-[#e2ce87] rounded-full border-transparent bg-transparent text-[#754416]"
                        >
                        <List className="h-5 w-5 text-[#754416]" />
                        Acompanhar pedido
                        </Button>

                        <div className="flex items-center gap-4 text-[#754416]">
                            <DropdownMenu>
                            <DropdownMenuTrigger>
                                <Button className="hover:bg-[#e2ce87] rounded-full bg-[#d7dfaf] text-[#754416]">
                                <User className="h-4 w-4 mr-2" />
                                Olá, {user?.nome || 'Usuário'} 💛
                                <ChevronDown className="ml-2 h-4 w-4" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="w-48 bg-[#d7dfaf] text-[#754416] rounded-sm">
                                <DropdownMenuItem className="hover:bg-[#e2ce87]" onClick={() => navigate("/history")}>
                                <History className="h-4 w-4 mr-2" />
                                Histórico e Pontos
                                </DropdownMenuItem>
                                <DropdownMenuItem className="hover:bg-[#e2ce87]" onClick={() => handleLogout()}>
                                <LogOut className="h-4 w-4 mr-2" />
                                Sair
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                            </DropdownMenu>
                        </div>
                    </div>
                </div>
            </header>

            <div className="flex-grow max-w-7xl mx-auto">
                <div className="flex items-center my-6"> 
                    <Button
                        className="bg-[#f8e0b3] text-[#754416] hover:bg-[#] hover:text-white rounded-full px-4 py-2"
                        onClick={() => navigate("/")}
                    >
                        <ArrowLeft className="mr-2" />
                        Voltar
                    </Button>
                </div>
                <div>
                    <Card>
                        <CardHeader className="text-2xl text-orange-800">
                            Acompanhe seu pedido
                        </CardHeader>
                        <CardContent>
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>ID</TableHead>
                                        <TableHead>Item</TableHead>
                                        <TableHead>Customizações</TableHead>
                                        <TableHead>Quantidade</TableHead>
                                        <TableHead>Status</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {orders.map((order) => (
                                        <TableRow key={order.id}>
                                            <TableCell>{order.id}</TableCell>
                                            <TableCell>{order.item}</TableCell>
                                            <TableCell>{order.customizations}</TableCell>
                                            <TableCell>{order.quantity}</TableCell>
                                            <TableCell>{order.status}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                </div>
            </div>

            <footer className="bg-[#412a2b]">
                <div className="max-w-6xl mx-auto px-5 py-8 flex justify-evenly gap-6 items-center">
                <div className="max-w-xs">
                    <p className="text-[#f8e0b3]">
                    TERRA&CAFÉ
                    </p>
                    <h1 className="text-[#ff751f] text-2xl font-bold font-serif my-4">
                    Seu café, no seu tempo do seu jeitinho
                    </h1>
                    <p className="text-[#776c59]">
                    Todos os direitos reservados © 2025
                    </p>
                </div>
                <div className="justify-items-start max-w-xs">
                    <p className="text-[#ff751f] my-2">
                    Sobre Nós
                    </p>
                    <p className="text-[#f8e0b3]">
                    Conheça mais sobre a nossa história e missão.
                    </p>
                    <p className="text-[#f8e0b3]">
                    Contatos
                    </p>
                    <p className="text-[#f8e0b3]">
                    Endereços
                    </p>
                </div>
                </div>
            </footer>

        </div>
    );
};

export default OrderStatus;