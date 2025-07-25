import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

const Register = () => {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [telefone, setTelefone] = useState("");
  const [senha, setSenha] = useState("");
  const navigate = useNavigate();
  const { register } = useAuth();

  const handleSubmit = async(e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register ({nome, email, telefone, senha});
      navigate("/login");
    } catch (error){
      console.error('Registration failed:',error);
    }
  };

  return (
    <div className="">
      <div className="min-h-screen bg-gradient-to-b from-orange-50 to-orange-100 flex items-center justify-center p-4">
        <div className="w-full max-w-4xl grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="flex items-center justify-center">
            <Card className="w-full max-w-md bg-[#fff9f3]">
              <CardHeader className="text-center">
                <div className="flex items-center justify-between mb-4 text-[#754416]">
                  <Button
                    variant="ghost"
                    onClick={() => navigate("/login")}
                    className="p-2"
                  >
                    <ArrowLeft className="h-5 w-5" />
                    Voltar
                  </Button>
                </div>
                <div className="py-2">
                  <img 
                  src="public/logo-bege.png" 
                  className="w-2/3 mx-auto item-center"
                  alt="" />
                </div>
                <CardTitle className="text-2xl text-[#754416] font-bold font-serif">
                  Criar nova conta
                </CardTitle>
                <CardDescription>
                  Seu café, no seu tempo, do seu jeitinho 💛
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-[#745516]" htmlFor="name">Nome completo:</Label>
                    <Input
                      id="name"
                      type="text"
                      placeholder="Seu nome completo"
                      value={nome}
                      onChange={(e) => setNome(e.target.value)}
                      required
                      className="rounded-lg"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label className="text-[#745516]" htmlFor="email">Email:</Label>
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
                    <Label className="text-[#745516]" htmlFor="phone">Telefone:</Label>
                    <Input
                      id="phone"
                      type="tel"
                      placeholder="(11) 99999-9999"
                      value={telefone}
                      onChange={(e) => setTelefone(e.target.value)}
                      required
                      className="rounded-lg"
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label className="text-[#745516]" htmlFor="password">Senha:</Label>
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

                  <Button 
                    type="submit"
                    className="w-full bg-[#d7dfaf] hover:bg-[#e2ce87] text-[#754416] font-bold transition-colors duration-300 rounded-full"
                    onClick={handleSubmit}
                  >
                    Cadastrar
                  </Button>

                  <div className="text-center">
                    <button
                      type="button"
                      onClick={() => navigate("/login")}
                      className="text-orange-600 hover:text-orange-700 font-medium"
                    >
                      Já tenho uma conta
                    </button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </div>

          <div className="hidden lg:block rounded-xl">
            <img 
            src="public\cafe-login.png"
            className="h-full rounded-xl"
            ></img>
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

export default Register;
