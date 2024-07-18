from src.api.api_handler import Api_handler
from src.downloader.bucket_downloader import Bucket_downloader
from src.reencoder.av1_reencoder import Av1_reencoder
from src.reencoder.vp8_reencoder import Vp8_reencoder
from src.reencoder.vp9_reencoder import Vp9_reencoder
from src.reencoder.video_reencoder import Video_reencoder
from src.utils.video_cutter import Video_cutter
from src.database.minio_handler import Minio_handler

import os
import time
from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Annotated
import uvicorn

# endpoints
DATABASE_ENDPOINT = os.environ['DATABASE_ENDPOINT']
DATABASE_PORT = os.environ['DATABASE_PORT']
DATABASE_USR = os.environ['DATABASE_USR']
DATABASE_PASSWD = os.environ['DATABASE_PASSWD']
DATABASE_PASSWD = os.environ['DATABASE_PASSWD']
DATABASE_BUCKET_NAME = os.environ['DATABASE_BUCKET_NAME']

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
    video_name : str
    video_begin : int
    video_end : int

class Delete_request(BaseModel):
    video_name : str

@app.get('/list')
def list_videos():
    database = Minio_handler(f"{DATABASE_ENDPOINT}:{DATABASE_PORT}", DATABASE_USR, DATABASE_PASSWD)
    return database.list(DATABASE_BUCKET_NAME)

@app.post('/cut')
async def cut_video(request : Cut_request):
    database = Minio_handler(f"{DATABASE_ENDPOINT}:{DATABASE_PORT}", DATABASE_USR, DATABASE_PASSWD)
    cutter = Video_cutter()
    video_name = request.video_name
    video_begin = request.video_begin
    video_end = request.video_end
    video_path = '/home/tmp/' + video_name
    original_video_path = '/home/tmp/original_' + video_name
    object_name = video_name
    # Baixando o vídeo da database
    database.get(DATABASE_BUCKET_NAME, video_name, original_video_path)

    # try:
    #     database.get(DATABASE_BUCKET_NAME, video_name)
    # except:         # TODO: treat video not found
    #     pass
    
    print('aqui')
    # try:
    
    cutter.cut(video_path=original_video_path, video_begin=video_begin, video_end=video_end, output_path=video_path)
    print('aqui tb')
    database.insert(DATABASE_BUCKET_NAME, video_path, object_name=object_name)
    print('ate aqui')
    
    return {'Video cortado com sucesso!'}
    # except Exception as e:
    #     return HTTPException(status_code=500, detail=f'Não foi possível cortar o vídeo: {str(e)}')
        
    # finally:
    #     if os.path.exists(video_name):      # Limpando arquivos temporários
    #         os.remove(video_name)

@app.post('/download')
def download_video(request : Download_request):
    database : Minio_handler = Minio_handler(f"{DATABASE_ENDPOINT}:{DATABASE_PORT}", DATABASE_USR, DATABASE_PASSWD)
    file_name = './'+request.video_name
    
    try:
        database.get(DATABASE_BUCKET_NAME, request.video_name, file_name)
        def iterfile():
            with open(file_name, 'rb') as file:
                yield from file
        return StreamingResponse(iterfile(), media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao fazer download do vídeo:{str(e)}')
    # TODO: fix this. The finally block does now awaits for the yields functions to run
    # finally:
    #     if os.path.exists(file_name):
    #         os.remove(file_name)

@app.post('/upload')
def upload_video(file : UploadFile = File(...)):
    if not os.path.exists("./tmp"):
        os.mkdir("./tmp")
    file_path = f"./tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    database : Minio_handler = Minio_handler(f"{DATABASE_ENDPOINT}:{DATABASE_PORT}", DATABASE_USR, DATABASE_PASSWD)
    database.insert(DATABASE_BUCKET_NAME, file_path, file.filename)
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
        database = Minio_handler(f"{DATABASE_ENDPOINT}:{DATABASE_PORT}", DATABASE_USR, DATABASE_PASSWD)
        database.insert(DATABASE_BUCKET_NAME, video_name)
        return {'Video cortado com sucesso!'}
    except Exception as e:
        return {'Erro ao cortar o vídeo:':f'{str(e)}'}
    finally:
        if os.path.exists(video_name):      # Limpando arquivos temporários
            os.remove(video_name)

@app.delete('/delete_video')
def delete_video(request : Delete_request):
    database = Minio_handler(DATABASE_ENDPOINT, DATABASE_USR, DATABASE_PASSWD)
    # try:
    database.remove(DATABASE_BUCKET_NAME, request.video_name)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f'Erro ao deletar o vídeo:{str(e)}')
    





if __name__ == '__main__':
    if 'OUTPUT_MOUNT_PATH' in os.environ:
        output_mount_path = os.environ['OUTPUT_MOUNT_PATH']
    else:
        raise Exception('No output mount point indicated!')
    
    if 'REENCODE_CODEC' not in os.environ:
        raise Exception('No reencode codec provided!')
    
    uvicorn.run(app, host='0.0.0.0', port=7000)