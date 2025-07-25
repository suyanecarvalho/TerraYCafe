import { CartItem, Customization } from '@/models/Drink';

export class CartService {
  static calculateItemTotal(item: CartItem): number {
    const basePrice = item.drink.preco_base * item.quantity;
    const customizationPrice = item.customizations.reduce((total, custom) => {
      return total + custom.price;
    }, 0) * item.quantity;
    console.log("Valor calculado: ", basePrice + customizationPrice);
    return basePrice + customizationPrice;
  }

  static updateItemQuantity(item: CartItem, newQuantity: number): CartItem {
    const updatedItem = { ...item, quantity: newQuantity };
    updatedItem.totalPrice = this.calculateItemTotal(updatedItem);
    return updatedItem;
  }

  static createCartItem(
    drink: any,
    quantity: number,
    customizations: Customization[]
  ): CartItem {
    const item: CartItem = {
      drink,
      quantity,
      customizations,
      totalPrice: 0
    };
    item.totalPrice = this.calculateItemTotal(item);
    return item;
  }

  static getCartTotal(items: CartItem[]): number {
    return items.reduce((total, item) => total + item.totalPrice, 0);
  }
}
