from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from terraycafe.model.sqlite.settings.connection import Base, db_connection
from terraycafe.controllers.rota_cliente import router as cliente_router
from terraycafe.controllers.rota_pedido import router as pedido_router
from terraycafe.controllers.rota_ingrediente import router as ingrediente_router
from terraycafe.controllers.rota_bebida import router as bebida_router
from terraycafe.controllers.rota_websocket import router as websocket_router

app = FastAPI(title="TerrayCaféAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", 
    "http://127.0.0.1:3000",
    "http://localhost:8080",        
    "http://127.0.0.1:8080",        
    "http://192.168.0.6:8080",
    "http://10.134.10.154:8080",
    "http://192.168.1.9:8080",
    "http://192.168.0.7:8080", 
    "http://localhost:8080",
   ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    db_conn = db_connection
    engine = db_conn.get_engine()
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas")
except Exception as e:
    print(e)

app.include_router(cliente_router)
app.include_router(pedido_router)
app.include_router(ingrediente_router)
app.include_router(bebida_router)
app.include_router(websocket_router)