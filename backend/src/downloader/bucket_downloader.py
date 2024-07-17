from src.downloader.video_downloader import Video_downloader
from google.cloud import storage
from pathlib import Path

class Bucket_downloader(Video_downloader):        

    # Baixa um vídeo do bucket
    def download_video(self, video_url : str, path_to_download : str = '.')->str:
        storage.Client.create_anonymous_client()
        client = storage.Client.create_anonymous_client()
        '''
        Google cloud url comes in this format: gs://{bucket_name}/{blob_name}"
        
        '''
        bucket_name, video_name = video_url.split('/')[-2], video_url.split('/')[-1]

        bucket = client.bucket(bucket_name)
        blob = bucket.blob(video_name)

        # Criando path, caso não exista
        if path_to_download != '.':
            Path(path_to_download).mkdir(parents=True, exist_ok=True)

        downloaded_video_path = path_to_download + '/' + video_name
        blob.download_to_filename(downloaded_video_path)
        return downloaded_video_path
        

