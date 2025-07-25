// Configuração da API
const API_CONFIG = {
  // Em desenvolvimento, usar URLs relativas para o proxy funcionar
  BASE_URL: '',
  TIMEOUT: 10000, // 10 segundos
  HEADERS: {
    'Content-Type': 'application/json',
  }
};

// Função para obter o token de autenticação
const getAuthToken = (): string | null => {
  const token = localStorage.getItem('token');
  if (token) {
    return token;
  }
  
  // Fallback: tentar pegar do user object
  const userData = localStorage.getItem('user');
  if (userData) {
    try {
      const user = JSON.parse(userData);
      return user.token || null;
    } catch {
      return null;
    }
  }
  return null;
};

// Função para criar headers padrão
const getHeaders = (includeAuth: boolean = true): HeadersInit => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  if (includeAuth) {
    const token = getAuthToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }

  return headers;
};

// Função para construir URL completa
const buildUrl = (endpoint: string): string => {
  const baseURL = "http://localhost:8000"; // URL base do proxy
  // Se já começar com http, usar como está (para produção)
  if (endpoint.startsWith('http')) {
    return endpoint;
  }
  
  // Em desenvolvimento, usar URL relativa para ativar o proxy
  /*if (endpoint.startsWith('/api')) {
    return endpoint; // /api/cliente/login
  }*/
  
  // Para outras rotas, usar diretamente
  return baseURL + endpoint; // /bebidas, /cliente, /produto
};

// Classe para fazer requisições HTTP reais
export class ApiService {
  static async get(endpoint: string, requireAuth: boolean = true): Promise<any> {
    const response = await fetch(buildUrl(endpoint), {
      method: 'GET',
      headers: getHeaders(requireAuth),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  static async post(endpoint: string, data: any, requireAuth: boolean = false): Promise<any> {
    const response = await fetch(buildUrl(endpoint), {
      method: 'POST',
      headers: getHeaders(requireAuth),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  static async put(endpoint: string, data: any, requireAuth: boolean = true): Promise<any> {
    const response = await fetch(buildUrl(endpoint), {
      method: 'PUT',
      headers: getHeaders(requireAuth),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  static async delete(endpoint: string, requireAuth: boolean = true): Promise<any> {
    const response = await fetch(buildUrl(endpoint), {
      method: 'DELETE',
      headers: getHeaders(requireAuth),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  static async patch(endpoint: string, data: any, requireAuth: boolean = true): Promise<any> {
    const response = await fetch(buildUrl(endpoint), {
      method: 'PATCH',
      headers: getHeaders(requireAuth),
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }
}

// Função helper para fazer requisições HTTP
export const apiRequest = async (
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH',
  endpoint: string,
  data?: any,
  requireAuth: boolean = true
): Promise<any> => {
  try {
    switch (method) {
      case 'GET':
        return await ApiService.get(endpoint, requireAuth);
      case 'POST':
        return await ApiService.post(endpoint, data, requireAuth);
      case 'PUT':
        return await ApiService.put(endpoint, data, requireAuth);
      case 'DELETE':
        return await ApiService.delete(endpoint, requireAuth);
      case 'PATCH':
        return await ApiService.patch(endpoint, data, requireAuth);
      default:
        throw new Error('Unsupported method');
    }
  } catch (error) {
    console.error(`API Error on ${method} ${endpoint}:`, error);
    throw error;
  }
};

// Funções específicas para diferentes operações da API
export const authAPI = {
  login: (credentials: { email: string; senha: string }) =>
    apiRequest('POST', '/cliente/login', {
      email: credentials.email,
      senha: credentials.senha
    }, false),
  
  register: (userData: { name: string; email: string; password: string; phone?: string }) =>
    apiRequest('POST', '/cliente/register', {
      nome: userData.name,
      email: userData.email,
      telefone: userData.phone || '',
      senha: userData.password
    }, false), 
  
  logout: () =>
    apiRequest('POST', '/cliente/logout', {}, true),
  
  me: () =>
    apiRequest('GET', '/cliente/me', undefined, true),
};

// API específica para bebidas (usando proxy direto)
export const bebidasAPI = {
  getAll: () =>
    apiRequest('GET', '/bebidas', undefined, false),
  
  getById: (id: string) =>
    apiRequest('GET', `/bebidas/${id}`, undefined, false),
};


export const ordersAPI = {
  getAll: () =>
    apiRequest('GET', '/pedido', undefined, true),
  
  create: (orderData: any) =>
    apiRequest('POST', '/pedido', orderData, true),
  
  getById: (orderId: string) =>
    apiRequest('GET', `/pedido/${orderId}`, undefined, true),
  
  update: (orderId: string, orderData: any) =>
    apiRequest('PUT', `/pedido/${orderId}`, orderData, true),
  
  delete: (orderId: string) =>
    apiRequest('DELETE', `/pedido/${orderId}`, undefined, true),
};

export const clienteAPI = {
  getAll: () =>
    apiRequest('GET', '/cliente', undefined, true),
  
  getById: (clienteId: string) =>
    apiRequest('GET', `/cliente/${clienteId}`, undefined, true),
  
  create: (clienteData: any) =>
    apiRequest('POST', '/cliente', clienteData, false),
  
  update: (clienteId: string, clienteData: any) =>
    apiRequest('PUT', `/cliente/${clienteId}`, clienteData, true),
  
  delete: (clienteId: string) =>
    apiRequest('DELETE', `/cliente/${clienteId}`, undefined, true),
};

export const productsAPI = {
  getAll: () =>
    apiRequest('GET', '/produtos', undefined, false),
  
  getById: (productId: string) =>
    apiRequest('GET', `/produtos/${productId}`, undefined, false),
  
  create: (productData: any) =>
    apiRequest('POST', '/produtos', productData, true),
  
  update: (productId: string, productData: any) =>
    apiRequest('PUT', `/produtos/${productId}`, productData, true),
  
  delete: (productId: string) =>
    apiRequest('DELETE', `/produtos/${productId}`, undefined, true),
};

export const ingredientsAPI = {
  getAll: () =>
    apiRequest('GET', '/decorator', undefined, true),
  
  create: (ingredientData: any) =>
    apiRequest('POST', '/ingredientes', ingredientData, true),
  
  update: (ingredientId: string, ingredientData: any) =>
    apiRequest('PUT', `/ingredientes/${ingredientId}`, ingredientData, true),
  
  delete: (ingredientId: string) =>
    apiRequest('DELETE', `/ingredientes/${ingredientId}`, undefined, true),
};