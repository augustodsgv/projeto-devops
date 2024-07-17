from src.api.api_handler import Api_handler
from src.downloader.bucket_downloader import Bucket_downloader
from src.reencoder.av1_reencoder import Av1_reencoder
from src.reencoder.vp8_reencoder import Vp8_reencoder
from src.reencoder.vp9_reencoder import Vp9_reencoder
from src.reencoder.video_reencoder import Video_reencoder
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()
output_mount_path = ''

class reencode_request(BaseModel):
    video_source : str

@app.post('/reencode')
def reencode_video(request : reencode_request):
    reencoder = create_reencoder()
    downloader = Bucket_downloader()
    handler = Api_handler(reencoder=reencoder, downloader=downloader)
    url = request.video_source
    handler.accept_request(url, output_mount_path)
    return {'Your video was recievied and will be reencoded soon'}

def create_reencoder() -> Video_reencoder: 
    if 'REENCODE_CODEC' in os.environ:
       codec_dst = os.environ['REENCODE_CODEC'] 
    else:
        raise Exception('No reencode codec provided!')
    
    codec_bitrate = None
    codec_crf_range = None
    codec_speed = None

    if 'BIT_RATE' in os.environ:
        codec_bitrate = os.environ['BIT_RATE']
    if 'CRF_RANGE' in os.environ:
        codec_crf_range = os.environ['CRF_RANGE']
    if 'SPEED' in os.environ:
        codec_speed = os.environ['SPEED']

    reencoder = None
    if codec_dst == 'VP8':
        reencoder = Vp8_reencoder(bit_rate=codec_bitrate, crf_range=int(codec_crf_range), speed=codec_speed)
    elif codec_dst == 'VP9':
        reencoder = Vp9_reencoder(bit_rate=codec_bitrate, crf_range=int(codec_crf_range), speed=codec_speed)    
    elif codec_dst == 'AV1':
        reencoder = Av1_reencoder(bit_rate=codec_bitrate, crf_range=int(codec_crf_range), speed=codec_speed)
    else:
        raise Exception(f'Invalid /"{codec_dst}/" Codec!')
    
    return reencoder

if __name__ == '__main__':
    if 'OUTPUT_MOUNT_PATH' in os.environ:
        output_mount_path = os.environ['OUTPUT_MOUNT_PATH']
    else:
        raise Exception('No output mount point indicated!')
    
    if 'REENCODE_CODEC' not in os.environ:
        raise Exception('No reencode codec provided!')
    
    uvicorn.run(app, host='0.0.0.0', port=8080)