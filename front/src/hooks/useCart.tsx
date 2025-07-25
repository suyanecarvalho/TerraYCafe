
import { useState, useCallback } from 'react';
import { CartItem, Customization } from '@/models/Drink';
import { CartService } from '@/services/cartService';

export const useCart = () => {
  const [cart, setCart] = useState<CartItem[]>([]);

  const addToCart = useCallback((drink: any, quantity: number, customizations: Customization[]) => {
    const item = CartService.createCartItem(drink, quantity, customizations);
    setCart(prevCart => [...prevCart, item]);
  }, []);

  const updateCart = useCallback((items: CartItem[]) => {
    setCart(items);
  }, []);

  const updateQuantity = useCallback((index: number, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeItem(index);
      return;
    }
    
    setCart(prevCart => {
      const updatedCart = [...prevCart];
      updatedCart[index] = CartService.updateItemQuantity(updatedCart[index], newQuantity);
      return updatedCart;
    });
  }, []);
 
  const removeItem = useCallback((index: number) => {
    setCart(prevCart => prevCart.filter((_, i) => i !== index));
  }, []);

  const updateItem = useCallback((index: number, item: CartItem) => {
    setCart(prevCart => {
      const updatedCart = [...prevCart];
      item.totalPrice = CartService.calculateItemTotal(item);
      updatedCart[index] = item;
      return updatedCart;
    });
  }, []);

  const clearCart = useCallback(() => {
    setCart([]);
  }, []);

  const getTotalItems = useCallback(() => {
    console.log("cart: ", cart);
    return cart.reduce((total, item) => total + item.quantity, 0);
  }, [cart]);

  const getTotalPrice = useCallback(() => {
    return CartService.getCartTotal(cart);
  }, [cart]);

  return {
    cart,
    addToCart,
    updateCart,
    updateQuantity,
    removeItem,
    updateItem,
    clearCart,
    getTotalItems,
    getTotalPrice
  };
};
