import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Plus, Minus, Trash2, Pencil } from "lucide-react";
import { PaymentModal } from "./PaymentModal";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { useOrder } from "@/hooks/useOrder";
import { useCart } from "@/hooks/useCart";
import { CartItem } from "@/models/Drink";
import { OrderService } from "@/services/orderService";

interface CartProps {
  items: CartItem[];
  isOpen: boolean;
  onClose: () => void;
  onUpdateCart: (items: CartItem[]) => void;
  onEditItem: (item: CartItem, index: number) => void;
}

export const Cart = ({ items, isOpen, onClose, onUpdateCart, onEditItem }: CartProps) => {
  const [showPayment, setShowPayment] = useState(false);
  const navigate = useNavigate();
  
  const { user } = useAuth();
  const { processOrder } = useOrder();
  const { getTotalPrice } = useCart();

  const updateQuantity = (index: number, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeItem(index);
      return;
    }
    
    const updatedItems = [...items];
    const item = updatedItems[index];
    const pricePerUnit = item.totalPrice / item.quantity;
    updatedItems[index] = {
      ...item,
      quantity: newQuantity,
      totalPrice: pricePerUnit * newQuantity
    };
    onUpdateCart(updatedItems);
  };

  const removeItem = (index: number) => {
    const updatedItems = items.filter((_, i) => i !== index);
    onUpdateCart(updatedItems);
  };

  const editItem = (index: number) => {
    const item = items[index];
    onEditItem(item, index);
  };

  const getCurrentTotal = () => {
    return items.reduce((total, item) => total + item.totalPrice, 0);
  };

  const handlePaymentComplete = async (forma_pagamento?: string) => {
    const total = getCurrentTotal();
    console.log("Iniciando pagamento. Total:", total, "Forma de pagamento:", forma_pagamento);

    try {
      // Prepara cada bebida no backend
      for (const item of items) {
        console.log("Preparando item:", item);
        const result = await OrderService.orderOnCart(
          user.id,
          item.drink,
          item.customizations
        );
        if (!result) {
          alert("Erro ao preparar bebida. Pedido não será criado.");
          return;
        }
      }

      // Cria o pedido principal
      console.log("Criando pedido para cliente:", user.id, "com forma de pagamento:", forma_pagamento);
      const pedidoResult = await OrderService.createOrder(user.id, forma_pagamento || "Dinheiro");
      console.log("Resultado criação do pedido:", pedidoResult);

      onUpdateCart([]);
      setShowPayment(false);
      navigate("/payment-confirmation");
    } catch (error) {
      alert("Erro ao finalizar pedido. Tente novamente.");
      console.error("Erro no pagamento:", error);
    }
  };

  const handleCheckout = () => {
    if (!user) {
      onClose();
      navigate("/login");
    } else {
      setShowPayment(true);
    }
  };

  if (items.length === 0) {
    return (
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="max-w-md mx-auto">
          <DialogHeader>
            <DialogTitle className="text-center">Carrinho</DialogTitle>
          </DialogHeader>
          <div className="text-center py-8">
            <div className="text-4xl mb-4">🛒</div>
            <p className="text-gray-600">Seu carrinho está vazio</p>
          </div>
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <>
      <Dialog open={isOpen} onOpenChange={onClose}>
        <DialogContent className="mx-auto max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-center">O que você está levando 🛒</DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Header da tabela */}
            <div className="grid grid-cols-13 gap-2 text-sm font-medium text-gray-600 border-b pb-2">
              <div className="col-span-4 col-start-1">Item</div>
              <div className="col-span-3 col-start-5">Adicionais</div>
              <div className="col-span-2 col-start-8">Quantidade</div>
              <div className="col-span-2 col-start-10">Preço</div>
              <div className="col-span-2 col-start-12"></div>
            </div>

            {/* Items do carrinho */}
            {items.map((item, index) => (
              <div key={index} className="grid grid-cols-13 gap-2 items-start py-3 border-b">
                <div className="col-span-4 col-start-1 flex items-center gap-2">
                  <span className="text-2xl">{item.drink.image}</span>
                  <div>
                    <p className="font-medium text-sm">{item.drink.nome}</p>
                  </div>
                </div>
                
                <div className="col-span-3 col-start-5">
                  {item.customizations.length > 0 ? (
                    <div className="space-y-1">
                      {item.customizations.map((custom, i) => (
                        <Badge key={i} variant="secondary" className="text-xs">
                          {custom.name} - R$ {custom.price}
                        </Badge>
                      ))}
                    </div>
                  ) : (
                    <span className="text-xs text-gray-400">Sem adicionais</span>
                  )}
                </div>

                <div className="col-span-2 col-start-8 flex items-center gap-1 whitespace-nowrap">
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-6 w-6"
                    onClick={() => updateQuantity(index, item.quantity - 1)}
                  >
                    <Minus className="h-3 w-3" />
                  </Button>
                  <span className="w-6 text-center text-sm">{item.quantity}</span>
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-6 w-6"
                    onClick={() => updateQuantity(index, item.quantity + 1)}
                  >
                    <Plus className="h-3 w-3" />
                  </Button>
                </div>

                <div className="col-span-2 col-start-10 text-sm font-medium whitespace-nowrap">
                  R$ {item.totalPrice}
                </div>
                
                <div className="col-span-1 col-start-12 whitespace-nowrap">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 text-red-500 hover:text-red-700"
                    onClick={() => removeItem(index)}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
                <div className="col-span-1 col-start-13 whitespace-nowrap">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 text-red-500 hover:text-red-700"
                    onClick={() => editItem(index)}
                  >
                    <Pencil className="h-3 w-3" />
                  </Button>
                </div>
              </div>
            ))}

            <Separator />

            <div className="flex justify-between items-center font-bold text-lg">
              <span>Subtotal</span>
              <span className="text-orange-600">R$ {getCurrentTotal()}</span>
            </div>

            <div className="flex gap-3 pt-4">
              <Button 
                variant="outline" 
                className="flex-1"
                onClick={onClose}
              >
                Continuar comprando
              </Button>
              <Button 
                className="flex-1 bg-orange-500 hover:bg-orange-600"
                onClick={handleCheckout}
              >
                Fechar pedido
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      <PaymentModal
        isOpen={showPayment}
        onClose={() => setShowPayment(false)}
        total={getCurrentTotal()}
        onPaymentComplete={handlePaymentComplete}
        user={user}
      />
    </>
  );
};
