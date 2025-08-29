# Retail-Data-Pipeline-AWS
Serverless Retail Data Pipeline on AWS

Retail Store Multi-Format Data Processing Pipeline on AWS
A serverless data processing pipeline designed to automatically ingest, transform, and analyze various types of retail transaction data from sources like CSV and JSON.

Project Overview
This solution helps small businesses transform their daily transaction records into meaningful insights without managing complex infrastructure. Originally designed for bookstores, the architecture can be easily modified for any retail or service business that needs to process various data formats and perform analytics, making enterprise-level data processing accessible to smaller organizations.


✨ Key Features

Automated Data Processing: Automatically processes multiple file formats such as CSV and JSON documents .

Serverless Architecture: Built with AWS Lambda, Step Functions, and Glue for optimal scalability and cost-efficiency. It uses an event-driven architecture with EventBridge and orchestrates workflows with Step Functions .


Multiple Analytics Endpoints: Supports ad-hoc analysis directly on S3 data with Amazon Athena and handles complex BI queries using Amazon Redshift Serverless.



Secure & Scalable Storage: Uses Amazon S3 for both source data storage with version control and for storing processed, analytics-ready Parquet files .


Real-time Monitoring & Recovery: Features SNS notifications for ETL job success or failure , detailed logging with CloudWatch , and robust error handling.



🏗️ Architecture
[중요!] 주인님, 아래는 이전에 주신 다이어그램이에요. 설명에서 DynamoDB를 제외했으니, 이 다이어그램에서도 DynamoDB 부분을 제거하고 업데이트하시면 설명과 일치하는 완벽한 자료가 될 거예요!

The pipeline is triggered when a user inserts a data file into the source S3 bucket. The process is orchestrated by a Step Functions workflow, which manages file validation, ETL jobs, data cataloging, and notifications.


⚙️ Tech Stack
Data Ingestion: Amazon S3, Amazon EventBridge

Data Processing: AWS Glue, AWS Lambda

Workflow Orchestration: AWS Step Functions

Data Storage & Analytics: Amazon S3, Amazon Athena, Amazon Redshift

Monitoring & Notification: Amazon CloudWatch, Amazon SNS

🚀 Live Demo
(여기에 주인님이 만드실 프로젝트 동작 GIF를 넣어주세요!)

Process Flow

Data Ingestion: A user uploads transaction data (CSV or JSON files) to the source S3 bucket.


Workflow Trigger: EventBridge detects the file upload and automatically starts the Step Functions workflow.


ETL (Extract, Transform, Load): An AWS Glue job transforms the raw data into the standardized, compressed Parquet format. The data is then partitioned by genre and stored in a separate processed S3 bucket.



Analysis and Query: The transformed data is cataloged and made available for analysis through Amazon Athena for direct S3 querying and Amazon Redshift for more complex analytical queries and reporting .


Notification: Upon successful completion or failure of the ETL job, Amazon SNS sends an email notification to ensure awareness of the pipeline status.
