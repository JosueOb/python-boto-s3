from ..src.cases import GetFacilityPrintNodeKeys
from .external_services import create_s3_bucket_service


def get_facility_printnode_keys():
    return GetFacilityPrintNodeKeys(
        s3_service=create_s3_bucket_service(),
        s3_uri='s3://secrets/test'  # TODO: get from an ENV VAR
    )
