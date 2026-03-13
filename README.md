# Serverless Student Performance Analytics System

## Project Overview

This project demonstrates integration between **Python** and **AWS serverless services (Amazon S3, AWS Lambda, DynamoDB, EC2)** to build an automated student performance analytics pipeline.

The pipeline performs:

- Uploading student datasets to Amazon S3  
- Triggering AWS Lambda automatically  
- Processing JSON records using Python  
- Calculating performance category  
- Detecting at-risk students  
- Storing processed records in DynamoDB  
- Running CRUD operations  
- Executing analytical queries  
- Exporting results  

---

## Development Environment

| Component | Details |
|-----------|---------|
| OS | Windows with WSL (Ubuntu) |
| Cloud Environment | AWS EC2 (Ubuntu) |
| Programming Language | Python 3.x |
| AWS SDK | Boto3 |
| Data Processing | Python JSON |
| Database | DynamoDB |

All commands were executed inside the **WSL terminal** or **EC2 instance**.

---

## AWS Services Used

### Amazon S3
Used for storing uploaded student JSON datasets.

### AWS Lambda
Used to:
- Read uploaded files from S3  
- Process records  
- Calculate derived fields  
- Store records in DynamoDB  

### Amazon DynamoDB
Used to store structured student records and support analytical queries.

### Amazon EC2
Used to execute Python scripts in cloud environment.

### IAM (Identity and Access Management)

Used to securely configure AWS permissions.

Two authentication methods were used:

- **IAM User** for WSL using `aws configure`
- **IAM Role** attached to EC2 instance

---

## AWS CLI Configuration

AWS CLI installation is handled using setup commands.

Before running the project, configure AWS credentials for your IAM user.

Run the following command:

```bash
aws configure
```

Enter the required credentials:

```
AWS Access Key ID: <your-access-key>
AWS Secret Access Key: <your-secret-key>
Default region name: <your-region>
Default output format: json
```

Example:

```
AWS Access Key ID: AKIA*************
AWS Secret Access Key: *********************
Default region name: us-east-1
Default output format: json
```

These credentials are securely stored in:

```
~/.aws/credentials
```

### Test the Configuration

To verify that AWS CLI is configured correctly, run:

```bash
aws s3 ls
```

If configured successfully, it will display the list of S3 buckets in your AWS account.

---

## Dataset

Source: Student Performance Dataset (Kaggle)
https://www.kaggle.com/datasets/nabeelqureshitiii/student-performance-dataset/data

---

## project structure

├── config/
|   └── get_d3_dynamodb.py
│
├── document/
|   ├── lambda_configuration.txt
│   └── lambda_function.py
│
├── scripts/
│   ├── table_creation.py
│   ├── upload_file.py
│   ├── crud_operations.py
│   ├── query_operations.py
│   ├── gsi_creation.py
│   ├── gsi_queries.py
│   ├── import.py
│   ├── export.py
│   └── advanced_queries.py
│
├── .gitignore
├── requirements.txt
└── README.md

---

## Running the Project (WSL)

1.Open WSL

2.Install dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install boto3 pandas
```

3.Clone repository

```bash
git clone <repository-url>
cd student_performance_project
```

4.Configure AWS CLI

```bash
aws configure
```

5.Run scripts in sequence

```bash
python -m scripts.table_creation
python -m scripts.upload_file
python -m scripts.crud_operations
python -m scripts.query_operations
python -m scripts.gsi_creation
python -m scripts.gsi_queries
python -m scripts.import
python -m scripts.export
python -m scripts.advanced_queries
```

---

## Assumptions

- AWS Free Tier account is available
- IAM permissions are configured correctly
- AWS CLI is configured
- Internet connectivity is available
- Python dependencies are installed

---

## Author

**R Madhumitha**