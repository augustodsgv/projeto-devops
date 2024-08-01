from abc import ABC, abstractmethod

class Database_handler(ABC):
    @abstractmethod
    def list(self, bucket_name : str):
        pass
    
    @abstractmethod
    def insert(self, file_path : str, object_name : str, bucket_name : str):
        pass
    
    # TODO : insert já atualiza, mas é melhor ter uma função separada para isto
    # @abstractmethod
    # def update(self, file_path : str, object_name : str, bucket_name : str):
    #     pass

    @abstractmethod
    def get(self, object_name : str, download_path : str, bucket_name : str):
        pass

    @abstractmethod
    def remove(self, object_name : str, bucket_name : str):
        pass