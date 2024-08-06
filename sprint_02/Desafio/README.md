# Documentação do Desafio de Modelagem de Dados 

## Normalização e Criação de Tabelas no Banco de Dados
Este documento irá explicar o processo de criação das tabelas normalizadas no banco de dados, garantindo que elas sejam criadas apenas se não existirem. Cada seção contém o código SQL necessário e uma breve explicação sobre o que ele faz.

## Script de Criação de Tabelas Normalizadas:
Este script cria as tabelas normalizadas no banco de dados concessionaria.db

# Clientes
## Código SQL

```bash
-- Verifica se a tabela Clientes já existe e a cria se não existir
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Clientes' AND xtype='U')
BEGIN
    CREATE TABLE Clientes (
        idCliente INT PRIMARY KEY, -- ID único do cliente, chave primária
        nomeCliente VARCHAR(255), -- Nome do cliente
        cidadeCliente VARCHAR(255), -- Cidade onde o cliente reside
        estadoCliente VARCHAR(255), -- Estado onde o cliente reside
        paisCliente VARCHAR(255) -- País onde o cliente reside
    );
END;
```

## Interpretação
  - Verifica se a tabela Clientes não existe no banco de dados
  - Se não existir, vai criar com as colunas:
  - id: Identificador único do cliente
  - nome: Nome do cliente
  - cidade: Cidade onde o cliente reside
  - eatado: Estado onde o cliente reside
  - pais: País onde reside

# Carros

```bash
-- Verifica se a tabela Carros já existe e a cria se não existir
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Carros' AND xtype='U')
BEGIN
    CREATE TABLE Carros (
        idCarro INT PRIMARY KEY, -- ID único do carro, chave primária
        marcaCarro VARCHAR(255), -- Marca do carro
        modeloCarro VARCHAR(255), -- Modelo do carro
        anoCarro INT, -- Ano de fabricação do carro
        kmCarro INT, -- Quilometragem do carro
        classiCarro VARCHAR(255) -- Classificação do carro
    );
END;
```

## Interpretação
  - Verifica se a tabela Carros não existe no banco de dados
  - Se não existir, vai criar com as colunas:
  - id: identificador único do carro 
  - marca: Marca do carro
  - modelo: Modelo do carro
  - ano: Ano de fabricação 
  - km: Quilometragem do carro
  - classi: Classificação do carro

# Locações

```bash
-- Verifica se a tabela Locacoes já existe e a cria se não existir
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Locacoes' AND xtype='U')
BEGIN
    CREATE TABLE Locacoes (
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
END;
```

## Interpretação
  - verifica se a tabela Locacoes não existe no banco de dados
  - Se não existir, vai criar com as colunas:
  - idLocacao: Identificador único da locação, chave primária
  - idCliente: Identificador do cliente, chave estrangeira para a tabela Clientes
  - idCarro: Identificador do carro, chave estrangeira para a tabela Carros
  - dataLocacao: Data da locação
  - dataEntrega: Data de entrega do carro
  - tipoCombustivel: Tipo de combustível utilizado
  - qtdDiaria: Quantidade de diárias
  - vltDiaria: Valor da diária

# Vendedores

```bash
-- Verifica se a tabela Vendedores já existe e a cria se não existir
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Vendedores' AND xtype='U')
BEGIN
    CREATE TABLE Vendedores (
        idVendedor INT PRIMARY KEY, -- ID único do vendedor, chave primária
        nomeVendedor VARCHAR(255), -- Nome do vendedor
        sexoVendedor VARCHAR(1), -- Sexo do vendedor
        estadoVendedor VARCHAR(255) -- Estado onde o vendedor reside
    );
END;
```

## Interpretação
  - verifica se a tabela Vendedores não existe no banco de dados
  - Se não existir, vai criar com as colunas:
  - idVendedor: Identificador único do vendedor
  - nomeVendedor: Nome do vendedor
  - sexoVendedor: Sexo do vendedor
  - estadoVendedor: Estado onde o vendedor reside

## Transações

```bash
-- Verifica se a tabela Transacoes já existe e a cria se não existir
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Transacoes' AND xtype='U')
BEGIN
    CREATE TABLE Transacoes (
        idTransacao INT PRIMARY KEY, -- ID único da transação, chave primária
        idLocacao INT, -- ID da locação, chave estrangeira para a tabela Locacoes
        idVendedor INT, -- ID do vendedor, chave estrangeira para a tabela Vendedores
        valor DECIMAL(10, 2), -- Valor da transação
        FOREIGN KEY (idLocacao) REFERENCES Locacoes(idLocacao), -- Define idLocacao como chave estrangeira
        FOREIGN KEY (idVendedor) REFERENCES Vendedores(idVendedor) -- Define idVendedor como chave estrangeira
    );
END;
```

