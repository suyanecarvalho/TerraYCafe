
CREATE TABLE IF NOT EXISTS Bebida (
    id bigint NOT NULL CONSTRAINT Bebida_pk PRIMARY KEY ,
    nome varchar(255) NOT NULL,
    descricao varchar(255) NOT NULL,
    preco_base float NOT NULL,
    categoria varchar(255) NOT NULL
);

-- Table: Cliente
CREATE TABLE IF NOT EXISTS Cliente (
    id bigint NOT NULL CONSTRAINT Cliente_pk PRIMARY KEY ,
    nome varchar(255) NOT NULL,
    email varchar(255) NOT NULL UNIQUE,
    pontos_fidelidade int NOT NULL
);

-- Table: Ingredientes
CREATE TABLE IF NOT EXISTS Ingredientes (
    id bigint NOT NULL CONSTRAINT Ingredientes_pk PRIMARY KEY ,
    nome varchar(255) NOT NULL,
    tipo varchar(255) NOT NULL,
    preco_adicional float NOT NULL
);

-- Table: Pedidos
CREATE TABLE IF NOT EXISTS Pedidos (
    id bigint NOT NULL CONSTRAINT Pedidos_pk PRIMARY KEY ,
    status varchar(50) NOT NULL,
    valor_total float NOT NULL,
    forma_pagamento varchar(50) NOT NULL,
    desconto int NOT NULL,
    data_hora datetime NOT NULL,
    Cliente_id int NOT NULL,
    CONSTRAINT Pedidos_Cliente FOREIGN KEY (Cliente_id)
    REFERENCES Cliente (id)
);

-- Table: item_pedido (criada antes de Personalizacao devido à referência)
CREATE TABLE IF NOT EXISTS item_pedido (
    id bigint NOT NULL CONSTRAINT item_pedido_pk PRIMARY KEY ,
    pedido_id bigint NOT NULL,
    preco float NOT NULL,
    Bebida_id bigint NOT NULL,
    CONSTRAINT item_pedido_Pedidos FOREIGN KEY (pedido_id)
    REFERENCES Pedidos (id),
    CONSTRAINT item_pedido_Bebida FOREIGN KEY (Bebida_id)
    REFERENCES Bebida (id)
);

-- Table: Personalizacao
CREATE TABLE IF NOT EXISTS Personalizacao (
    id bigint NOT NULL CONSTRAINT Personalizacao_pk PRIMARY KEY ,
    Ingredientes_id bigint NOT NULL,
    item_pedido_id bigint NOT NULL,
    CONSTRAINT Personalizacao_Ingredientes FOREIGN KEY (Ingredientes_id)
    REFERENCES Ingredientes (id),
    CONSTRAINT Personalizacao_item_pedido FOREIGN KEY (item_pedido_id)
    REFERENCES item_pedido (id)
);

-- End of file.

