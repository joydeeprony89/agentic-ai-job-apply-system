"""
AWS integration for the application.
"""
import json
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, List, Optional, BinaryIO

from core.config import settings

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

# Initialize Lambda client
lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)


async def upload_to_s3(
    file_content: str,
    object_name: str,
    bucket: str = settings.S3_BUCKET_NAME,
    content_type: str = 'application/json'
) -> bool:
    """
    Upload a file to an S3 bucket.
    
    Args:
        file_content: Content to upload
        object_name: S3 object name
        bucket: Bucket to upload to
        content_type: Content type of the file
        
    Returns:
        True if file was uploaded, else False
    """
    try:
        s3_client.put_object(
            Body=file_content,
            Bucket=bucket,
            Key=object_name,
            ContentType=content_type
        )
        return True
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return False


async def download_from_s3(
    object_name: str,
    bucket: str = settings.S3_BUCKET_NAME
) -> Optional[str]:
    """
    Download a file from an S3 bucket.
    
    Args:
        object_name: S3 object name
        bucket: Bucket to download from
        
    Returns:
        File content as string if successful, else None
    """
    try:
        response = s3_client.get_object(Bucket=bucket, Key=object_name)
        return response['Body'].read().decode('utf-8')
    except ClientError as e:
        print(f"Error downloading from S3: {e}")
        return None


async def store_job_data_in_s3(
    job_data: Dict[str, Any],
    job_id: str
) -> str:
    """
    Store job data in S3.
    
    Args:
        job_data: Job data to store
        job_id: Job ID
        
    Returns:
        S3 object key
    """
    object_key = f"jobs/{job_id}.json"
    await upload_to_s3(
        file_content=json.dumps(job_data),
        object_name=object_key
    )
    return object_key


async def invoke_lambda_crawler(
    keywords: List[str],
    location: str,
    platform: str
) -> Dict[str, Any]:
    """
    Invoke Lambda function to crawl job listings.
    
    Args:
        keywords: Search keywords
        location: Job location
        platform: Platform to crawl (e.g., linkedin, indeed)
        
    Returns:
        Lambda response
    """
    payload = {
        "keywords": keywords,
        "location": location,
        "platform": platform
    }
    
    try:
        response = lambda_client.invoke(
            FunctionName=f"job-crawler-{platform}",
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        return json.loads(response['Payload'].read().decode('utf-8'))
    except ClientError as e:
        print(f"Error invoking Lambda: {e}")
        return {"error": str(e)}