## Interpretação
  - verifica se a tabela Vendedores não existe no banco de dados
  - Se não existir, vai criar com as colunas:
  - idTransacao: Identificador único da transação
  - idLocacao: Identificador da locação
  - idVendedor: Identificador do vendedor
  - valor: Valor da transação


# Criação Dimensional
## Script de Criação de Tabelas Dimensionais 

```bash
-- Criação da Tabela de Dimensão Cliente
CREATE TABLE IF NOT EXISTS DimCliente (
    idCliente INT PRIMARY KEY, -- ID único do cliente, chave primária
    nomeCliente VARCHAR(255), -- Nome do cliente
    cidadeCliente VARCHAR(255), -- Cidade onde o cliente reside
    estadoCliente VARCHAR(255), -- Estado onde o cliente reside
    paisCliente VARCHAR(255) -- País onde o cliente reside
);
```

```bash
-- Criação da Tabela de Dimensão Carro
CREATE TABLE IF NOT EXISTS DimCarro (
    idCarro INT PRIMARY KEY, -- ID único do carro, chave primária
    marcaCarro VARCHAR(255), -- Marca do carro
    modeloCarro VARCHAR(255), -- Modelo do carro
    anoCarro INT, -- Ano de fabricação do carro
    kmCarro INT, -- Quilometragem do carro
    classiCarro VARCHAR(255) -- Classificação do carro
);
```

```bash
-- Criação da Tabela de Dimensão Vendedor
CREATE TABLE IF NOT EXISTS DimVendedor (
    idVendedor INT PRIMARY KEY, -- ID único do vendedor, chave primária
    nomeVendedor VARCHAR(255), -- Nome do vendedor
    sexoVendedor VARCHAR(1), -- Sexo do vendedor
    estadoVendedor VARCHAR(255) -- Estado onde o vendedor reside
);
```
```bash
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
```

```bash
-- Criação da Tabela Fato Transação
CREATE TABLE IF NOT EXISTS FactTransacao (
    idTransacao INT PRIMARY KEY, -- ID único da transação, chave primária
    idLocacao INT, -- ID da locação, chave estrangeira para a tabela FactLocacao
    idVendedor INT, -- ID do vendedor, chave estrangeira para a tabela DimVendedor
    valor DECIMAL(10, 2), -- Valor da transação
    FOREIGN KEY (idLocacao) REFERENCES FactLocacao(idLocacao), -- Define idLocacao como chave estrangeira
    FOREIGN KEY (idVendedor) REFERENCES DimVendedor(idVendedor) -- Define idVendedor como chave estrangeira
);
```

## Explicação dos Passos de Normalização
A normalização foi feita seguindo as formas normais para reduzir a redundância e melhorar a integridade dos dados. Cada tabela foi criada para armazenar informações específicas, evitando a duplicação de dados. As tabelas foram desenhadas com chaves primárias para identificação única de registros e chaves estrangeiras para manter relacionamentos entre tabelas.

## Desenho da Modelagem Relacional (Após Normalização)
  - Clientes: Armazena informações sobre os clientes
  - Carros: Armazena informações sobre os carros
  - Locacoes: Armazena informações sobre as locações, relacionando clientes e carros
  - Vendedores: Armazena informações sobre os vendedores
  - Transacoes: Armazena informações sobre as transações, relacionando locações e vendedores


## Desenho da Modelagem Dimensional
  - DimCliente: Dimensão que armazena informações sobre os clientes
  - DimCarro: Dimensão que armazena informações sobre os carros
  - DimVendedor: Dimensão que armazena informações sobre os vendedores
  - FactLocacao: Tabela fato que armazena informações sobre as locações
  - FactTransacao: Tabela fato que armazena informações sobre as transações


## Entregáveis
  - Scripts SQL de criação de tabelas normalizadas (M.Relacional.sql).
  - Scripts SQL de criação de tabelas dimensionais (M.Dimensional.sql).
  - Explicação breve dos passos seguidos para a normalização.
  - Desenho da modelagem relacional após a normalização.
  - Desenho da modelagem dimensional.
