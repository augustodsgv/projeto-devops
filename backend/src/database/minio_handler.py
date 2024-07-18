from src.database.database_handler import Database_handler
from minio import Minio
import os

class Minio_handler(Database_handler):
    def __init__(self, minio_url : str, minio_usr : str, minio_passwd : str):
        self.client = Minio(minio_url,
                            access_key=minio_usr,
                            secret_key=minio_passwd,
                            secure=False        # "Insecure" to allow CORS 
                            )
        


    def list(self, bucket_name : str):
        if not self.client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"No such bucket \"{bucket_name}\"")
        
        return [obj.object_name for obj in self.client.list_objects(bucket_name)]
        
    
    def insert(self, bucket_name : str, file_path : str, object_name : str = None):
        print(file_path)
        print(os.listdir("/home/tmp/"))
        # Checking existence of the bucket
        if not self.client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"No such bucket \"{bucket_name}\"")
        
        # Checking existence of the file
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'No such file \"{file_path}\"')
        
        if object_name == None:
            ...
            # object_name = file_path.split('/')[-1]      # If no object name was provided, using the file name
        result = self.client.fput_object(bucket_name, file_path=file_path, object_name=object_name)
        print(result)
  

    def get(self, bucket_name : str, object_name : str, download_path : str):
        if not self.client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"No such bucket \"{bucket_name}\"")
        if not object_name in self.list(bucket_name=bucket_name):
            raise FileNotFoundError(f"No such object \"{object_name}\" inside bucket \"{bucket_name}\"")
        
        self.client.fget_object(bucket_name=bucket_name, object_name=object_name, file_path=download_path)

    def remove(self, bucket_name : str, object_name : str):
        if not self.client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"No such bucket \"{bucket_name}\"")
        if not object_name in self.list(bucket_name=bucket_name):
            raise FileNotFoundError(f"No such object \"{object_name}\" inside bucket \"{bucket_name}\"")
        
        self.client.remove_object(bucket_name=bucket_name, object_name=object_name)
    