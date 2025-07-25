import { Order, CartItem, Drink, Customizations } from '@/models/Drink';
import { apiRequest } from './api';

export class OrderService {
  static createOrderData(items: CartItem[], total: number) {
    return {
      items,
      total
    };
  }

  static createOrderToCart(id: number, drink: Drink, customizations?: Customizations[]) {
    const orderObj = {
      cliente_id: id,
      tipo_bebida: drink.nome,
      ingredientes: customizations ? customizations.map(({ id }) => id) : [],
    };
    console.log("Objeto enviado para preparar bebida:", orderObj);
    return orderObj;
  }

  static async saveOrder(items: CartItem[], total: number): Promise<Order> {
    try {
      const orderData = this.createOrderData(items, total);
      const response = await apiRequest('POST', '/pedidos/criar', orderData);
      return response.data;
    } catch (error) {
      console.error('Save order error:', error);
      throw new Error('Falha ao salvar pedido. Tente novamente.');
    }
  }

  static async orderOnCart(id: number, drink: Drink, customizations: Customizations[])  {
    try {
      const orderItem = this.createOrderToCart(id, drink, customizations);
      console.log("Order item to cart:", orderItem);
      const response = await apiRequest('POST', '/pedidos/bebida/preparar', orderItem);
      console.log("Resposta do backend /pedidos/bebida/preparar:", response);
      if (!response) {
        throw new Error('Falha ao preparar bebida. Resposta vazia do backend.');
      }
      return response;
    } catch (error) {
      console.error('Prepare order error:', error);
      throw new Error('Falha ao salvar item. Tente novamente.');
    }
  } 

  static async getOrderHistory(): Promise<Order[]> {
    try {
      const response = await apiRequest('GET', '/pedidos');
      console.log("Order history response:", response.pedidos);
      return response.pedidos;
    } catch (error) {
      console.error('Get order history error:', error);
      // Fallback para localStorage em caso de erro
      try {
        const ordersData = localStorage.getItem('orderHistory');
        return ordersData ? JSON.parse(ordersData) : [];
      } catch (fallbackError) {
        console.error('Fallback error:', fallbackError);
        return [];
      }
    }
  }

  static async createOrder(id: number, pagamento: string) {
    try {
      const orderData = {
        cliente_id: id,
        forma_pagamento: pagamento
      };
      console.log("Creating order with data:", orderData);
      const response = await apiRequest('POST', '/pedidos/criar', orderData);
      console.log("Resposta do backend /pedidos/criar:", response.data);
      return response.data;
    } catch (error) {
      console.error('Create order error:', error);
      throw new Error('Falha ao criar pedido. Tente novamente.');
    }
  }

  static async updateOrderStatus(id: number) {
    try {
      const response = await apiRequest('PATCH', `/pedidos/${id}/atualizar`);
      console.log("Order status updated:", response.data);
      return response.data;
    } catch (error) {
      console.error('Update order status error:', error);
      throw new Error('Falha ao atualizar status do pedido. Tente novamente.');
    }
  }
}
