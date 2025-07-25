import { useLocation, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

const NotFound = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen place-items-centr justify-items-center bg-[#fff9f3] p-10">
      <div className="align-center text-center text-[#745516] font-bold">
        <img className="rounded-xl p-4" src="public/not-found.png" alt="" />
        Página não encontrada
      </div>
      <div className="align-center p-6">
        <Button 
        className="bg-[#f8e0b3] text-[#41242b] hover:bg-[#d1a164] hover:text-white"
        onClick={() => navigate("/")}
        >
          <ArrowLeft/>
          Voltar para tela inicial
        </Button>
      </div>
    </div>
  );
};

export default NotFound;
