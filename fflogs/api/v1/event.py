class FFLogsEvent(object):

    def __init__(self) -> None:
        super().__init__()

        self.timestamp = -1
        self.type = ""
        self.source = FFLogsSource("", "", "", "", "", "")
        self.sourceIsFriendly = False,
        self.target = FFLogsSource("", "", "", "", "", "")
        self.targetIsFriendly = True
        self.ability = FFLogsAbility("", "", "", "")
        self.fight: -1

class FFLogsSource(object):

    def __init__(self, name, id, guid, type, icon, server) -> None:
        self.name = name
        self.id = id
        self.guid = guid
        self.type = type
        self.icon = icon
        self.server = server

class FFLogsAbility(object):

    def __init__(self, name, guid, type, abilityIcon) -> None:
        self.name = name
        self.guid = guid
        self.type = type
        self.abilityIcon = abilityIcon

def abilityFromJSON(child_json):
    if child_json is None:
        return None

    name = ""
    guid = ""
    type = ""
    abilityIcon = ""
    
    child_json_keys = child_json.keys()
    if "name" in child_json_keys:
        name = child_json["name"]
    if "guid" in child_json_keys:
        guid = child_json["guid"]
    if "type" in child_json_keys:
        type = child_json["type"]
    if "abilityIcon" in child_json_keys:
        abilityIcon = child_json["abilityIcon"]

    return FFLogsAbility(name, guid, type, abilityIcon)

def sourceFromJSON(child_json):
    if child_json is None:
        return None
    
    name = ""
    id = ""
    guid = ""
    type = ""
    icon = ""
    server = ""

    child_json_keys = child_json.keys()
    if "name" in child_json_keys:
        name = child_json["name"]
    if "id" in child_json_keys:
        id = child_json["id"]
    if "guid" in child_json_keys:
        guid = child_json["guid"]
    if "type" in child_json_keys:
        type = child_json["type"]
    if "icon" in child_json_keys:
        icon = child_json["icon"]
    if "server" in child_json_keys:
        server = child_json["server"]

    return FFLogsSource(name, id, guid, type, icon, server)

def fromJSON(json):
    if json is None:
        return None
    
    print(json)
    fflogs_event = FFLogsEvent()
    fflogs_event.timestamp = json["timestamp"]
    fflogs_event.type = json["type"]
    if "source" in json.keys():
        fflogs_event.source = sourceFromJSON(json["source"])
    fflogs_event.sourceIsFriendly = json["sourceIsFriendly"]
    if "target" in json.keys():
        fflogs_event.target = sourceFromJSON(json["target"])
    fflogs_event.targetIsFriendly = json["targetIsFriendly"]
    if "ability" in json.keys():
        fflogs_event.ability = abilityFromJSON(json["ability"])
    fflogs_event.fight: json["fight"]

    return fflogs_event
