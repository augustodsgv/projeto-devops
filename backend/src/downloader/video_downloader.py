from abc import ABC, abstractmethod

class Video_downloader(ABC):

    @abstractmethod
    def download_video(self, video_url : str, path_to_download):
        pass