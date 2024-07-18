from minio import Minio

client = Minio("localhost:9000",
               access_key="root",
               secret_key="rootroot",
               secure=False)

bucket_name = "bucket-teste1"
file_name = "arquivo.txt"
download_file_path = "downloads/arquivo.txt"

# Checking if bucket exists
if not client.bucket_exists(bucket_name):
    raise NameError(f"Couldn't file bucket with name {bucket_name}")
client.fget_object(bucket_name, file_name, download_file_path)