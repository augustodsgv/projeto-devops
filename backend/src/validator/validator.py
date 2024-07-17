from abc import ABC, abstractmethod

class Validator(ABC):
    def __init__():
        pass
    
    @abstractmethod
    def compare(original_video : str, recompressed_video : str):
        pass