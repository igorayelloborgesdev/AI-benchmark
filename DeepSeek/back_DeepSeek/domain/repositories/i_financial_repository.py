from abc import ABC, abstractmethod
from typing import List
from typing import Optional
from datetime import date

class IFinancialRepository(ABC):

    @abstractmethod
    def create_cdis(self, cdis: List[any]) -> int:
        pass

    @abstractmethod
    def get_cdis_by_date_range(
        self,
        data_inicial: Optional[date] = None,
        data_final: Optional[date] = None
    ):
        pass

    @abstractmethod
    def save_historical_data(self, data: List[any]) -> int:
        pass

    @abstractmethod
    def get_historical_data(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None     
    ):
        pass