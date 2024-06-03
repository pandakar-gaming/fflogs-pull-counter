"""
An attempt to expand this a bit and get this to be more object-oriented.
This class is intended for representing what we pull from the YAML config
for the fight.
"""

class FightConfig:

    def __init__(self, yaml_settings, fight_abbreviation):
        # Top level info
        self.public_key = yaml_settings['public_key']
        self.root_pull_location_folder = yaml_settings['pull_location_folder']

        # Information pertaining to the fight
        self.fight_name = yaml_settings[fight_abbreviation]['full_name']
        self.difficulty = yaml_settings[fight_abbreviation]['difficulty']
        self.zone_name = yaml_settings[fight_abbreviation]['zone_name']
        self.boss_id = yaml_settings[fight_abbreviation]['boss_id']
        self.phase_map = {}
        if self.difficulty == "Ultimate":
            self.num_phases = len(yaml_settings[fight_abbreviation]['phases'])
            for phase in yaml_settings[fight_abbreviation]['phases']:

                self.phase_map[phase] = yaml_settings[fight_abbreviation]['phases'][phase]
        else:
            self.num_phases = 1

        # Information pertaining to saving fight results afterwards
        self.expected_save_folder = self.root_pull_location_folder + fight_abbreviation
        self.total_pulls_file_location = self.expected_save_folder
        self.previous_fight_urls = []
        self.read_previous_fight_urls()
        self.expected_csv_results_file = F"{self.root_pull_location_folder}/{fight_abbreviation}/summarized_results.csv"

    def read_previous_fight_urls(self):
        try:
            with open(F"{self.expected_save_folder}/all_logs.txt", 'r') as previous_logs:
                for log in previous_logs.readlines():
                    log = log.strip()
                    self.previous_fight_urls.append(log)
        except IOError:
            pass