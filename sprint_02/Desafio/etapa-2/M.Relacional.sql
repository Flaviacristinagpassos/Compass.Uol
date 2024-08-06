-- Verifica se a tabela Clientes já existe e a cria se não existir
CREATE TABLE IF NOT EXISTS Clientes (
    idCliente INT PRIMARY KEY, -- ID único do cliente, chave primária
    nomeCliente VARCHAR(255), -- Nome do cliente
    cidadeCliente VARCHAR(255), -- Cidade onde o cliente reside
    estadoCliente VARCHAR(255), -- Estado onde o cliente reside
    paisCliente VARCHAR(255) -- País onde o cliente reside
);

-- Verifica se a tabela Carros já existe e a cria se não existir
CREATE TABLE IF NOT EXISTS Carros (
    idCarro INT PRIMARY KEY, -- ID único do carro, chave primária
    marcaCarro VARCHAR(255), -- Marca do carro
    modeloCarro VARCHAR(255), -- Modelo do carro
    anoCarro INT, -- Ano de fabricação do carro
    kmCarro INT, -- Quilometragem do carro
    classiCarro VARCHAR(255) -- Classificação do carro
);

-- Verifica se a tabela Locacoes já existe e a cria se não existir
CREATE TABLE IF NOT EXISTS Locacoes (
    idLocacao INT PRIMARY KEY, -- ID único da locação, chave primária
    idCliente INT, -- ID do cliente, chave estrangeira para a tabela Clientes
    idCarro INT, -- ID do carro, chave estrangeira para a tabela Carros
    dataLocacao DATE, -- Data da locação
    dataEntrega DATE, -- Data de entrega do carro
    tipoCombustivel VARCHAR(255), -- Tipo de combustível utilizado
    qtdDiaria INT, -- Quantidade de diárias
    vltDiaria DECIMAL(10, 2), -- Valor da diária
    FOREIGN KEY (idCliente) REFERENCES Clientes(idCliente), -- Define idCliente como chave estrangeira
    FOREIGN KEY (idCarro) REFERENCES Carros(idCarro) -- Define idCarro como chave estrangeira
);

-- Verifica se a tabela Vendedores já existe e a cria se não existir
CREATE TABLE IF NOT EXISTS Vendedores (
    idVendedor INT PRIMARY KEY, -- ID único do vendedor, chave primária
    nomeVendedor VARCHAR(255), -- Nome do vendedor
    sexoVendedor VARCHAR(1), -- Sexo do vendedor
    estadoVendedor VARCHAR(255) -- Estado onde o vendedor reside
);

-- Verifica se a tabela Transacoes já existe e a cria se não existir
CREATE TABLE IF NOT EXISTS Transacoes (
    idTransacao INT PRIMARY KEY, -- ID único da transação, chave primária
    idLocacao INT, -- ID da locação, chave estrangeira para a tabela Locacoes
    idVendedor INT, -- ID do vendedor, chave estrangeira para a tabela Vendedores
    valor DECIMAL(10, 2), -- Valor da transação
    FOREIGN KEY (idLocacao) REFERENCES Locacoes(idLocacao), -- Define idLocacao como chave estrangeira
    FOREIGN KEY (idVendedor) REFERENCES Vendedores(idVendedor) -- Define idVendedor como chave estrangeira
);
