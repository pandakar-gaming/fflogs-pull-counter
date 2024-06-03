import argparse
import csv
import logging
import os
import sys
import yaml

from multiprocessing import Manager, Process
from datetime import datetime
from time import sleep

from fflogs import api_connector
from config import fight_config
from domain import summarized_pull

def get_config_settings(fight_abbreviation):
    CONFIG_FILE = "pull_count_config.yml"
    with open(os.path.join(sys.path[0], CONFIG_FILE), 'r') as config:
        settings = yaml.load(config, Loader=yaml.SafeLoader)

        if fight_abbreviation not in settings['supported_fights']:
            logging.error("Error: was expecting one of the following fights.")
            for fight in settings['supported_fights']:
                logging.error(fight)
            sys.exit(1)

        config = fight_config.FightConfig(settings, fight_abbreviation=fight_abbreviation)
        
        return config

def get_report_status(report_hash, config_settings, last_known_report):
    fflogs_report = api_connector.get_fights_in_report(report_hash=report_hash, public_key=config_settings.public_key)

    if fflogs_report is None:
        return last_known_report

    fflogs_report.available_fights = [fight for fight in fflogs_report.available_fights if fight.zoneName == config_settings.zone_name]
    return fflogs_report


def update_pull_counter(current_report, prior_reports, config_settings):
    num_pulls = 0
    for report in prior_reports:
        num_pulls += len(report.available_fights)
    logging.debug(F"Read {num_pulls} prior pulls")

    num_pulls += len(current_report.available_fights)

    if not os.path.isdir(config_settings.total_pulls_file_location):
        os.makedirs(config_settings.total_pulls_file_location)

    file_location = config_settings.total_pulls_file_location + '/pulls_total.txt'
    with open(file_location, 'w') as total_pulls_file:
        total_pulls_file.write(F"Total Pulls: {num_pulls}")

def write_csv_results(current_report, prior_reports, config_settings):
    header_row = [
        "report_url",
        "report_hash",
        "date_of_fight",
        "phase_reached",
        "fight_duration",
        "boss_percentage"
    ]
    fights = []
    for report in prior_reports:
        fights.extend(report.available_fights)

    fights.extend(current_report.available_fights)

    summarized_fights = [summarized_pull.SummarizedPull(fight, config_settings.phase_map) for fight in fights]

    with open(config_settings.expected_csv_results_file, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow(header_row)
        writer.writerows([summarized_fight.as_csv_row() for summarized_fight in summarized_fights])


def process_fights(report_hash, config_settings, prior_reports, continue_looping):
    SLEEP_TIME = 30
    current_report = None
    while continue_looping.value:
        logging.info("Fetched most up-to-date results, sleeping for {} seconds...".format(SLEEP_TIME))
        current_report = get_report_status(report_hash, config_settings, current_report)
        update_pull_counter(current_report, prior_reports, config_settings)
        i = 0
        while i < SLEEP_TIME:
            sleep(1)
            i += 1
            if not continue_looping.value:
                break
    
    write_csv_results(current_report, prior_reports, config_settings)

def get_prior_reports(config_settings):
    prior_reports = []
    for previous_url in config_settings.previous_fight_urls:
        prior_hash = api_connector.get_report_hash_from_url(previous_url)
        report = api_connector.get_fights_in_report(prior_hash, public_key=config_settings.public_key)
        report.available_fights = [fight for fight in report.available_fights if fight.zoneName == config_settings.zone_name]
        prior_reports.append(report)

    return prior_reports

def get_medicated_events(config_settings, fflogs_report):
    fflogs_events = api_connector.get_medicated_usage_for_report(config_settings.public_key, fflogs_report)
    # from here, filter out Selene / Eos / Esteem / ?
    # filter to only friendlies that the report cares about
        # TODO setup friendlies that the report cares about (only those involved in the fight we asked for)
    return fflogs_events

def main():
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    parser = argparse.ArgumentParser(description="Periodically poll a given fflogs log (presumed live logging) " +
                                                "and update pull counts for stream.")
    parser.add_argument("-u", "--url",
                        dest="input_url",
                        help="FFLogs URL that's currently being live logged to",
                        required=True)
    parser.add_argument("-f", "--fight_code",
                        dest="fight_code",
                        help="Fight abbreviation that we want to track counts for",
                        required=True)
    args = parser.parse_args()

    fight_code = args.fight_code
    report_hash = api_connector.get_report_hash_from_url(args.input_url)
    config_settings = get_config_settings(fight_code)

    logging.info("Reading prior reports...")
    prior_reports = get_prior_reports(config_settings)

    num_pulls = 0
    for report in prior_reports:
        num_pulls += len(report.available_fights)
    logging.info(F"Read {num_pulls} prior pulls")

    manager = Manager()
    exit_flag = manager.Value('flag', True)
    subprocess = Process(target=process_fights, args=(report_hash, config_settings, prior_reports, exit_flag))
    subprocess.start()
    while exit_flag.value:
        current_time = datetime.now().time().strftime("%H:%M:%S")
        input(F"[{current_time}] Started counting pulls from live log, enter any key to exit...\n")
        exit_flag.value = False
    subprocess.join()

if __name__ == "__main__":
    main()
