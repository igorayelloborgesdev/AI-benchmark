USE ChatGPTDB

delete from Empresa
delete from Segmento
delete from SegmentoClassificacao
delete from SetorEconomico
delete from Subsetor

DBCC CHECKIDENT ('Empresa', RESEED, 0);
DBCC CHECKIDENT ('Segmento', RESEED, 0);
DBCC CHECKIDENT ('SegmentoClassificacao', RESEED, 0);
DBCC CHECKIDENT ('SetorEconomico', RESEED, 0);
DBCC CHECKIDENT ('Subsetor', RESEED, 0);

select * from Empresa
select * from Segmento
select * from SegmentoClassificacao
select * from SetorEconomico
select * from Subsetor