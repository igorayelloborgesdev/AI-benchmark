USE MetaAIDB;
GO

CREATE TABLE dbo.SegmentoClassificacao (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Chave primária autoincrementada
    Sigla VARCHAR(10) NOT NULL,        -- Sigla extraída dos parênteses
    Descritivo VARCHAR(255) NOT NULL   -- Texto após os parênteses
);

CREATE TABLE dbo.[SetorEconomico] (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Chave primária autoincrementada
    Descritivo VARCHAR(255) NOT NULL   -- Nome do setor econômico
);

CREATE TABLE dbo.Subsetor (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Chave primária autoincrementada
    Descritivo VARCHAR(255) NOT NULL   -- Nome do subsetor
);

CREATE TABLE dbo.Segmento (
    ID INT IDENTITY(1,1) PRIMARY KEY,  -- Chave primária autoincrementada
    Descritivo VARCHAR(255) NOT NULL   -- Nome do segmento
);

CREATE TABLE dbo.Empresa (
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
        REFERENCES dbo.SegmentoClassificacao(ID),
    
    CONSTRAINT FK_Empresa_SetorEconomico FOREIGN KEY (SetorEconomicoID) 
        REFERENCES dbo.SetorEconomico(ID),
    
    CONSTRAINT FK_Empresa_Subsetor FOREIGN KEY (SubsetorID) 
        REFERENCES dbo.Subsetor(ID),
    
    CONSTRAINT FK_Empresa_Segmento FOREIGN KEY (SegmentoID) 
        REFERENCES dbo.Segmento(ID)
);

CREATE TABLE CDI_Diario (
    Data DATE NOT NULL,
    Valor FLOAT NOT NULL,
    PRIMARY KEY (Data)
);

CREATE TABLE IBOV_Historico (
    Data DATE NOT NULL PRIMARY KEY,
    Abertura FLOAT NOT NULL,
    Alta FLOAT NOT NULL,
    Baixa FLOAT NOT NULL,
    Fechamento FLOAT NOT NULL,
    Volume BIGINT NOT NULL
);

CREATE TABLE Acao_Historico (
    Data DATE NOT NULL,
    Codigo VARCHAR(10) NOT NULL,
    Abertura FLOAT NOT NULL,
    Alta FLOAT NOT NULL,
    Baixa FLOAT NOT NULL,
    Fechamento FLOAT NOT NULL,
    Volume BIGINT NOT NULL,
    PRIMARY KEY (Data, Codigo) -- Permite várias ações diferentes na mesma data
);