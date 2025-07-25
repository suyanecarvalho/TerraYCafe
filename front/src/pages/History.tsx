
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface OrderItem {
  id: string;
  date: string;
  items: {
    name: string;
    quantity: number;
    customizations: string[];
    price: number;
  }[];
  total: number;
  status: "entregue" | "preparando" | "cancelado";
}

const mockOrders: OrderItem[] = [
  {
    id: "1",
    date: "2024-01-15",
    items: [
      {
        name: "Café com Leite de amêndoas, Com açúcar",
        quantity: 1,
        customizations: ["Leite de amêndoas", "Com açúcar"],
        price: 16.50
      }
    ],
    total: 16.50,
    status: "entregue"
  },
  {
    id: "2", 
    date: "2024-01-14",
    items: [
      {
        name: "Café com Leite de amêndoas, Com açúcar",
        quantity: 1,
        customizations: ["Leite de amêndoas", "Com açúcar"],
        price: 16.50
      }
    ],
    total: 16.50,
    status: "entregue"
  },
  {
    id: "3",
    date: "2024-01-13", 
    items: [
      {
        name: "Café com Leite de amêndoas, Com açúcar",
        quantity: 1,
        customizations: ["Leite de amêndoas", "Com açúcar"],
        price: 16.50
      }
    ],
    total: 16.50,
    status: "preparando"
  }
];

const History = () => {
  const navigate = useNavigate();

  const getStatusColor = (status: string) => {
    switch (status) {
      case "entregue":
        return "bg-green-100 text-green-800";
      case "preparando":
        return "bg-yellow-100 text-yellow-800";
      case "cancelado":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 to-orange-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center gap-4">
          <Button
            variant="ghost"
            onClick={() => navigate("/")}
            className="p-2"
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <h1 className="text-2xl font-bold text-orange-800">Histórico de Pedidos</h1>
        </div>
      </header>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-gradient-to-r from-orange-200 to-yellow-200 rounded-lg p-6 mb-8 text-center">
          <div className="text-4xl mb-2">👩🏽‍🍳</div>
          <h2 className="text-2xl font-bold text-orange-800 mb-1">
            O tradicional bem feito
          </h2>
          <p className="text-orange-700">
            com muito carinho 🧡
          </p>
        </div>

        <div className="space-y-6">
          <h3 className="text-2xl font-bold text-orange-800">
            Total de Pontos: 350
          </h3>
          
          <h3 className="text-xl font-bold text-orange-800">
            Esse é o seu Histórico com a gente 😊
          </h3>

          {/* Tabela de pedidos */}
          <div className="bg-white rounded-lg shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-yellow-100">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Pedido</th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Data</th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Quantidade</th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Total</th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-700">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {mockOrders.map((order) => (
                    <tr key={order.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="space-y-1">
                          {order.items.map((item, index) => (
                            <div key={index} className="text-sm">
                              <p className="font-medium">{item.name}</p>
                              {item.customizations.length > 0 && (
                                <div className="flex flex-wrap gap-1 mt-1">
                                  {item.customizations.map((custom, i) => (
                                    <Badge key={i} variant="secondary" className="text-xs">
                                      {custom}
                                    </Badge>
                                  ))}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {new Date(order.date).toLocaleDateString('pt-BR')}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {order.items.reduce((sum, item) => sum + item.quantity, 0)}
                      </td>
                      <td className="px-6 py-4 text-sm font-medium">
                        R$ {order.total.toFixed(2)}
                      </td>
                      <td className="px-6 py-4">
                        <Badge className={`${getStatusColor(order.status)} border-0`}>
                          {order.status.toUpperCase()}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default History;
