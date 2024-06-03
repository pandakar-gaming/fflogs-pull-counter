from . import report
from . import event

import logging
import requests

def get_fights_in_report(report_hash, public_key) -> report.Report:
    base_url = F"https://www.fflogs.com/v1/report/fights/{report_hash}?api_key={public_key}"
    logging.debug(F"Making request to {base_url}")

    session = requests.Session()
    retry = requests.urllib3.util.retry.Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=20,
        status_forcelist=(500, 502, 504),
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    
    print(base_url)
    response = session.get(base_url)
    if response.status_code != 200:
        logging.error("Bad response when trying to process fight - {}", response.json())

    if response.json() is not None and "start" in response.json().keys() and "end" in response.json().keys() and "fights" in response.json().keys():
        fflogs_report = report.Report(report_hash, response.json())
        return fflogs_report
    
    return None

def get_medicated_usage_for_report(public_key, fflogs_report) -> list:
    medicated_buff_id = 1000049
    return get_specified_event_for_report(public_key, fflogs_report, medicated_buff_id)

def get_specified_event_for_report(public_key, fflogs_report, event_id) -> list:
    initial_start_time = 9999999999999999   # TODO get from fight
    initial_end_time = 0                    # TODO get from fight
    for fight in fflogs_report.available_fights:
        if fight.start_time < initial_start_time:
            initial_start_time = fight.start_time
        if fight.end_time > initial_end_time:
            initial_end_time = fight.end_time
    base_url = F"https://www.fflogs.com/v1/report/events/buffs/{fflogs_report.report_hash}?start={initial_start_time}&end={initial_end_time}&abilityid={event_id}&api_key={public_key}"
    session = requests.Session()
    retry = requests.urllib3.util.retry.Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=20,
        status_forcelist=(500, 502, 504),
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    print(base_url)
    response = session.get(base_url)
    if response.status_code != 200:
        logging.error("Bad response when trying to process fight - {}", response.json())

    fflogs_events = []
    if response.json() is not None:
        # print(response.json())
        response_json = response.json()

        if not "events" in response_json.keys():
            return fflogs_events

        for json_event in response_json["events"]:
            fflogs_event = event.fromJSON(json_event)
            if fflogs_event is not None:
                fflogs_events.append(fflogs_event)
    
    return fflogs_events