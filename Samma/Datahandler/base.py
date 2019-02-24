
from abc import ABC

class DataHandler(ABC):

    @abstractmethod
    def update_bars(self):
        raise NotImplementedError("Implement update_bars()!!")
    @abstractmethod
    def get_latest_bar(self, symbol):
        raise NotImplementedError("Implement get_latest_bar()!!")
