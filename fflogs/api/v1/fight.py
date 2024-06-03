UCOB_BOSS_ID = 1039
UWU_BOSS_ID  = 1042

class FFLogsFight(object):

    def __init__(self) -> None:
        super().__init__()
        # from json
        self.id = -1
        self.boss = -1
        self.start_time = -1
        self.end_time = 1
        self.name = ""
        self.zoneID = -1
        self.zoneName = ""
        self.size = -1
        self.difficulty = -1
        self.kill = False
        self.partial = -1
        self.standardComposition = True
        self.hasEcho = False
        self.bossPercentage = 10000
        self.fightPercentage = -1
        self.lastPhaseForPercentageDisplay = 1
        self.maps = []
        # extra helpers
        self.report_hash = ""
        self.fight_duration_s = 0
        self.fight_duration_mins = 0
        self.phase_reached = ""
        self.date_of_encounter = None

    # gives in ms, need diff / 1000 for s then / 60 for m
    def calculate_fight_duration(self):
        self.fight_duration_s = (self.end_time - self.start_time) / 1000
        self.fight_duration_mins = (self.end_time - self.start_time) / 60000

    def __repr__(self) -> str:
        return F"{self.id} - {self.report_hash}"


def fromJSON(json, report_hash = None, date_of_encounter = None) -> FFLogsFight:
    fight = FFLogsFight()
    fight.id = json["id"]
    fight.boss = json["boss"]
    fight.start_time = json["start_time"]
    fight.end_time = json["end_time"]
    fight.name = json["name"]
    fight.zoneID = json["zoneID"]
    fight.zoneName = json["zoneName"]
    if "size" in json.keys():
        fight.size = json["size"]
    if "difficulty" in json.keys():
        fight.difficulty = json["difficulty"]
    if "kill" in json.keys():
        fight.kill = json["kill"]
    if "partial" in json.keys():
        fight.partial = json["partial"]
    if "standardComposition" in json.keys():
        fight.standardComposition = json["standardComposition"]
    if "hasEcho" in json.keys():
        fight.hasEcho = json["hasEcho"]
    if "bossPercentage" in json.keys():
        fight.bossPercentage = json["bossPercentage"] / 100
    if "fightPercentage" in json.keys():
        fight.fightPercentage = json["fightPercentage"]
    if "lastPhaseForPercentageDisplay" in json.keys():
        fight.lastPhaseForPercentageDisplay = json["lastPhaseForPercentageDisplay"]
    if "maps" in json.keys():
        fight.maps = json["maps"]

    fight.report_hash = report_hash
    fight.date_of_encounter = date_of_encounter
    fight.calculate_fight_duration()

    return fight

def fromCSVEntry(row) -> FFLogsFight:
    fight = FFLogsFight()
    fight.id = int(row["fight_num"])
    fight.report_hash = row["report_hash"]
    fight.phase_reached = row["phase_reached"]
    fight.fight_duration_s = row["fight_duration (s)"]
    return fight