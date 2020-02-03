For deploying this project on AWS, the following services were configured:

- IAM (Users and Roles)
- S3
- EC2
- CodeDeploy
- Travis

### IAM
Create a Policy for the EC2 role with the permissions below. This allows the EC2 to get data from S3.

```{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:Get*",
                "s3:List*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}```

Create 2 Policies for Travis, one to upload to S3 and the other to send a command to CodeDeploy.

Travis and S3:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```

Travis and CodeDeploy. 
Replace SERVER_REGION, ACCOUNT_ID and CODEDEPLOY_APPLICATION_NAME with the AWS EC2 Region (i.e: us-east-1), your AWS Account id (found in the IAM main panel) and the application name.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "codedeploy:RegisterApplicationRevision",
                "codedeploy:GetApplicationRevision"
            ],
            "Resource": [
                "arn:aws:codedeploy:<SERVER_REGION>:<ACCOUNT_ID>:application:<CODEDEPLOY_APPLICATION_NAME>"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "codedeploy:CreateDeployment",
                "codedeploy:GetDeployment"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "codedeploy:GetDeploymentConfig"
            ],
            "Resource": [
                "arn:aws:codedeploy:<SERVER_REGION>:<ACCOUNT_ID>:deploymentconfig:CodeDeployDefault.OneAtATime",
                "arn:aws:codedeploy:<SERVER_REGION>:<ACCOUNT_ID>:deploymentconfig:CodeDeployDefault.HalfAtATime",
                "arn:aws:codedeploy:<SERVER_REGION>:<ACCOUNT_ID>:deploymentconfig:CodeDeployDefault.AllAtOnce"
            ]
        }Travis
    ]
}
```

Create the Travis IAM User. Grant it programmatic access. Download and save the credentials for this User. Add the two policies created for Travis. Attach the AWSCodeDeployFullAccess policy.

Create a new Role for the EC2 instance and attach the policy created for the EC2 previously. Choose service as AWS Service > EC2.

Finally, create a Role for CodeDeploy and attach the Predefined policy AWSCodeDeployRole. Choose service as AWS Service > CodeDeploy.

### EC2

Create a new EC2 instance, take note of the region, we will reference it as <EC2_INSTANCE_REGION> later. Attach the Role created in the previous step.
Add a Tag to the EC2 instance. Key and value are free to choose. Example: "app" and "myapplicationname-ec2".

### S3

Create an S3 Bucket. Take note of the name and select the same region as the EC2 instance. We will reference them as S3_BUCKET_NAME and S3_BUCKET_REGION later in this tutorial.

### CodeDeploy

Verify that the CodeDeploy agent is running by connecting to the EC2 and executing

```$ sudo service codedeploy-agent statu```

If you get an error, run

```$ sudo service codedeploy-agent star```

In case it is not installed, do as following:

sudo apt-get update
sudo apt-get install ruby
sudo apt-get install wget
cd /home/ubuntu
wget https://<BUCKET_NAME>.s3.<REGION_IDENTIFIER>.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto

BUCKET_NAME is in the form of ```aws-codedeploy-us-east-2```
So, https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install, is a valid S3 URL


Create a new CodeDeploy application. In Name use the same name chosen in the Travis policy (CODEDEPLOY_APPLICATION_NAME). Platform is EC2/On-premises.

Create a DeploymentGroup for the application. Take note of the name, we will reference it as CODEDEPLOY_DEPLOYMENT_GROUP_NAME in the Travis configuration. Set the Role created for CodeDeploy. Set the KEY-VALUE just as the EC2 tag created previously. Default configuration is CodeDeployDefault.AllAtOnce.

### Travis

Now we need to add the Travis' deployment providers. One provider for S3 and another one for CodeDeploy, just like the policies created earlier for Travis.

Add the in the `deploy` object.

deploy:
  - provider: s3
    access_key_id: $AWS_ACCESS_KEY
    secret_access_key: $AWS_SECRET_KEY
    local_dir: dpl_cd_upload
    skip_cleanup: true
    bucket: <S3_BUCKET_NAME>
    region: <S3_BUCKET_REGION>
  - provider: codedeploy
    access_key_id: $AWS_ACCESS_KEY
    secret_access_key: $AWS_SECRET_KEY
    bucket: <S3_BUCKET_NAME>
    key: latest.zip
    bundle_type: zip
    application: <CODEDEPLOY_APPLICATION_NAME>
    deployment_group: <CODEDEPLOY_DEPLOYMENT_GROUP_NAME>
    region: <EC2_INSTANCE_REGION>

AWS_ACCESS_KEY and AWS_SECRET_KEY are downloaded when you create a Travis user. Set these values as Travis environment variables.

### appspec.yml

Now to customize the deployment, we must create in the root folder of our project a file named appspec.yml. It must contain the necessary information to complete the installation and execute the application. Below there is a appspec.yml file example.
```
version: 0.0
os: linux
files:
  - source: ./
    destination: /home/ubuntu/myapp
    runas: ubuntu
hooks:
  AfterInstall:
    - location: scripts/AfterInstall.sh
      timeout: 300
```