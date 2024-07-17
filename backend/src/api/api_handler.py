from src.reencoder.video_reencoder import Video_reencoder
from src.downloader.video_downloader import Video_downloader


class Api_handler:
    def __init__(self, reencoder : Video_reencoder, downloader : Video_downloader):
        self.reencoder : Video_reencoder = reencoder
        self.downloader : Video_downloader = downloader

    def accept_request(self, video_url : str, path_to_reencode : str = './tmp'):
        downloaded_video_path = self.downloader.download_video(video_url=video_url, path_to_download=path_to_reencode)
        self.reencoder.reencode(downloaded_video_path)
        