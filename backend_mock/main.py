from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class reencode_request(BaseModel):
    video_source : str

@app.post('/reencode')
def reencode(request : reencode_request):
    print(request.model_dump_json())
    return {f'Your video from {request} was recievied and will be reencoded soon'}