import { DiscountStrategy } from "./discountStrategies";

export class DiscountContext {
    private strategy: DiscountStrategy;

    constructor(strategy: DiscountStrategy) {
        this.strategy = strategy;
    }

    setStrategy(strategy: DiscountStrategy): void {
        this.strategy = strategy;
    }

    getDiscountedValue(total: number): number {
        return this.strategy.applyDiscount(total);
    }
}