import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, ChefHat } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

const Login = () => {
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = (e: React.FormEvent) => { // chama o email, senha de Auth
    e.preventDefault();
    login(email, senha);
    navigate("/");
  };

  return (
    <div className="">
      <div className="min-h-screen bg-gradient-to-b from-orange-50 to-orange-100 flex items-center justify-center p-4">
        <div className="w-full max-w-4xl grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="flex items-center justify-center">
            <Card className="w-full max-w-md bg-[#fff9f3] rounded-lg">
              <CardHeader className="text-center">
                <div className="flex items-center justify-between mb-4 text-[#d1a164]">
                  <Button
                    variant="ghost"
                    onClick={() => navigate("/")}
                    className="p-2"
                  >
                    <ArrowLeft className="h-5 w-5" />
                    Voltar
                  </Button>
                  <div></div>
                </div>
                <div>
                  <img 
                    src="public/logo-bege.png" 
                    alt="Cozy Cafe Logo" 
                    className="w-2/3 item-center mx-auto mb-4"
                  />
                </div>
                <CardTitle className="text-2xl text-[#754416] font-bold font-serif">
                  Acesse sua conta
                </CardTitle>
                <CardDescription>
                  Seu café, no seu tempo, do seu jeitinho 💛
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="email">Email:</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="exemplo@email.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      className="rounded-lg"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="password">Senha:</Label>
                    <Input
                      id="password"
                      type="password"
                      placeholder="pelo menos 8 caracteres"
                      value={senha}
                      onChange={(e) => setSenha(e.target.value)}
                      required
                      className="rounded-lg"
                    />
                  </div>

                  <div className="text-right">
                    <button
                      type="button"
                      className="text-sm text-orange-600 hover:text-orange-700"
                    >
                      Esqueceu a senha?
                    </button>
                  </div>
                  
                  <Button 
                    type="submit"
                    className="w-full bg-[#d7dfaf] hover:bg-[#e2ce87] text-[#754416] font-bold transition-colors duration-300 rounded-full"
                  >
                    Entrar
                  </Button>

                  <div className="text-center">
                    <button
                      type="button"
                      onClick={() => navigate("/register")}
                      className="text-orange-600 hover:text-orange-700 font-medium"
                    >
                      Cadastre-se
                    </button>
                  </div>
                  <div className="text-center">
                    <Button
                      variant="outline"
                      onClick={() => navigate("/kitchenlogin")}
                      className="w-full border-orange-300 text-orange-700 hover:bg-orange-100 rounded-full"
                    >
                      <ChefHat className="h-4 w-4 mr-2" />
                      Entrar como cozinha
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>

          <div className="hidden lg:block rounded-lg">
            <img 
            src="public/cafe-login.png" 
            alt="" 
            className="rounded-xl h-full"
            />
          </div>
      </div>
      </div>

    <footer className="bg-[#412a2b]">
        <div className="max-w-6xl mx-auto px-5 py-8 flex justify-evenly gap-6 items-center">
          <div className="max-w-xs">
            <p className="text-[#f8e0b3]">
              TERRA&CAFÉ
            </p>
            <h1 className="text-[#ff751f] text-2xl font-bold font-serif my-4">
              Seu café, no seu tempo do seu jeitinho
            </h1>
            <p className="text-[#776c59]">
              Todos os direitos reservados © 2025
            </p>
          </div>
          <div className="justify-items-start max-w-xs">
            <p className="text-[#ff751f] my-2">
              Sobre Nós
            </p>
            <p className="text-[#f8e0b3]">
              Conheça mais sobre a nossa história e missão.
            </p>
            <p className="text-[#f8e0b3]">
              Contatos
            </p>
            <p className="text-[#f8e0b3]">
              Endereços
            </p>
          </div>
        </div>
      </footer>
  </div>
  );
};

export default Login;
