
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface Ingredient {
  id: string;
  name: string;
  type: string;
  additional: boolean;
  price: number;
  status: boolean;
}

interface IngredientModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (ingredient: any) => void;
  ingredient?: Ingredient | null;
}

export const IngredientModal = ({ open, onClose, onSave, ingredient }: IngredientModalProps) => {
  const [formData, setFormData] = useState({
    name: "",
    type: "",
    additional: false,
    price: 0,
    status: true
  });

  useEffect(() => {
    if (ingredient) {
      setFormData({
        name: ingredient.name,
        type: ingredient.type,
        additional: ingredient.additional,
        price: ingredient.price,
        status: ingredient.status
      });
    } else {
      setFormData({
        name: "",
        type: "",
        additional: false,
        price: 0,
        status: true
      });
    }
  }, [ingredient, open]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  const ingredientTypes = [
    "Especiaria",
    "Adoçante", 
    "Acompanhamento",
    "Base",
    "Cobertura"
  ];

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="text-xl text-orange-800">
            {ingredient ? "Edite seu ingrediente" : "Adicione seu ingrediente"}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="ingredient-name">Nome:</Label>
            <Input
              id="ingredient-name"
              placeholder="Nome do ingrediente"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="ingredient-type">Tipo:</Label>
            <Select
              value={formData.type}
              onValueChange={(value) => setFormData({ ...formData, type: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecione o tipo" />
              </SelectTrigger>
              <SelectContent>
                {ingredientTypes.map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Relaciona-lo ou Desrelaciona-lo do produto:</Label>
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <input
                  type="radio"
                  checked={formData.additional}
                  onChange={() => setFormData({ ...formData, additional: true })}
                  className="text-orange-500"
                />
                <span>Café com Chantilly</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="radio"
                  checked={!formData.additional}
                  onChange={() => setFormData({ ...formData, additional: false })}
                  className="text-orange-500"
                />
                <span>Cappuccino</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="radio"
                  checked={false}
                  onChange={() => {}}
                  className="text-orange-500"
                />
                <span>Frappuccino</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="radio"
                  checked={false}
                  onChange={() => {}}
                  className="text-orange-500"
                />
                <span>Chocolate Gelado</span>
              </label>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="ingredient-price">Preço base:</Label>
            <Input
              id="ingredient-price"
              type="number"
              step="0.01"
              min="0"
              placeholder="R$ 7,00"
              value={formData.price}
              onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) || 0 })}
            />
          </div>

          <div className="space-y-2">
            <Label>Categoria:</Label>
            <div className="bg-blue-100 text-blue-800 px-3 py-2 rounded-md text-center">
              Cafés Clássicos
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
