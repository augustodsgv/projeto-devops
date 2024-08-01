from src.database.database_handler import Database_handler
from minio import Minio
import os
import logging

class Minio_handler(Database_handler):
    def __init__(self, minio_url : str, minio_usr : str, minio_passwd : str, default_bucket : str | None = None):
        self.client = Minio(minio_url,
                            access_key=minio_usr,
                            secret_key=minio_passwd,
                            secure=False        # "Insecure" to allow CORS 
                            )
        self.default_bucket = default_bucket
        # Creating an default bucket, if it does not exist already
        if self.default_bucket is not None and not self.client.bucket_exists(default_bucket):
            logging.info(f'Creating bucket {default_bucket}')
            self.client.make_bucket(self.default_bucket)


    def list(self, bucket_name : str | None = None)->list:
        if bucket_name is None:
            if self.default_bucket is not None:
                bucket_name = self.default_bucket
            else:
                raise TypeError("Either the provided or the default bucket names should be non None")
        
        if not self.client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"No such bucket \"{bucket_name}\"")
        
        return [obj.object_name for obj in self.client.list_objects(bucket_name)]
        
    
    def insert(self, file_path : str, object_name : str  | None = None, bucket_name : str | None = None):
        if bucket_name is None:
            if self.default_bucket is not None:
                bucket_name = self.default_bucket
            else:
                raise TypeError("Either the provided or the default bucket names should be non None")

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
  

    def get(self, object_name : str, download_path : str, bucket_name : str | None = None)->None:
        if bucket_name is None:
            if self.default_bucket is not None:
                bucket_name = self.default_bucket
            else:
                raise TypeError("Either the provided or the default bucket names should be non None")
        
        if not self.client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"No such bucket \"{bucket_name}\"")
        if not object_name in self.list(bucket_name=bucket_name):
            raise FileNotFoundError(f"No such object \"{object_name}\" inside bucket \"{bucket_name}\"")
        
        self.client.fget_object(bucket_name=bucket_name, object_name=object_name, file_path=download_path)

    def remove(self, object_name : str, bucket_name : str | None = None):
        if bucket_name is None:
            if self.default_bucket is not None:
                bucket_name = self.default_bucket
            else:
                raise TypeError("Either the provided or the default bucket names should be non None")
        
        if not self.client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"No such bucket \"{bucket_name}\"")
        if not object_name in self.list(bucket_name=bucket_name):
            raise FileNotFoundError(f"No such object \"{object_name}\" inside bucket \"{bucket_name}\"")
        
        self.client.remove_object(bucket_name=bucket_name, object_name=object_name)
    