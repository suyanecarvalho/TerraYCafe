/*import { User, UserRegister } from '@/models/User';
import { apiRequest } from './api';

export class AuthService {
  static async login(email: string, senha: string): Promise<User> {
    try {
      const response = await apiRequest('POST', '/cliente/login', { email, senha });
      const token = response.access_token;
      console.log('Accessing token: ', response.access_token);
      const user = response.user;
      console.log('Login response: ', response);
      localStorage.setItem("token", token);
      return user;
    } catch (error) {
      console.error('Login error:', error); 
      throw new Error('Falha no login. Verifique suas credenciais.');
    }
  }
*/
import { User, UserRegister } from '@/models/User';
import { apiRequest } from './api';

export class AuthService {
  static async login(email: string, senha: string): Promise<User> {
    try {
      const response = await apiRequest('POST', '/cliente/login', { email, senha });
      const token = response.access_token || response.token;
      
      if (!token) {
        throw new Error('Token não recebido na resposta');
      }
      
      localStorage.setItem('token', token);
      
      // Se a resposta já inclui os dados do usuário, retorna normalizado
      if (response.user || response.nome) {
        return response;
      }
      
      // Se não, busca os dados do usuário
      return await this.getCurrentUser();
    } catch (error) {
      console.error('Login error:', error);
      throw new Error(error.message || 'Falha no login. Verifique suas credenciais.');
    }
  }

  static async register(userData: UserRegister): Promise<User> {
    try {
      const response = await apiRequest('POST', '/cliente/register', {
        nome: userData.nome,
        email: userData.email,
        telefone: userData.telefone || '',
        senha: userData.senha
      });
      
      return response;
    } catch (error) {
      console.error('Register error:', error);
      throw new Error(error.message || 'Falha no cadastro. Tente novamente.');
    }
  }

  static async logout(): Promise<void> {
    try {
      await apiRequest('POST', '/cliente/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
    }
  }

  static async getCurrentUser(): Promise<User | null> {
    try {
      const response = await apiRequest('GET', '/cliente/me');
      return response;
    } catch (error) {
      console.error('Get current user error:', error);
      return null;
    }
  }
}