
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ArrowLeft, Edit, Trash2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";

interface Customer {
  id: string;
  name: string;
  email: string;
  loyaltyPoints: number;
  phone: string;
}

const KitchenDiscounts = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  const [customers, setCustomers] = useState<Customer[]>([
    { id: "PROD001", name: "João", email: "joao.silva@email.com", loyaltyPoints: 5, phone: "3551-4532" },
    { id: "PROD002", name: "Bruna", email: "bruna.carvalho@email.com", loyaltyPoints: 10, phone: "1344-3266" },
    { id: "PROD003", name: "Zé Bentinho da Silva", email: "ze.bentinho.silva@email.com", loyaltyPoints: 5, phone: "3333-4523" },
    { id: "PROD004", name: "Marlene", email: "marlene@email.com", loyaltyPoints: 10, phone: "2344-2353" },
    { id: "PROD005", name: "Bruce Wave", email: "bruce.wave@email.com", loyaltyPoints: 10, phone: "2342-2342" },
    { id: "PROD006", name: "Gugu Liberato", email: "gugu.liberato@email.com", loyaltyPoints: 20, phone: "2342-3294" }
  ]);

  const getLoyaltyBadgeColor = (points: number) => {
    if (points >= 20) return "bg-purple-100 text-purple-800";
    if (points >= 10) return "bg-blue-100 text-blue-800";
    return "bg-green-100 text-green-800";
  };

  const getLoyaltyLevel = (points: number) => {
    if (points >= 20) return "VIP";
    if (points >= 10) return "Gold";
    return "Bronze";
  };

  // Função para editar cliente
  const handleEditCustomer = (customer: Customer) => {
    console.log("Editando cliente:", customer);
    toast({
      title: "Editar Cliente",
      description: `Funcionalidade de edição para ${customer.name} será implementada.`,
    });
  };

  // Função para deletar cliente
  const handleDeleteCustomer = (customer: Customer) => {
    console.log("Deletando cliente:", customer);
    setCustomers(prev => prev.filter(c => c.id !== customer.id));
    toast({
      title: "Cliente Removido",
      description: `${customer.name} foi removido da lista de fidelidade.`,
      variant: "destructive",
    });
  };

  // Função para editar programa de fidelidade
  const handleEditLoyaltyProgram = () => {
    console.log("Editando programa de fidelidade");
    toast({
      title: "Editar Programa",
      description: "Funcionalidade de edição do programa de fidelidade será implementada.",
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 to-orange-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <Button
            variant="outline"
            onClick={() => navigate("/kitchen")}
            className="border-orange-300 text-orange-700 hover:bg-orange-100"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Voltar
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-orange-800">Descontos</h1>
            <p className="text-orange-600">Programa de fidelidade dos clientes</p>
          </div>
        </div>

        {/* Customers Loyalty Section */}
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle className="text-2xl text-orange-800">
                Descontos de cada cliente 🧑‍🍳
              </CardTitle>
              <Button
                className="bg-orange-500 hover:bg-orange-600"
                onClick={handleEditLoyaltyProgram}
              >
                Editar Fidelidade
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Nome</TableHead>
                  <TableHead>Data</TableHead>
                  <TableHead>Pontos de Fidelidade</TableHead>
                  <TableHead>Telefone</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {customers.map((customer) => (
                  <TableRow key={customer.id}>
                    <TableCell>{customer.id}</TableCell>
                    <TableCell>{customer.name}</TableCell>
                    <TableCell>{customer.email}</TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getLoyaltyBadgeColor(customer.loyaltyPoints)}`}>
                          {getLoyaltyLevel(customer.loyaltyPoints)}
                        </span>
                        <span className="text-sm text-gray-600">
                          {customer.loyaltyPoints} pts
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>{customer.phone}</TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleEditCustomer(customer)}
                          title={`Editar ${customer.name}`}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => handleDeleteCustomer(customer)}
                          title={`Deletar ${customer.name}`}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* Loyalty Program Info */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle className="text-xl text-orange-800">
              Programa de Fidelidade - Níveis
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-green-50 p-4 rounded-lg border-2 border-green-200">
                <h3 className="font-bold text-green-800 mb-2">Bronze (0-9 pontos)</h3>
                <p className="text-green-700 text-sm">Cliente novo - sem desconto</p>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-200">
                <h3 className="font-bold text-blue-800 mb-2">Gold (10-19 pontos)</h3>
                <p className="text-blue-700 text-sm">5% de desconto em todos os produtos</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg border-2 border-purple-200">
                <h3 className="font-bold text-purple-800 mb-2">VIP (20+ pontos)</h3>
                <p className="text-purple-700 text-sm">10% de desconto + bebida grátis por mês</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default KitchenDiscounts;
