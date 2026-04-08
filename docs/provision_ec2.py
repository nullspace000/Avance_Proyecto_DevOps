import boto3
ec2 = boto3.resource("ec2")
MAX_INSTANCES = 9
existing = list(ec2.instances.filter(
    Filters=[{"Name": "instance-state-name", "Values": ["pending", "running"]}],
))
remaining = MAX_INSTANCES - len(existing)
if remaining <= 0:
    print("Límite de instancias alcanzado, no se lanzan nuevas instancias.")
else:
    instances = ec2.create_instances(
        ImageId="ami-xxxxxxxx", # Sustituir por AMI válida 
        InstanceType="t3.micro",
        MinCount=1,
        MaxCount=remaining,
        IamInstanceProfile={"Name": "LabInstanceProfile"},
)
print(f"Lanzadas {len(instances)} instancias nuevas.")