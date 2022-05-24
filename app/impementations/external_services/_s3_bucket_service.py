import typing

from botocore.client import BaseClient


class InvalidUriError(Exception):
    """
    Raises if S3 URI is malformed
    """


class S3ContentsNotFound(Exception):
    """
    Raises if no contents found at a specific `s3_uri`
    """


class S3BucketService:
    def __init__(self, s3_client: BaseClient):
        self.s3_client = s3_client

    def _split_uri(self, s3_uri: str) -> typing.Tuple:
        if not s3_uri.startswith('s3://'):
            raise InvalidUriError(f'URI must start with "s3://": {s3_uri}')
        parts = s3_uri.split('//')
        if len(parts) != 2:
            raise InvalidUriError(f'Should only be "//" in {s3_uri}')
        key = parts[1]
        key_parts = key.split('/')
        bucket = key_parts[0]
        key = '/'.join(key_parts[1:])
        return bucket, key

    def list_subdirectories(self, s3_uri: str) -> typing.List:
        bucket, prefix = self._split_uri(s3_uri)
        response = self.s3_client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
        if 'Contents' not in response:
            raise S3ContentsNotFound(s3_uri)
        if 'CommonPrefixes' in response:
            return [
                p['Prefix'] for p in response['CommonPrefixes']
            ]
        return []

    def list_filenames(self, s3_uri) -> typing.List[typing.Any]:
        bucket, prefix = self._split_uri(s3_uri)
        filenames = []
        next_continuation_token = None

        while True:
            if filenames == []:
                res = self.s3_client.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                )
            else:
                res = self.s3_client.list_objects_v2(
                    Bucket=bucket,
                    Prefix=prefix,
                    ContinuationToken=next_continuation_token,
                )

            filenames += [r['Key'] for r in res['Contents']]
            next_continuation_token = res.get('NextContinuationToken')
            if next_continuation_token is None:
                break

        return filenames
