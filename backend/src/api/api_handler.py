from src.reencoder.video_reencoder import Video_reencoder
from src.downloader.video_downloader import Video_downloader
from src.database.database_handler import Database_handler
from src.utils.video_cutter import Video_cutter

class Api_handler:
    def __init__(self, reencoder : Video_reencoder, downloader : Video_downloader, database : Database_handler, cutter : Video_cutter):
        self.reencoder : Video_reencoder = reencoder
        self.downloader : Video_downloader = downloader
        self.database : Database_handler = database
        self.cutter : Video_cutter = cutter

    def reencode_request(self, video_url : str, path_to_reencode : str = './tmp'):
        downloaded_video_path = self.downloader.download_video(video_url=video_url, path_to_download=path_to_reencode)
        self.reencoder.reencode(downloaded_video_path)

    # def cut_request(self, video_url : str, path_to_reencode : str = './tmp'):
    #     downloaded_video_path = self.downloader.download_video(video_url=video_url, path_to_download=path_to_reencode)

    def cut_request(self, video_path : str, video_begin : int, video_end : int):
        video_name = video_path.split('/')[-1]
        self.cutter.cut(video_path=video_path,video_begin=video_begin, video_end=video_end, output_path="./tmp" + video_name)
        self.database.insert("bucket-teste1", "./tmp" + video_name, video_name)
        