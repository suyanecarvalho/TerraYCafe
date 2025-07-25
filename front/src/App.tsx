import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Login from "./pages/Login";
import Register from "./pages/Register";
import History from "./pages/History";
import PaymentConfirmation from "./pages/PaymentConfirmation";
import Kitchen from "./pages/Kitchen";
import KitchenDashboard from "./pages/KitchenDashboard";
import KitchenIngredients from "./pages/KitchenIngredients";
import KitchenDiscounts from "./pages/KitchenDiscounts";
import KitchenOrdersHistory from "./pages/KitchenOrdersHistory";
import NotFound from "./pages/NotFound";
import KitchenLogin from "./pages/KitchenLogin";
import OrderStatus from "./pages/OrderStatus";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/history" element={<History />} />
          <Route path="/payment-confirmation" element={<PaymentConfirmation />} />
          <Route path="/order-status" element={<OrderStatus />} />

          {/* Kitchen Routes */}
          <Route path="/kitchenlogin" element={<KitchenLogin />} />
          <Route path="/kitchen" element={<Kitchen />} />
          <Route path="/kitchen/dashboard" element={<KitchenDashboard />} />
          <Route path="/kitchen/ingredients" element={<KitchenIngredients />} />
          <Route path="/kitchen/discounts" element={<KitchenDiscounts />} />
          <Route path="/kitchen/orders-history" element={<KitchenOrdersHistory />} />
          
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;