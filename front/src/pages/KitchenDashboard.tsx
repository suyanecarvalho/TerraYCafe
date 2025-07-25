
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Clock, CheckCircle, XCircle, Coffee } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { OrderService } from "@/services/orderService";

interface Order {
  id: number;
  status: string;
  valor_total: number;
  forma_pagamento: string;
  desconto: number;
  data_hora: string;
  cliente_id: number;
}

const KitchenDashboard = () => {
  const navigate = useNavigate();
  const [currentTime, setCurrentTime] = useState(new Date());

  /*const [liveOrders, setLiveOrders] = useState<LiveOrder[]>([
    {
      id: "ORD001",
      customerName: "João Silva",
      items: ["Café Expresso", "Croissant"],
      status: "preparing",
      orderTime: "14:30",
      estimatedTime: 5
    },
    {
      id: "ORD002", 
      customerName: "Maria Santos",
      items: ["Cappuccino", "Pão de Queijo"],
      status: "pending",
      orderTime: "14:32",
      estimatedTime: 8
    },
    {
      id: "ORD003",
      customerName: "Pedro Costa",
      items: ["Suco de Laranja"],
      status: "ready",
      orderTime: "14:25",
      estimatedTime: 0
    }
  ]);*/

  const [liveOrders, setLiveOrders] = useState<Order[]>([]);

  useEffect(() => {
    fetchOrders();
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const updateOrderStatus = async (orderId: number) => {
    try {
      await OrderService.updateOrderStatus(orderId);
      fetchOrders();
    } catch (error) {
      console.error('Error updating order status:', error);
    }
  };

  const fetchOrders = async () => {
    try {
      const fetchedOrders = await OrderService.getOrderHistory();
      const filteredOrders = (fetchedOrders || []).filter(order => order.status !== "Cancelado");
      setLiveOrders(filteredOrders);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };

  const getStatusColor = (status: Order["status"]) => {
    switch (status) {
      case "pending":
        return "bg-yellow-100 border-yellow-300 text-yellow-800";
      case "preparing":
        return "bg-blue-100 border-blue-300 text-blue-800";
      case "ready":
        return "bg-green-100 border-green-300 text-green-800";
      case "delivered":
        return "bg-gray-100 border-gray-300 text-gray-800";
      default:
        return "bg-gray-100 border-gray-300 text-gray-800";
    }
  };

  const getStatusIcon = (status: Order["status"]) => {
    switch (status) {
      case "pending":
        return <Clock className="h-5 w-5" />;
      case "preparing":
        return <Coffee className="h-5 w-5" />;
      case "ready":
        return <CheckCircle className="h-5 w-5" />;
      case "delivered":
        return <CheckCircle className="h-5 w-5" />;
      default:
        return <Clock className="h-5 w-5" />;
    }
  };

  const getStatusText = (status: Order["status"]) => {
    switch (status) {
      case "pending":
        return "Aguardando";
      case "preparing":
        return "Preparando";
      case "ready":
        return "Pronto";
      case "delivered":
        return "Entregue";
      default:
        return "Aguardando";
    }
  };

  const recebidoOrders = liveOrders.filter(order => order.status === "Recebido");
  const preparandoOrders = liveOrders.filter(order => order.status === "Em preparo");
  const prontoOrders = liveOrders.filter(order => order.status === "Pronto");

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 to-orange-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              onClick={() => navigate("/kitchen")}
              className="border-orange-300 text-orange-700 hover:bg-orange-100"
            >
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-orange-800">Dashboard da Cozinha</h1>
              <p className="text-orange-600">Pedidos em tempo real</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-orange-800">
              {currentTime.toLocaleTimeString()}
            </div>
            <div className="text-orange-600">
              {currentTime.toLocaleDateString()}
            </div>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2">
                <Clock className="h-8 w-8 text-yellow-600" />
                <div>
                  <p className="text-2xl font-bold text-yellow-800">{recebidoOrders.length}</p>
                  <p className="text-sm text-yellow-600">Recebido</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2">
                <Coffee className="h-8 w-8 text-blue-600" />
                <div>
                  <p className="text-2xl font-bold text-blue-800">{preparandoOrders.length}</p>
                  <p className="text-sm text-blue-600">Preparando</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-8 w-8 text-green-600" />
                <div>
                  <p className="text-2xl font-bold text-green-800">{prontoOrders.length}</p>
                  <p className="text-sm text-green-600">Prontos</p>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-8 w-8 text-gray-600" />
                <div>
                  <p className="text-2xl font-bold text-gray-800">{liveOrders.length}</p>
                  <p className="text-sm text-gray-600">Total Hoje</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Live Orders */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Pending Orders */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl text-yellow-800 flex items-center gap-2">
                <Clock className="h-6 w-6" />
                Recebido ({recebidoOrders.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {recebidoOrders.map((order) => (
                <div
                  key={order.id}
                  className={`p-4 rounded-lg border-2 ${getStatusColor(order.status)}`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold">{order.cliente_id}</h3>
                    <span className="text-sm">{order.data_hora}</span>
                  </div>
                  <div className="space-y-1 mb-3">
                    {/*{order.items.map((item, index) => (
                      <p key={index} className="text-sm">• {item}</p>
                    ))}*/}
                  </div>
                  <Button
                    size="sm"
                    onClick={() => updateOrderStatus(order.id)}
                    className="w-full bg-blue-500 hover:bg-blue-600"
                  >
                    Começar Preparo
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Preparing Orders */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl text-blue-800 flex items-center gap-2">
                <Coffee className="h-6 w-6" />
                Preparando ({preparandoOrders.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {preparandoOrders.map((order) => (
                <div
                  key={order.id}
                  className={`p-4 rounded-lg border-2 ${getStatusColor(order.status)}`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold">{order.cliente_id}</h3>
                    <span className="text-sm">{order.data_hora}</span>
                  </div>
                  <div className="space-y-1 mb-3">
                    {/*{order.items.map((item, index) => (
                      <p key={index} className="text-sm">• {item}</p>
                    ))}*/}
                  </div>
                  <div className="text-sm mb-3">
                  </div>
                  <Button
                    size="sm"
                    onClick={() => updateOrderStatus(order.id)}
                    className="w-full bg-green-500 hover:bg-green-600"
                  >
                    Marcar como Pronto
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Ready Orders */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl text-green-800 flex items-center gap-2">
                <CheckCircle className="h-6 w-6" />
                Prontos ({prontoOrders.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {prontoOrders.map((order) => (
                <div
                  key={order.id}
                  className={`p-4 rounded-lg border-2 ${getStatusColor(order.status)}`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold">{order.cliente_id}</h3>
                    <span className="text-sm">{order.data_hora}</span>
                  </div>
                  <div className="space-y-1 mb-3">
                    {/*{order.items.map((item, index) => (
                      <p key={index} className="text-sm">• {item}</p>
                    ))}*/}
                  </div>
                  <div className="text-sm mb-3 text-green-700 font-medium">
                    ✅ Pronto para entrega!
                  </div>
                  <Button
                    size="sm"
                    onClick={() => updateOrderStatus(order.id)}
                    className="w-full bg-gray-500 hover:bg-gray-600"
                  >
                    Marcar como Entregue
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default KitchenDashboard;