
import { useState, useCallback } from 'react';
import { OrderService } from '@/services/orderService';
import { CartItem, Order } from '@/models/Drink';

export const useOrder = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

const processOrder = useCallback(
  async (items: CartItem[], total: number, cliente_id: number, forma_pagamento: string): Promise<Order> => {
    try {
      setLoading(true);
      setError(null);

      // 1. Prepara cada bebida no backend
      for (const item of items) {
        await OrderService.orderOnCart(
          cliente_id,
          item.drink,
          item.customizations
        );
      }

      // 2. Cria o pedido principal (sem itens, pois já estão temporários no backend)
      const order = await OrderService.createOrder(cliente_id, forma_pagamento);
      return order;
    } catch (error: any) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  },
  []
);
  const getOrderHistory = useCallback(async (): Promise<Order[]> => {
    try {
      setLoading(true);
      setError(null);
      const orders = await OrderService.getOrderHistory();
      return orders;
    } catch (error: any) {
      setError(error.message);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    processOrder,
    getOrderHistory
  };
};
