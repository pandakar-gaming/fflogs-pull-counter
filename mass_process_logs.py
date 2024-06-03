import argparse
import csv
import logging

import get_current_pull_count
from domain import summarized_pull

def write_csv_results(prior_reports, config_settings):
    """
    """
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


    summarized_fights = [summarized_pull.SummarizedPull(fight, config_settings.phase_map) for fight in fights]

    with open(config_settings.expected_csv_results_file, 'w', newline='\n', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow(header_row)
        writer.writerows([summarized_fight.as_csv_row() for summarized_fight in summarized_fights])


def main():
    """
    Entrypoint for reprocessing logs in full.
    """
    FORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    parser = argparse.ArgumentParser(description="Periodically poll a given fflogs log (presumed live logging) " +
                                                "and update pull counts for stream.")
    parser.add_argument("-f", "--fight_code",
                        dest="fight_code",
                        help="Fight abbreviation that we want to reprocess counts for",
                        required=True)
    args = parser.parse_args()

    fight_code = args.fight_code
    config_settings = get_current_pull_count.get_config_settings(fight_code)
    logging.info("Reading prior reports...")
    prior_reports = get_current_pull_count.get_prior_reports(config_settings)

    num_pulls = 0
    for report in prior_reports:
        num_pulls += len(report.available_fights)
        # medicated_for_report = get_current_pull_count.get_medicated_events(config_settings, report)
        # for medicated_event in medicated_for_report:
            # print(medicated_event)
    logging.info("Read %d prior pulls", num_pulls)
    write_csv_results(prior_reports=prior_reports, config_settings=config_settings)


if __name__ == "__main__":
    main()