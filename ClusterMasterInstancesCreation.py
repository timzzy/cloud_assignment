import boto3
import base64

ec2 = boto3.resource('ec2',region_name='us-east-1')

# Bash
bash_script = """#!/bin/bash
sudo apt-get update -y
cd ~
wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-8.0/mysql-cluster-community-management-server_8.0.35-1ubuntu20.04_amd64.deb
sudo dpkg -i mysql-cluster-community-management-server_8.0.35-1ubuntu20.04_amd64.deb
sudo mkdir /var/lib/mysql-cluster
"""

# feeding the script to Base64
user_data = base64.b64encode(bash_script.encode("ascii")).decode('ascii')

instance = ec2.create_instances(
    ImageId='ami-06aa3f7caf3a30282',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName="USEast1RSAKeyPairNotPuTTY",
    SecurityGroupIds=[
        'sg-018850844634ee8ba',
    ],
    UserData=user_data
)

for x in instance:
    x.wait_until_running()
# Reload the instance attributes
for x in instance:
    x.reload()
# Printing instance IDs and Host Public DNS
print("\n\tInstance ID\t\tDNS\n")
for x in instance:
    print(x.id, "\t", x.private_dns_name)


# Writing DNS to a file
with open('D:\DevOps Projects\DB EC2 instances\dns_names.txt', 'w') as file:
    for x in instance:
        # Write the instance ID and public DNS to the file
        file.write(f"{x.private_dns_name}\n")