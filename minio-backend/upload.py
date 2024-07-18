from minio import Minio

client = Minio("localhost:9000",
               access_key="root",
               secret_key="rootroot",
               secure=False)

source_file = "arquivo.txt"
bucket_name = "bucket-teste1"
dest_file = "arquivo.txt"

if client.bucket_exists(bucket_name):
    print(f"Bucket {bucket_name} encontrado!")
else:
    client.make_bucket(bucket_name)
    print(f"Bucket {bucket_name} não encontrado. Criando um novo com este nome!")

client.fput_object(bucket_name, dest_file, source_file)

print(f"Arquivo {source_file} criado com sucesso!")
