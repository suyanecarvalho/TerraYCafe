
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  basePrice: number;
}

interface ProductModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (product: any) => void;
  product?: Product | null;
}

export const ProductModal = ({ open, onClose, onSave, product }: ProductModalProps) => {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    category: "Cafés Clássicos",
    basePrice: 0
  });

  useEffect(() => {
    if (product) {
      setFormData({
        name: product.name,
        description: product.description,
        category: product.category,
        basePrice: product.basePrice
      });
    } else {
      setFormData({
        name: "",
        description: "",
        category: "Cafés Clássicos",
        basePrice: 0
      });
    }
  }, [product, open]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="text-xl text-orange-800">
            {product ? "Edite um produto" : "Adicione um produto"}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="product-id">ID:</Label>
            <Input
              id="product-id"
              placeholder="ID do ingrediente"
              value={product?.id || "Auto-gerado"}
              disabled
              className="bg-gray-100"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="product-name">Nome:</Label>
            <Input
              id="product-name"
              placeholder="Nome do ingrediente"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="product-description">Descrição:</Label>
            <Textarea
              id="product-description"
              placeholder="Descrição do ingrediente"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={3}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="product-price">Preço base:</Label>
            <Input
              id="product-price"
              type="number"
              step="0.01"
              min="0"
              placeholder="R$ 7,00"
              value={formData.basePrice}
              onChange={(e) => setFormData({ ...formData, basePrice: parseFloat(e.target.value) || 0 })}
            />
          </div>

          <div className="space-y-2">
            <Label>Categoria:</Label>
            <div className="bg-blue-100 text-blue-800 px-3 py-2 rounded-md text-center">
              {formData.category}
            </div>
          </div>

          <Button
            type="submit"
            className="w-full bg-green-500 hover:bg-green-600 text-white"
          >
            Concluído
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
};
