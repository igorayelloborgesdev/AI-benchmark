# application/interfaces/segmento_classificacao_repository.py
from abc import ABC, abstractmethod
from typing import Any

class ISegmentoClassificacaoRepository(ABC):
    """Interface para repositório de SegmentoClassificacao."""

    @abstractmethod
    async def inserir_segmento(self, sigla: str, descritivo: str) -> Any:
        """Insere um novo segmento na tabela SegmentoClassificacao."""
        pass
