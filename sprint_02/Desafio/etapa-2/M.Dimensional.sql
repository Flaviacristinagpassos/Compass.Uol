-- Criação da Tabela de Dimensão Cliente
CREATE TABLE IF NOT EXISTS DimCliente (
    idCliente INT PRIMARY KEY, -- ID único do cliente, chave primária
    nomeCliente VARCHAR(255), -- Nome do cliente
    cidadeCliente VARCHAR(255), -- Cidade onde o cliente reside
    estadoCliente VARCHAR(255), -- Estado onde o cliente reside
    paisCliente VARCHAR(255) -- País onde o cliente reside
);

-- Criação da Tabela de Dimensão Carro
CREATE TABLE IF NOT EXISTS DimCarro (
    idCarro INT PRIMARY KEY, -- ID único do carro, chave primária
    marcaCarro VARCHAR(255), -- Marca do carro
    modeloCarro VARCHAR(255), -- Modelo do carro
    anoCarro INT, -- Ano de fabricação do carro
    kmCarro INT, -- Quilometragem do carro
    classiCarro VARCHAR(255) -- Classificação do carro
);

-- Criação da Tabela de Dimensão Vendedor
CREATE TABLE IF NOT EXISTS DimVendedor (
    idVendedor INT PRIMARY KEY, -- ID único do vendedor, chave primária
    nomeVendedor VARCHAR(255), -- Nome do vendedor
    sexoVendedor VARCHAR(1), -- Sexo do vendedor
    estadoVendedor VARCHAR(255) -- Estado onde o vendedor reside
);

-- Criação da Tabela Fato Locação
CREATE TABLE IF NOT EXISTS FactLocacao (
    idLocacao INT PRIMARY KEY, -- ID único da locação, chave primária
    idCliente INT, -- ID do cliente, chave estrangeira para a tabela DimCliente
    idCarro INT, -- ID do carro, chave estrangeira para a tabela DimCarro
    dataLocacao DATE, -- Data da locação
    dataEntrega DATE, -- Data de entrega do carro
    tipoCombustivel VARCHAR(255), -- Tipo de combustível utilizado
    qtdDiaria INT, -- Quantidade de diárias
    vltDiaria DECIMAL(10, 2), -- Valor da diária
    FOREIGN KEY (idCliente) REFERENCES DimCliente(idCliente), -- Define idCliente como chave estrangeira
    FOREIGN KEY (idCarro) REFERENCES DimCarro(idCarro) -- Define idCarro como chave estrangeira
);

-- Criação da Tabela Fato Transação
CREATE TABLE IF NOT EXISTS FactTransacao (
    idTransacao INT PRIMARY KEY, -- ID único da transação, chave primária
    idLocacao INT, -- ID da locação, chave estrangeira para a tabela FactLocacao
    idVendedor INT, -- ID do vendedor, chave estrangeira para a tabela DimVendedor
    valor DECIMAL(10, 2), -- Valor da transação
    FOREIGN KEY (idLocacao) REFERENCES FactLocacao(idLocacao), -- Define idLocacao como chave estrangeira
    FOREIGN KEY (idVendedor) REFERENCES DimVendedor(idVendedor) -- Define idVendedor como chave estrangeira
);
