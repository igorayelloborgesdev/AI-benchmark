USE CopilotDB;
GO

CREATE TABLE SegmentoClassificacao (
    ID INT PRIMARY KEY IDENTITY(1,1),
    sigla NVARCHAR(10) NOT NULL,
    descritivo NVARCHAR(255) NOT NULL
);
CREATE TABLE [SetorEconomico] (
    ID INT PRIMARY KEY IDENTITY(1,1),
    descritivo NVARCHAR(255) NOT NULL
);
CREATE TABLE Subsetor (
    ID INT PRIMARY KEY IDENTITY(1,1),
    descritivo NVARCHAR(255) NOT NULL
);
CREATE TABLE Segmento (
    ID INT PRIMARY KEY IDENTITY(1,1),
    descritivo NVARCHAR(255) NOT NULL
);
CREATE TABLE Empresa (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Nome NVARCHAR(255) NOT NULL,
    codigo NVARCHAR(10) NOT NULL,
    SegmentoClassificacaoID INT NULL,
    SetorEconomicoID INT NOT NULL,
    SubsetorID INT NOT NULL,
    SegmentoID INT NOT NULL,
    CONSTRAINT FK_Empresa_SegmentoClassificacao FOREIGN KEY (SegmentoClassificacaoID) REFERENCES dbo.SegmentoClassificacao(ID),
    CONSTRAINT FK_Empresa_SetorEconomico FOREIGN KEY (SetorEconomicoID) REFERENCES dbo.SetorEconomico(ID),
    CONSTRAINT FK_Empresa_Subsetor FOREIGN KEY (SubsetorID) REFERENCES dbo.Subsetor(ID),
    CONSTRAINT FK_Empresa_Segmento FOREIGN KEY (SegmentoID) REFERENCES dbo.Segmento(ID)
);