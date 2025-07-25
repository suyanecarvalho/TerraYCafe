
export interface DiscountStrategy {
  applyDiscount(total: number): number;
}

export class PixDiscountStrategy implements DiscountStrategy {
    applyDiscount(total: number): number {
        return total * 0.95;
    }
}

export class DebitCardDiscountStrategy implements DiscountStrategy {
    applyDiscount(total: number): number {
        return total;
    }
}

export class VoucherDiscountStrategy implements DiscountStrategy {
    applyDiscount(total: number): number {
        return total * 0.9;
    }
}

export class NoDiscountStrategy implements DiscountStrategy {
    applyDiscount(total: number): number {
        return total;
    }
}