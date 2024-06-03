from .api.v1 import v1_api_connector
from .api.v1 import report

import logging

def get_fights_in_report(report_hash, public_key) -> report.Report:
    return v1_api_connector.get_fights_in_report(report_hash, public_key)

"""
# really basic validator - we need a specific URL here
# Input: a URL to live read logs from
# Output: the hash on the end of the report URL so we can properly hit the API with it
# NOTE: The url specifically needs to be https://www.fflogs.com/reports/{hash}. Otherwise it bad time
"""
def get_report_hash_from_url(url):
    if "https://www.fflogs.com/reports/" not in url:
        logging.error(F"Error: was expecting fflogs.com url. Got following: '{url}'.")
        raise ValueError(F"Error: was expecting fflogs.com url. Got following: '{url}'")
    
    report_hash = url.split("/reports/")
    return report_hash[1]

def get_medicated_usage_for_report(public_key, fflogs_report):
    return v1_api_connector.get_medicated_usage_for_report(public_key, fflogs_report)