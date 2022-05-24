import typing
from app.impementations.external_services import S3BucketService


class GetFacilityPrintNodeKeys:
    def __init__(self, s3_service: S3BucketService, s3_uri: str):
        self.s3_service = s3_service
        self.s3_uri = s3_uri

    def execute(self):
        result = self.s3_service.list_filenames(self.s3_uri)
        return result
