
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ChefHat, Package, Users, Percent, History, Settings } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";

const Kitchen = () => {
  const navigate = useNavigate();

  const menuCards = [
    {
      title: "Ver a cozinha",
      description: "Dashboard de pedidos em tempo real",
      icon: ChefHat,
      path: "/kitchen/dashboard",
      color: "bg-green-100 hover:bg-green-200"
    },
    {
      title: "Histórico de Pedidos",
      description: "Visualizar pedidos anteriores",
      icon: History,
      path: "/kitchen/orders-history",
      color: "bg-blue-100 hover:bg-blue-200"
    },
    {
      title: "Descontos",
      description: "Gerenciar promoções e descontos",
      icon: Percent,
      path: "/kitchen/discounts",
      color: "bg-yellow-100 hover:bg-yellow-200"
    },
    {
      title: "Ingredientes e Produtos",
      description: "Gerenciar ingredientes e produtos",
      icon: Package,
      path: "/kitchen/ingredients",
      color: "bg-orange-100 hover:bg-orange-200"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 to-orange-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <ChefHat className="h-12 w-12 text-orange-600" />
            <h1 className="text-4xl font-bold text-orange-800">Terra&Café</h1>
          </div>
          <p className="text-xl text-orange-700">Sistema da Cozinha</p>
          <p className="text-lg text-orange-600">Seu café, no seu tempo, do seu jeitinho ☕</p>
        </div>

        {/* Menu Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {menuCards.map((card, index) => (
            <Card 
              key={index}
              className={`cursor-pointer transition-all duration-200 ${card.color} border-2 hover:border-orange-300 hover:shadow-lg`}
              onClick={() => navigate(card.path)}
            >
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  <card.icon className="h-16 w-16 text-orange-700" />
                </div>
                <CardTitle className="text-2xl text-orange-800">
                  {card.title}
                </CardTitle>
                <CardDescription className="text-lg text-orange-600">
                  {card.description}
                </CardDescription>
              </CardHeader>
            </Card>
          ))}
        </div>

        {/* Footer */}
        <div className="text-center">
          <Button
            variant="outline"
            onClick={() => navigate("/kitchenlogin")}
            className="border-orange-300 text-orange-700 hover:bg-orange-100"
          >
            <LogOut className="h-4 w-4 mr-2" />
            Sair
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Kitchen;
