
import { useMemo, useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { CreditCard, Smartphone, DollarSign, Gift } from "lucide-react";
import { DiscountStrategy, PixDiscountStrategy, DebitCardDiscountStrategy, VoucherDiscountStrategy, NoDiscountStrategy } from "@/patterns/discountStrategies";
import { DiscountContext } from "@/patterns/discountContext";
import { OrderService } from "@/services/orderService";

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  total: number;
  onPaymentComplete: () => void;
  user: any;
}

const paymentMethods = [
  { id: "Pix", name: "Pix", icon: Smartphone, discount: "5% de desconto" },
  { id: "Credit", name: "Cartão de crédito", icon: CreditCard },
  { id: "DebitCard", name: "Cartão de débito", icon: CreditCard, discount: "" },
  { id: "Voucher", name: "Fidelidade", icon: Gift, discount: "10% de desconto" }
];

export const PaymentModal = ({ isOpen, onClose, total, onPaymentComplete, user }: PaymentModalProps) => {
  const [selectedMethod, setSelectedMethod] = useState("Pix");

  const discountStrategiesMap: { [key: string]: DiscountStrategy } = useMemo(() => ({
    Pix: new PixDiscountStrategy(),
    Credit: new NoDiscountStrategy(),
    DebitCard: new DebitCardDiscountStrategy(),
    Voucher: new VoucherDiscountStrategy()
  }), []);

  const discountContext = useMemo(() => new DiscountContext(new NoDiscountStrategy), []);

  const getDiscountedTotal = () => {
    const strategy = discountStrategiesMap[selectedMethod] || new NoDiscountStrategy();
    discountContext.setStrategy(strategy);
    return discountContext.getDiscountedValue(total);
  };

  const handlePayment = () => {
    // Simular processamento do pagamento
    OrderService.createOrder(user.id, selectedMethod)
    setTimeout(() => {
      onPaymentComplete();
      onClose();
    }, 1000);
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-md mx-auto">
        <DialogHeader>
          <DialogTitle className="text-center text-xl">Seu jeito de pagar</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-6">
          {/* Opções de pagamento */}
          <div>
            <h4 className="font-medium mb-4">Opções:</h4>
            <RadioGroup value={selectedMethod} onValueChange={setSelectedMethod}>
              <div className="space-y-3">
                {paymentMethods.map((method) => {
                  const IconComponent = method.icon;
                  return (
                    <div key={method.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50">
                      <div className="flex items-center space-x-3">
                        <RadioGroupItem value={method.id} id={method.id} />
                        <IconComponent className="h-5 w-5 text-gray-600" />
                        <Label htmlFor={method.id} className="font-medium">
                          {method.name}
                        </Label>
                      </div>
                      {method.discount && (
                        <span className="text-sm text-green-600 font-medium">
                          {method.discount}
                        </span>
                      )}
                    </div>
                  );
                })}
              </div>
            </RadioGroup>
          </div>

          {/* Total */}
          <div className="bg-orange-50 p-4 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="text-lg font-medium">Total:</span>
              <div className="text-right">
                {getDiscountedTotal() < total && (
                  <div className="text-sm text-gray-500 line-through">
                    R$ {total.toFixed(2)}
                  </div>
                )}
                <div className="text-xl font-bold text-orange-600">
                  R$ {getDiscountedTotal().toFixed(2)}
                </div>
              </div>
            </div>
          </div>

          {/* Botão de finalizar */}
          <Button 
            className="w-full bg-green-500 hover:bg-green-600 text-white"
            onClick={handlePayment}
          >
            Fazer pedido
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
