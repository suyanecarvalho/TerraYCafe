
export interface Drink {
  id: string;
  nome: string;
  preco_base: number;
  image: string;
  description: string;
}

export interface Customization {
  id: number;
  name: string;
  price: number;
}

export interface Customizations {
  id: number;
  name: string;
  price: number;
}

export interface CartItem {
  drink: Drink;
  quantity: number;
  customizations: Customization[];
  totalPrice: number;
}

export interface Order {
  id: number;
  status: string;
  valor_total: number;
  forma_pagamento: string;
  desconto: number;
  data_hora: string;
  cliente_id: number;
}

export interface Ingredient {
  id: string;
  nome: string;
  preco_adicional: number;
}
