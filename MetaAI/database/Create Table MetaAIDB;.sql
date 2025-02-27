USE MetaAIDB;
GO

CREATE TABLE [dbo].[SegmentoClassificacao] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [Sigla] VARCHAR(10) NOT NULL,
    [Descritivo] VARCHAR(100) NOT NULL
);
CREATE TABLE [dbo].[Setor_Economico] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [Descritivo] VARCHAR(100) NOT NULL
);
CREATE TABLE [dbo].[Subsetor] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [Descritivo] VARCHAR(100) NOT NULL
);
CREATE TABLE [dbo].[Segmento] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [Descritivo] VARCHAR(100) NOT NULL
);
CREATE TABLE [dbo].[Empresa] (
    [ID] INT IDENTITY(1,1) PRIMARY KEY,
    [Nome] VARCHAR(100) NOT NULL,
    [Codigo] VARCHAR(10) NOT NULL,
    [SetorEconomicoID] INT NOT NULL,
    [SubsetorID] INT NOT NULL,
    [SegmentoID] INT NOT NULL,
    [SegmentoClassificacaoID] INT NULL,
    CONSTRAINT [FK_Empresa_SetorEconomico] FOREIGN KEY ([SetorEconomicoID]) REFERENCES [dbo].[Setor_Economico]([ID]),
    CONSTRAINT [FK_Empresa_Subsetor] FOREIGN KEY ([SubsetorID]) REFERENCES [dbo].[Subsetor]([ID]),
    CONSTRAINT [FK_Empresa_Segmento] FOREIGN KEY ([SegmentoID]) REFERENCES [dbo].[Segmento]([ID]),
    CONSTRAINT [FK_Empresa_SegmentoClassificacao] FOREIGN KEY ([SegmentoClassificacaoID]) REFERENCES [dbo].[SegmentoClassificacao]([ID])
);