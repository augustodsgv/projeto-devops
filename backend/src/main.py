from src.api.api_handler import Api_handler
from src.downloader.bucket_downloader import Bucket_downloader
from src.reencoder.av1_reencoder import Av1_reencoder
from src.reencoder.vp8_reencoder import Vp8_reencoder
from src.reencoder.vp9_reencoder import Vp9_reencoder
from src.reencoder.video_reencoder import Video_reencoder
from src.utils.video_cutter import Video_cutter
from src.database.minio_handler import Minio_handler

import os
from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Annotated
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
output_mount_path = ''

class Download_request(BaseModel):
    video_name : str

class Cut_request(BaseModel):
    video_path : str
    video_begin : int
    video_end : int
    new_name : Optional[str] = None

class Reencode_request(BaseModel):
    video_source : str
@app.post('/list')
def list_videos():
    database = Minio_handler("database:9000", "root", "rootroot")
    return database.list("bucket-teste1")

@app.post('/cut')
def cut_video(request : Cut_request):
    cutter = Video_cutter()
    video_path = request.video_path
    video_begin = request.video_begin
    video_end = request.video_end
    new_name = request.new_name
    
    # Setting the new video object name
    if new_name == None:
        video_name = video_path.split('/')[-1]
    else:
        video_name = new_name
    try:
        cutter.cut(video_path=video_path, video_begin=video_begin, video_end=video_end, output_path=video_name)
        database = Minio_handler("database:9000", "root", "rootroot")
        database.insert("bucket-teste1", video_name)
        return {'Video cortado com sucesso!'}
    except Exception as e:
        return {'Erro ao cortar o vídeo:':f'{str(e)}'}
    finally:
        if os.path.exists(video_name):      # Limpando arquivos temporários
            os.remove(video_name)

@app.post('/download')
def download_video(request : Download_request):
    database : Minio_handler = Minio_handler("database:9000", "root", "rootroot")
    file_name = './'+request.video_name
    try:
        database.get("bucket-teste1", request.video_name, file_name)
        def iterfile():
            with open(file_name, 'rb') as file:
                yield from file
        return StreamingResponse(iterfile(), media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao fazer download do vídeo o vídeo:{str(e)}')
    # TODO: fix this. The finally block does now awaits for the yields functions to run
    # finally:
    #     if os.path.exists(file_name):
    #         os.remove(file_name)

@app.post('/upload')
def upload_video(file : UploadFile = File(...)):
    file_path = f"./{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {"filename" : file.filename}


@app.post('/cut_file')
def cut_video(request : Cut_request):
    cutter = Video_cutter()
    video_path = request.video_path
    video_begin = request.video_begin
    video_end = request.video_end
    new_name = request.new_name
    
    # Setting the new video object name
    if new_name == None:
        video_name = video_path.split('/')[-1]
    else:
        video_name = new_name
    try:
        cutter.cut(video_path=video_path, video_begin=video_begin, video_end=video_end, output_path=video_name)
        database = Minio_handler("database:9000", "root", "rootroot")
        database.insert("bucket-teste1", video_name)
        return {'Video cortado com sucesso!'}
    except Exception as e:
        return {'Erro ao cortar o vídeo:':f'{str(e)}'}
    finally:
        if os.path.exists(video_name):      # Limpando arquivos temporários
            os.remove(video_name)

@app.post('/reencode')
def reencode_video(request : Reencode_request):
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
    
    uvicorn.run(app, host='0.0.0.0', port=7000)