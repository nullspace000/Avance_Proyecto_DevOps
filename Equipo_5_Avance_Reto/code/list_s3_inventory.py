import boto3 
#El método list_buckets y el paginador de list_objects_v2 están documentados en la referencia
#oficial de Boto3 y son la forma estándar de listar buckets y objetos a gran escala
s3 = boto3.client("s3")

response = s3.list_buckets()
for bucket in response.get("Buckets", []):
    name = bucket["Name"]
    print(f"Bucket: {name}")
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=name):
        for obj in page.get("Contents", []):
            print(f" - {obj['Key']} ({obj['Size']} bytes)")