USE ChatGPTDB

delete from SegmentoClassificacao
DBCC CHECKIDENT ('SegmentoClassificacao', RESEED, 0);
select * from SegmentoClassificacao