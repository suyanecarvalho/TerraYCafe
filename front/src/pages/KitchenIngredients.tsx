
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ArrowLeft, Plus, Edit, Trash2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { IngredientModal } from "@/components/IngredientModal";
import { ProductModal } from "@/components/ProductModal";

interface Ingredient {
  id: string;
  name: string;
  type: string;
  additional: boolean;
  price: number;
  status: boolean;
}

interface Product {
  id: string;
  name: string;
  description: string;
  category: string;
  basePrice: number;
}

const KitchenIngredients = () => {
  const navigate = useNavigate();
  const [ingredientModalOpen, setIngredientModalOpen] = useState(false);
  const [productModalOpen, setProductModalOpen] = useState(false);
  const [editingIngredient, setEditingIngredient] = useState<Ingredient | null>(null);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  const [ingredients, setIngredients] = useState<Ingredient[]>([
    { id: "1", name: "Açúcar em Pó", type: "Especiaria", additional: false, price: 0, status: true },
    { id: "2", name: "Adoçante", type: "Adoçante", additional: false, price: 0.20, status: true },
    { id: "3", name: "Biscoito Complementar", type: "Acompanhamento", additional: true, price: 0.80, status: true },
    { id: "4", name: "Canela em Pó", type: "Base", additional: false, price: 0.50, status: true },
    { id: "5", name: "Chantilly", type: "Cobertura", additional: true, price: 2.00, status: true },
    { id: "6", name: "Café", type: "Base", additional: false, price: 25.00, status: true }
  ]);

  const [products, setProducts] = useState<Product[]>([
    { id: "1", name: "Café Expresso", description: "Nosso blend exclusivo artesanal preparado com grãos especiais", category: "Cafés Clássicos", basePrice: 7.00 },
    { id: "2", name: "Cappuccino", description: "Café expresso com leite vaporizado e espuma de leite", category: "Cafés Clássicos", basePrice: 12.00 },
    { id: "3", name: "Suco de Laranja", description: "Suco natural da fruta 100% natural", category: "Sucos e Vitaminas", basePrice: 9.00 },
    { id: "4", name: "Croissant", description: "Croissant fresco assado", category: "Lanches", basePrice: 8.50 },
    { id: "5", name: "Pão de Queijo Tradicional", description: "Clássico pão de queijo mineiro", category: "Lanches", basePrice: 6.00 },
    { id: "6", name: "Café Expresso Simples", description: "Café forte e aromático", category: "Cafés Clássicos", basePrice: 5.00 }
  ]);

  const handleEditIngredient = (ingredient: Ingredient) => {
    setEditingIngredient(ingredient);
    setIngredientModalOpen(true);
  };

  const handleEditProduct = (product: Product) => {
    setEditingProduct(product);
    setProductModalOpen(true);
  };

  const handleDeleteIngredient = (id: string) => {
    setIngredients(ingredients.filter(ingredient => ingredient.id !== id));
  };

  const handleDeleteProduct = (id: string) => {
    setProducts(products.filter(product => product.id !== id));
  };

  const handleSaveIngredient = (ingredientData: any) => {
    if (editingIngredient) {
      setIngredients(ingredients.map(ing => 
        ing.id === editingIngredient.id ? { ...ing, ...ingredientData } : ing
      ));
    } else {
      const newIngredient = {
        id: Date.now().toString(),
        ...ingredientData
      };
      setIngredients([...ingredients, newIngredient]);
    }
    setIngredientModalOpen(false);
    setEditingIngredient(null);
  };

  const handleSaveProduct = (productData: any) => {
    if (editingProduct) {
      setProducts(products.map(prod => 
        prod.id === editingProduct.id ? { ...prod, ...productData } : prod
      ));
    } else {
      const newProduct = {
        id: Date.now().toString(),
        ...productData
      };
      setProducts([...products, newProduct]);
    }
    setProductModalOpen(false);
    setEditingProduct(null);
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
            <h1 className="text-3xl font-bold text-orange-800">Ingredientes e Produtos</h1>
            <p className="text-orange-600">Gerencie seus ingredientes e produtos</p>
          </div>
        </div>

        {/* Ingredients Section */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle className="text-2xl text-orange-800">
                O que temos de ingredientes 🧑‍🍳
              </CardTitle>
              <Button
                onClick={() => {
                  setEditingIngredient(null);
                  setIngredientModalOpen(true);
                }}
                className="bg-orange-500 hover:bg-orange-600"
              >
                <Plus className="h-4 w-4 mr-2" />
                Adicionar Ingrediente
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Nome</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Adicional</TableHead>
                  <TableHead>Preço</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {ingredients.map((ingredient) => (
                  <TableRow key={ingredient.id}>
                    <TableCell>{ingredient.id}</TableCell>
                    <TableCell>{ingredient.name}</TableCell>
                    <TableCell>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        ingredient.type === "Especiaria" ? "bg-purple-100 text-purple-800" :
                        ingredient.type === "Adoçante" ? "bg-green-100 text-green-800" :
                        ingredient.type === "Acompanhamento" ? "bg-blue-100 text-blue-800" :
                        ingredient.type === "Base" ? "bg-yellow-100 text-yellow-800" :
                        "bg-pink-100 text-pink-800"
                      }`}>
                        {ingredient.type}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        ingredient.additional ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                      }`}>
                        {ingredient.additional ? "Sim" : "Não"}
                      </span>
                    </TableCell>
                    <TableCell>R$ {ingredient.price.toFixed(2)}</TableCell>
                    <TableCell>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        ingredient.status ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                      }`}>
                        {ingredient.status ? "Ativo" : "Inativo"}
                      </span>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleEditIngredient(ingredient)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => handleDeleteIngredient(ingredient.id)}
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

        {/* Products Section */}
        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle className="text-2xl text-orange-800">
                Nossos produtos 🧑‍🍳
              </CardTitle>
              <Button
                onClick={() => {
                  setEditingProduct(null);
                  setProductModalOpen(true);
                }}
                className="bg-orange-500 hover:bg-orange-600"
              >
                <Plus className="h-4 w-4 mr-2" />
                Adicionar produto
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Nome</TableHead>
                  <TableHead>Descrição</TableHead>
                  <TableHead>Categoria</TableHead>
                  <TableHead>Preço base</TableHead>
                  <TableHead>Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {products.map((product) => (
                  <TableRow key={product.id}>
                    <TableCell>{product.id}</TableCell>
                    <TableCell>{product.name}</TableCell>
                    <TableCell className="max-w-xs truncate">{product.description}</TableCell>
                    <TableCell>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        product.category === "Cafés Clássicos" ? "bg-blue-100 text-blue-800" :
                        product.category === "Sucos e Vitaminas" ? "bg-green-100 text-green-800" :
                        "bg-yellow-100 text-yellow-800"
                      }`}>
                        {product.category}
                      </span>
                    </TableCell>
                    <TableCell>R$ {product.basePrice.toFixed(2)}</TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleEditProduct(product)}
                        >
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => handleDeleteProduct(product.id)}
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
      </div>

      <IngredientModal
        open={ingredientModalOpen}
        onClose={() => {
          setIngredientModalOpen(false);
          setEditingIngredient(null);
        }}
        onSave={handleSaveIngredient}
        ingredient={editingIngredient}
      />

      <ProductModal
        open={productModalOpen}
        onClose={() => {
          setProductModalOpen(false);
          setEditingProduct(null);
        }}
        onSave={handleSaveProduct}
        product={editingProduct}
      />
    </div>
  );
};

export default KitchenIngredients;
