from abc import ABC, abstractmethod

class Video_reencoder(ABC):
    @abstractmethod
    def reencode(
        self,
        input_file : str,
        output_file : str = None
        ):
        pass

    @property
    @abstractmethod
    def crf(self):
        pass

    # Makes video reencoding
    @abstractmethod
    def reencode(self, input_file : str, output_file : str = None) -> bool:
        pass
