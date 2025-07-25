export interface User {
  id?: number;
  nome: string;
  email: string;
  telefone?: string;
  pontos_fidelidade?: number;
  access_token?: string; // lidar com o token
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
}

export interface UserRegister {
  nome: string;
  email: string;
  telefone?: string;
  senha: string;
}