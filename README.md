# homework-series-xinrou-xiao

This is Xinrou's cloud computing project.

  

Tech stack:

1. Python3.11 and FastAPI for backend development

2. React18 adn Semantic UI for frontend development

3. Terraform for infrastruture set up

4. Github actions for CI/CD.

  

please refer to README.md under each folder to know more.

  ---
 **From this assignment, I will change to use deployement script instead of Github action for easier reconstruct.**

  

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

for other resource, you may find from terraform output:

grovery site ip: `<client_ec2_ip>`, you can access `http://<client_ec2_ip>` to see the page

management site ip: `<management_ec2_ip>`, you can access `http://<management_ec2_ip>` to see the page

RDS endpoint: `<rds_endpoint>`

s3 bucket(for product images): `<s3_bucket_id>`

Cognito user pool id(for management site): `<us-east-1_JcCDDv0zc>`

Cognito user pool client id(for management site):`<user_pool_client_id>`

API gateway domain(for POS sytstem): `api_base_url`

Lambda funtion id(for POS sytstem):`<lambda_function_name>`
Cognito pool client id: `<user_pool_client_id>` 
Cognito pool id: `<user_pool_id>`

Just a little tips, I am using Windows while developing, so I used Gitbash to run .sh file, you may consider to execute them with Gitbash too.

To test the POS system, please follow the step:

cd sample_pos_client
pip install -r requirements.txt
python python .\pos_test.py
you should be able to see the result through console with following expected result:

test /inventory and /price with store_id = 1, product_id = 1 & 2, min_amount = 30.
test /deduct with store_id = 1, product_id = 1 & 2, quantity = 1
test /deduct-batch, first case is store_id = 1, product_id = 1 & 2, quantity = 1, second case is store_id = 1, product_id = 3 & 4, quantity = 1(should return error for insufficient stock)
test /inventory for invalid store and product id
test /deduct for Insufficient stock
test /undefined_route for invalid api route

