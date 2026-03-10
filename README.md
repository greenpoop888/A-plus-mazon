# homework-series-xinrou-xiao

This is Xinrou's cloud computing project.

  

Tech stack:

1. Python3.11 and FastAPI for backend development

2. React18 adn Semantic UI for frontend development

3. Terraform for infrastruture set up

4. shell scripts for deployment

  

please refer to README.md under each folder to know more.

  ---
 **Please notice that this assignmenet was written under my personal AWS account, my Learner lab account was deactivated by AWS, and after comminucated with professor, he suggested me to develop using my personal AWS account, for your grading purpose, you might need to use personal AWS account since I will create a LabRole in my terraform to simulate lab environment.**

* You need to generate key pair and access key manually to keep going on,
- generate key pair
  1. Go to Ec2 console
  2. Click on Key Pairs under Network & Security in left navigate menu
  3. Check your region is us-east-1 (important)
  4. Click on create key pair
  5. Enter vockey for Name, RSA for key pair type, pem for file format
  6. Create key pair
  7. it should automatically download your pem file, please make sure to store it, my deploy script will ask for it's path

- generate access key
  1. Go to IAM console
  2. Click on Users under Access Management in left navigate menu
  3. Click on Create user
  4. Enter the name you want for this IAM, uncheck "Provide user access to the AWS Management Console", go next
  5. Click on Attach policies directly for Permissions options, then search for AdministratorAccess and check it, go next
  6. Review and Create user
  7. Go back to Users console, click on the user you just created.
  8. Click on Security credential tab
  9. Click on Create Access Key
  10. Check Command Line Interface(CLI) for Use case and create access key.
  11. The access key will be used to configure aws cli, my deploy script will ask for that, so please save the file
  

- To setup all infrastructure and deployement, **please make sure you have your AWS SSH key pem file**:

```bash

cd  scripts

./deploy.sh

```

deploy.sh will first ask you to configure aws credential, then apply terraform resources, upload images to S3, then call deploy_ec2.sh twice to deploy grocery and management site both frontend and backend to EC2, also set up database table and seed data after deploy grocery site.

You will have to input **"aws credential, your RDS dbadmin user password, your AWS SSH key pem file location."** during the scripts.

  ---

* To create Cognito user, you need to run this script, please make sure your aws credential before running this script(aws configure), if you ran deploy.sh before this, you are good to continue:

```bash

cd  scripts

./create_user.sh

```

create_user.sh will ask you to input your email address, and a temporary password, you will need to update this password when you first login to management site.
 * to see the management site, visit `http://<management_ec2_ip>`, you must login first.
* you can visit `http://<management_ec2_ip>:8000/docs` to see API document, notice that all Apis required authentication from Cognito, so users are only allow to use api through management site.


* To run traffic generation script
```bash
cd simulator
pip install -r requirements.txt
python ./traffic_generator.py
```

You will be asked to input:
1. how many request you want to send per second?
2. the minimum quantity per request
3. the maximum quantity per request

* To run restock script
```bash
cd simulator
pip install -r requirements.txt
python ./restock.py
```

You will be asked to input:
1. The quantity to trigger restock?
2. The amount to add to the item that is under your given quantity


For your reference, in my design, even user have delete a scubscription, it won't delete user's accesss to the file they subscribed to, so if user subscribe back, they can still see the reports during their old previous subscription duration.