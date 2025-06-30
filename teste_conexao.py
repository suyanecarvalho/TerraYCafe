
from terraycafe.model.sqlite.settings.connection import DBConnection


def main() -> str:    
    
    try:        
        # Cria conexão
        db = DBConnection()
        db.connect_to_db()
        
        print("Conexão feita")
        
    except Exception as e:
        print(f"Falha na conexão: {e}")


if __name__ == "__main__":
    main()
    
