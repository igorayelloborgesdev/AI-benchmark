USE DeepSeekDB;
GO

CREATE TABLE SegmentoClassificacao (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Coluna ID como primary key e autoincremento
    Sigla NVARCHAR(10) NOT NULL,       -- Coluna para a sigla (tamanho máximo de 10 caracteres)
    Descritivo NVARCHAR(100) NOT NULL  -- Coluna para o descritivo (tamanho máximo de 100 caracteres)
);
CREATE TABLE [SetorEconomico] (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Coluna ID como primary key e autoincremento
    Descritivo NVARCHAR(100) NOT NULL  -- Coluna para o descritivo (tamanho máximo de 100 caracteres)
);
CREATE TABLE Subsetor (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Coluna ID como primary key e autoincremento
    Descritivo NVARCHAR(100) NOT NULL  -- Coluna para o descritivo (tamanho máximo de 100 caracteres)
);
CREATE TABLE Segmento (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Chave primária autoincrementada
    Descritivo VARCHAR(255) NOT NULL   -- Nome do segmento
);
CREATE TABLE Empresa (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Chave primária autoincrementada
    Nome VARCHAR(255) NOT NULL,         -- Nome da empresa
    Codigo VARCHAR(50) NOT NULL,        -- Código/Sigla da empresa
    
    -- Chaves estrangeiras
    SegmentoClassificacaoID INT NULL,   -- FK opcional (NÃO obrigatória)
    SetorEconomicoID INT NOT NULL,      -- FK obrigatória
    SubsetorID INT NOT NULL,            -- FK obrigatória
    SegmentoID INT NOT NULL,            -- FK obrigatória

    -- Definição das chaves estrangeiras
    CONSTRAINT FK_Empresa_SegmentoClassificacao FOREIGN KEY (SegmentoClassificacaoID) 
        REFERENCES SegmentoClassificacao(ID),
    
    CONSTRAINT FK_Empresa_SetorEconomico FOREIGN KEY (SetorEconomicoID) 
        REFERENCES SetorEconomico(ID),
    
    CONSTRAINT FK_Empresa_Subsetor FOREIGN KEY (SubsetorID) 
        REFERENCES Subsetor(ID),
    
    CONSTRAINT FK_Empresa_Segmento FOREIGN KEY (SegmentoID) 
        REFERENCES Segmento(ID)
);