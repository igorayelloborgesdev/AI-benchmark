USE GeminiDB;
GO

CREATE TABLE SegmentoClassificacao (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Sigla VARCHAR(10) NOT NULL,
    Descritivo VARCHAR(255) NOT NULL
);
CREATE TABLE SetorEconomico (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Descritivo VARCHAR(255) NOT NULL
);
CREATE TABLE Subsetor (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Descritivo VARCHAR(255) NOT NULL
);
CREATE TABLE Segmento (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Descritivo VARCHAR(255) NOT NULL
);
CREATE TABLE Empresa (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Nome VARCHAR(255) NOT NULL,
    Codigo VARCHAR(20) NOT NULL,
    SegmentoClassificacaoID INT NULL, -- Chave estrangeira para SegmentoClassificacao (não obrigatória)
    SetorEconomicoID INT NOT NULL, -- Chave estrangeira para SetorEconomico (obrigatória)
    SubsetorID INT NOT NULL, -- Chave estrangeira para Subsetor (obrigatória)
    SegmentoID INT NOT NULL, -- Chave estrangeira para Segmento (obrigatória)
    FOREIGN KEY (SegmentoClassificacaoID) REFERENCES SegmentoClassificacao(ID),
    FOREIGN KEY (SetorEconomicoID) REFERENCES SetorEconomico(ID),
    FOREIGN KEY (SubsetorID) REFERENCES Subsetor(ID),
    FOREIGN KEY (SegmentoID) REFERENCES Segmento(ID)
);