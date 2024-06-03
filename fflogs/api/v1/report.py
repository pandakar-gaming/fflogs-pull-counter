import datetime
from . import fight

class Report(object):

    def __init__(self, report_hash, report_json) -> None:
        super().__init__()
        self.report_hash = report_hash

        self.start_time = datetime.datetime.fromtimestamp(report_json['start'] / 1e3)
        self.end_time = datetime.datetime.fromtimestamp(report_json['end'] / 1e3)
        self.report_date = self.start_time.strftime("%Y-%m-%d")

        self.available_fights = []

        for json_fight in report_json['fights']:
            deserialized_fight = fight.fromJSON(json_fight, report_hash=report_hash, date_of_encounter=self.report_date)
            self.available_fights.append(deserialized_fight)
