import boto3
import botocore
from ..impementations.external_services import S3BucketService


def create_s3_client() -> botocore.client.BaseClient:
    return boto3.client('s3', config=botocore.config.Config(
        signature_version='s3v4',
        s3={'use_accelerate_endpoint': False},
    ))


def create_s3_bucket_service() -> S3BucketService:
    return S3BucketService(s3_client=create_s3_client())
