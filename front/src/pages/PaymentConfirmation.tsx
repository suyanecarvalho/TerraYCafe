
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle, Home, History } from "lucide-react";
import { useNavigate } from "react-router-dom";

const PaymentConfirmation = () => {
  const navigate = useNavigate();

  // Auto redirect after 5 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/");
    }, 5000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-green-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md text-center">
        <CardHeader>
          <div className="flex justify-center mb-4">
            <CheckCircle className="h-16 w-16 text-green-500" />
          </div>
          <CardTitle className="text-2xl text-green-700">
            Pagamento Confirmado!
          </CardTitle>
          <CardDescription className="text-lg">
            Seu pedido foi realizado com sucesso
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-green-700 font-medium mb-2">
              ✅ Pedido confirmado
            </p>
            <p className="text-green-600 text-sm">
              Seu café estará pronto em breve!
            </p>
          </div>

          <div className="text-sm text-gray-600">
            Você será redirecionado automaticamente em 5 segundos...
          </div>

          <div className="flex gap-3">
            <Button
              variant="outline"
              className="flex-1"
              onClick={() => navigate("/history")}
            >
              <History className="h-4 w-4 mr-2" />
              Ver Histórico
            </Button>
            <Button
              className="flex-1 bg-orange-500 hover:bg-orange-600"
              onClick={() => navigate("/")}
            >
              <Home className="h-4 w-4 mr-2" />
              Início
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PaymentConfirmation;
