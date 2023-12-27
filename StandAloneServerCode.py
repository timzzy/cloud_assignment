import boto3
import base64

ec2 = boto3.resource('ec2',region_name='us-east-1')

# Bash to install MySQL and Sakila DB
bash_script = """#!/bin/bash
sudo apt-get update -y
sudo apt-get install mysql-server -y
# downloading SakilaDB
sudo wget https://downloads.mysql.com/docs/sakila-db.tar.gz
sudo tar -xvzf sakila-db.tar.gz
# importing SakilaDB
sudo mysql -u root < sakila-db/sakila-schema.sql
sudo mysql -u root < sakila-db/sakila-data.sql
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
print(instance[0].id, "\t", instance[0].private_dns_name)