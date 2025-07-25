import { useState, useEffect } from 'react';
import { AuthService } from '@/services/authService';
import { User, AuthState, UserRegister } from '@/models/User';

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Função para normalizar os dados do usuário
  const normalizeUser = (data: any): User => {
    return {
      id: data.id || data.user?.id,
      nome: data.nome || data.name || data.user?.nome || '',
      email: data.email || data.user?.email || '',
      telefone: data.telefone || data.phone || data.user?.telefone || '',
      pontos_fidelidade: data.pontos_fidelidade || data.user?.pontos_fidelidade || 0
    };
  };

  // Carrega o usuário ao iniciar
  useEffect(() => {
    const initAuth = async () => {
      try {
        const userData = await AuthService.getCurrentUser();
        if (userData) {
          const normalizedUser = normalizeUser(userData);
          setAuthState({
            user: normalizedUser,
            isAuthenticated: !!normalizedUser
          });
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  
  const login = async (email: string, senha: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await AuthService.login(email, senha);
      const normalizedUser = normalizeUser(response);
      
      setAuthState({
        user: normalizedUser,
        isAuthenticated: true
      });
      return normalizedUser;
    } catch (error: any) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  
  const register = async (userData: UserRegister) => {
    try {
      setLoading(true);
      setError(null);
      const response = await AuthService.register(userData);
      const normalizedUser = normalizeUser(response);
      
      setAuthState({
        user: normalizedUser,
        isAuthenticated: false
      });
      return normalizedUser;
    } catch (error: any) {
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  
  const logout = async () => {
    try {
      setLoading(true);
      await AuthService.logout();
      setAuthState({
        user: null,
        isAuthenticated: false
      });
    } catch (error) {
      console.error('Logout error:', error);
      
      setAuthState({
        user: null,
        isAuthenticated: false
      });
    } finally {
      setLoading(false);
    }
  };

  return {
    ...authState,
    loading,
    error,
    login,
    register,
    logout
  };
};