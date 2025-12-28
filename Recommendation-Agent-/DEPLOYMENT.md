# AWS Deployment Guide for Retail Recommendation Agent

This guide will walk you through deploying the Retail Recommendation Agent Streamlit application on AWS using Elastic Beanstalk.

## Prerequisites

1. AWS Account
2. AWS CLI installed and configured
3. EB CLI (Elastic Beanstalk Command Line Interface) installed
4. Docker (optional, for containerized deployment)

## Deployment Options

We'll cover two deployment options:
1. **AWS Elastic Beanstalk** (Recommended for simplicity)
2. **AWS ECS with Docker** (For containerized deployment)

## Option 1: Deploying with AWS Elastic Beanstalk

### Step 1: Prepare the Application

First, we need to create a few additional files for deployment:

#### 1. Create a requirements.txt file (if not already present)

```bash
pip freeze > requirements.txt
```

#### 2. Create an application.py file (EB entry point)

Create a new file named `application.py`:

```python
import streamlit as st
from app import *

# This is the main entry point for Elastic Beanstalk
if __name__ == "__main__":
    # Run the Streamlit app
    st.run()
```

#### 3. Create a .ebextensions configuration

Create a folder named `.ebextensions` and add a file named `01_setup.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: application.py
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current"
```

### Step 2: Initialize Elastic Beanstalk Application

1. Install the EB CLI if you haven't already:
   ```bash
   pip install awsebcli
   ```

2. Initialize your EB application:
   ```bash
   eb init
   ```
   
   Follow the prompts to:
   - Select your region
   - Choose your application name
   - Select Python as the platform
   - Choose the appropriate Python version (3.9 or later)

### Step 3: Create Environment and Deploy

1. Create an environment and deploy:
   ```bash
   eb create retail-recommendation-env
   ```

2. Deploy updates:
   ```bash
   eb deploy
   ```

3. Open the application:
   ```bash
   eb open
   ```

## Option 2: Containerized Deployment with AWS ECS

### Step 1: Create a Dockerfile

Create a file named `Dockerfile` in the project root:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Build and Push Docker Image

1. Build the Docker image:
   ```bash
   docker build -t retail-recommendation-agent .
   ```

2. Tag and push to Amazon ECR:
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name retail-recommendation-agent
   
   # Tag the image
   docker tag retail-recommendation-agent:latest <your-account-id>.dkr.ecr.<region>.amazonaws.com/retail-recommendation-agent:latest
   
   # Push to ECR
   docker push <your-account-id>.dkr.ecr.<region>.amazonaws.com/retail-recommendation-agent:latest
   ```

### Step 3: Deploy to ECS

1. Create an ECS task definition
2. Create an ECS service
3. Configure load balancer and security groups

## Environment Variables

For both deployment options, you'll need to configure environment variables:

- `PINECONE_API_KEY`: Your Pinecone API key
- Any other API keys required by your application

### Setting Environment Variables in Elastic Beanstalk

```bash
eb setenv PINECONE_API_KEY=your_pinecone_api_key_here
```

### Setting Environment Variables in ECS

Configure environment variables in your task definition or use AWS Systems Manager Parameter Store.

## Data Considerations

The application uses synthetic retail data stored in the `pdf/synthetic_retail_data/` directory. Ensure this data is included in your deployment package.

## Security Considerations

1. Never commit API keys to version control
2. Use IAM roles for EC2 instances or ECS tasks
3. Store sensitive configuration in AWS Systems Manager Parameter Store or AWS Secrets Manager
4. Use HTTPS for production deployments

## Scaling Considerations

1. For Elastic Beanstalk, configure auto-scaling policies
2. For ECS, configure service auto-scaling
3. Consider using Amazon ElastiCache for caching embeddings
4. Use Amazon CloudFront for content delivery if needed

## Monitoring and Logging

1. Enable CloudWatch logging for your application
2. Set up CloudWatch alarms for key metrics
3. Use AWS X-Ray for distributed tracing (if needed)

## Cost Optimization

1. Use Spot Instances for development environments
2. Right-size your instances based on usage patterns
3. Use scheduled scaling to reduce costs during low-traffic periods
4. Consider using AWS Fargate for serverless container deployment

## Troubleshooting

1. Check CloudWatch logs for application errors
2. Verify environment variables are correctly set
3. Ensure the application can access external services (Pinecone API)
4. Check security group configurations for network access

## Updating the Application

1. Make your code changes
2. For Elastic Beanstalk: `eb deploy`
3. For ECS: Build and push a new Docker image, then update the service