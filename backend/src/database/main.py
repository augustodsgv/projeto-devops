from minio_handler import Minio_handler

handler = Minio_handler("localhost:9000", "root", "rootroot")
handler.insert(bucket_name="bucket-teste1",file_path="./database_handler.py", object_name="banana.py")
print(handler.list("bucket-teste1"))

handler.get("bucket-teste1", "database_handler.py", "./abluble.py")
handler.remove("bucket-teste1", "database_handler.py")
print(handler.list("bucket-teste1"))