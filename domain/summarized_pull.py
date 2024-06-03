
class SummarizedPull(object):

    def __init__(self, fflogs_fight, phase_map) -> None:
        self.report_hash = fflogs_fight.report_hash
        self.report_url = F"https://www.fflogs.com/reports/{fflogs_fight.report_hash}"
        self.date_of_encounter = fflogs_fight.date_of_encounter
        self.phase_reached = 1
        if fflogs_fight.lastPhaseForPercentageDisplay is not None:
            self.phase_reached = fflogs_fight.lastPhaseForPercentageDisplay
        if self.phase_reached in phase_map.keys():
            self.phase_reached = phase_map[self.phase_reached]["name"]
        self.fight_duration_s = fflogs_fight.fight_duration_s
        self.boss_percentage = fflogs_fight.bossPercentage

    def as_csv_row(self):
        return [
            self.report_url,
            self.report_hash,
            self.date_of_encounter,
            self.phase_reached,
            self.fight_duration_s,
            self.boss_percentage
        ]