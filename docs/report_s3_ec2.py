import boto3
#programar este script con cron o integrarlo en un pipeline de CI/CD para generar reportes periódicos de uso de recursos.

ec2 = boto3.client("ec2")
s3 = boto3.client("s3")

# EC2
instances = ec2.describe_instances()
running = 0
for reservation in instances["Reservations"]:
    for inst in reservation["Instances"]:
        state = inst["State"]["Name"]
        if state in ("running", "pending"):
            running += 1

print(f"Instancias EC2 activas: {running}") 

# S3
buckets = s3.list_buckets().get("Buckets", [])
print(f"Buckets S3: {len(buckets)}")
for b in buckets:
    print(f" - {b['Name']}")