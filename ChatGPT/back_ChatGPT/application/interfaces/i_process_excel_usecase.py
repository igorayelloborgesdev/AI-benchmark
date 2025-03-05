from fastapi import UploadFile
from abc import ABC, abstractmethod
from typing import List, Tuple

class IProcessExcelUseCase(ABC):
    """Interface para o caso de uso de processamento de Excel."""

    @abstractmethod
    async def execute(self, file: UploadFile) -> List[Tuple[str, str]]:
        """Processa o arquivo Excel e retorna uma lista de tuplas (Sigla, Descritivo)."""
        pass
