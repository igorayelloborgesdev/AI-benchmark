# application/repositories/segmento_classificacao_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from domain.repositories.segmento_classificacao_repository import ISegmentoClassificacaoRepository

class SegmentoClassificacaoRepository(ISegmentoClassificacaoRepository):
    """Implementação do repositório para SegmentoClassificacao."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def inserir_segmento(self, sigla: str, descritivo: str):
        """Insere um novo segmento na tabela SegmentoClassificacao."""        
        query = text("INSERT INTO dbo.SegmentoClassificacao (Sigla, Descritivo) VALUES (:sigla, :descritivo)")
        await self.session.execute(query, {"sigla": sigla, "descritivo": descritivo})
        await self.session.commit()
