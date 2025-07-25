import { apiRequest } from "./api";
import { Drink } from "@/models/Drink";

export class DrinkService {
    static async getDrinks(): Promise<Drink[]> {
        try {
        const response = await apiRequest("GET", "/bebidas");
        console.log("Resposta das bebidas:", response);
        return response;
        } catch (error) {
        console.error("Error fetching drinks:", error);
        throw new Error("Failed to fetch drinks. Please try again later.");
        }
    }
    
    static async getDrinkById(id: string): Promise<Drink> {
        try {
        const response = await apiRequest("GET", `/bebidas/${id}`);
        return response.data;
        } catch (error) {
        console.error(`Error fetching drink with ID ${id}:`, error);
        throw new Error("Failed to fetch drink details. Please try again later.");
        }
    }
}