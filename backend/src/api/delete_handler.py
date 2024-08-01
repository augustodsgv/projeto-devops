from fastapi import HTTPException

from src.database.database_handler import Database_handler

class Delete_handler:
    def __init__(self, database : Database_handler):
        self.database = database

    def delete(self, file_name)->None:
        # Deleteing the video from database
        if not file_name in self.database.list():
            raise HTTPException(status_code=404, detail=f'Video {file_name} not found!')
        self.database.remove(file_name)
        return {'Your video has been'}
        