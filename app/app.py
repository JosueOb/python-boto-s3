from . import config

from .dependencies_factory import cases

config.initialize()
use_case = cases.get_facility_printnode_keys()
result = use_case.execute()
