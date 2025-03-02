from abc import ABC, abstractmethod
from fastapi import UploadFile

class IExcelProcessorUseCase(ABC):
    """Interface para processamento de arquivos Excel."""

    @abstractmethod
    async def processar_dados(self, excel_file: UploadFile):
        """Processa um arquivo Excel e retorna os dados extraídos."""
        pass
