
# Arquitetura MVC React-Friendly - Terra&Café

## 📋 Visão Geral

Esta documentação explica a implementação da arquitetura MVC adaptada para React no projeto Terra&Café. A estrutura foi projetada para ser mais idiomática ao ecossistema React, mantendo os princípios do MVC tradicional.

## 🏗️ Estrutura da Arquitetura

```
src/
├── models/           # Interfaces e tipos de dados (Model)
├── services/         # Lógica de negócio pura (Controller)
├── hooks/           # Custom hooks - ponte entre services e views
├── components/      # Componentes reutilizáveis (View)
└── pages/          # Páginas da aplicação (View)
```

## 🔍 Detalhamento das Camadas

### 1. **Models (`src/models/`)**
**Responsabilidade**: Definir estruturas de dados e tipos TypeScript.

**Arquivos criados**:
- `User.ts` - Tipos para usuário e autenticação
- `Drink.ts` - Tipos para bebidas, carrinho e pedidos

**Exemplo**:
```typescript
export interface CartItem {
  drink: Drink;
  quantity: number;
  customizations: Customization[];
  totalPrice: number;
}
```

**Características**:
- ✅ Apenas interfaces e tipos
- ✅ Sem lógica de negócio
- ✅ Reutilizáveis em toda aplicação

### 2. **Services (`src/services/`)**
**Responsabilidade**: Lógica de negócio pura, independente do React.

**Arquivos criados**:
- `authService.ts` - Gerenciamento de autenticação
- `cartService.ts` - Lógica de cálculos do carrinho
- `orderService.ts` - Gerenciamento de pedidos

**Exemplo**:
```typescript
export class CartService {
  static calculateItemTotal(item: CartItem): number {
    const basePrice = item.drink.price * item.quantity;
    const customizationPrice = item.customizations.reduce((total, custom) => {
      return total + custom.price;
    }, 0) * item.quantity;
    return basePrice + customizationPrice;
  }
}
```

**Características**:
- ✅ Lógica pura (sem dependências React)
- ✅ Métodos estáticos para facilitar uso
- ✅ Testáveis independentemente
- ✅ Reutilizáveis em qualquer contexto

### 3. **Hooks (`src/hooks/`)**
**Responsabilidade**: Ponte entre services e componentes React.

**Arquivos criados**:
- `useAuth.tsx` - Hook para autenticação
- `useCart.tsx` - Hook para gerenciamento do carrinho
- `useOrder.tsx` - Hook para pedidos

**Exemplo**:
```typescript
export const useCart = () => {
  const [cart, setCart] = useState<CartItem[]>([]);

  const addToCart = useCallback((drink: any, quantity: number, customizations: Customization[]) => {
    const item = CartService.createCartItem(drink, quantity, customizations);
    setCart(prevCart => [...prevCart, item]);
  }, []);

  return {
    cart,
    addToCart,
    // ... outros métodos
  };
};
```

**Características**:
- ✅ Gerenciam estado React
- ✅ Consomem services para lógica de negócio
- ✅ Encapsulam efeitos colaterais
- ✅ Reutilizáveis entre componentes

### 4. **Components & Pages (Views)**
**Responsabilidade**: Interface do usuário e apresentação.

**Refatorações realizadas**:
- `Index.tsx` - Usa `useAuth` e `useCart`
- `Cart.tsx` - Usa `useAuth`, `useOrder` e `useCart`
- `Login.tsx` - Usa `useAuth`
- `Register.tsx` - Usa `useAuth`

**Características**:
- ✅ Focados apenas na UI
- ✅ Consomem hooks para dados/lógica
- ✅ Componentes mais limpos e focados
- ✅ Fáceis de testar e manter

## 🔄 Fluxo de Dados

```
User Interaction → Component → Hook → Service → Data/API
                                ↓
Component ← Hook ← Service Response
```

**Exemplo prático - Adicionar item ao carrinho**:
1. Usuário clica "Adicionar ao carrinho" (Component)
2. Component chama `addToCart` do hook `useCart`
3. Hook usa `CartService.createCartItem` para calcular
4. Hook atualiza estado local
5. Component re-renderiza com novo estado

## ✅ Benefícios da Implementação

### **Separação de Responsabilidades**
- Models: Apenas estruturas de dados
- Services: Apenas lógica de negócio
- Hooks: Apenas ponte React
- Views: Apenas apresentação

### **Testabilidade**
- Services podem ser testados isoladamente
- Hooks podem ser testados com React Testing Library
- Components focam apenas na UI

### **Reutilização**
- Services são agnósticos ao React
- Hooks encapsulam lógica React complexa
- Components podem ser reutilizados facilmente

### **Manutenibilidade**
- Código organizado por responsabilidade
- Bugs são mais fáceis de localizar
- Novas funcionalidades têm local claro

### **Performance**
- Hooks usam `useCallback` para otimização
- Re-renders controlados e eficientes
- Estado bem gerenciado

## 🔧 Diferenças do MVC Tradicional

| Aspecto | MVC Tradicional | MVC React-Friendly |
|---------|----------------|-------------------|
| Controllers | Classes com métodos | Services + Hooks |
| Estado | No modelo/controller | Nos Hooks |
| Reatividade | Manual | Automática (React) |
| Testabilidade | Separada | Integrada com React |
| Reutilização | Limitada | Alta |


## 📝 Convenções Estabelecidas

- **Services**: Classes com métodos estáticos
- **Hooks**: Prefixo `use` + funcionalidade
- **Models**: Interfaces em PascalCase
- **Arquivos**: camelCase para services, PascalCase para models
- **Imports**: Usar paths absolutos com `@/`

## 🎯 Conclusão

A implementação mantém todos os benefícios do MVC tradicional enquanto se adapta perfeitamente ao paradigma React. O resultado é um código mais limpo, testável e maintível, seguindo as melhores práticas do ecossistema React.
