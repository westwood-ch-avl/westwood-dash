from pprint import pprint

def isValidEvent(event: dict) -> bool:

    valid = True
    
    if event.get("userId", "null") == "null" or event.get("userId", "null") is None:

        valid = False
    
    elif event.get("startTimestamp", "null") == "null" or event.get("startTimestamp", "null") is None:

        valid = False
    
    elif event.get("stopTimestamp", "null") == "null" or event.get("stopTimestamp", "null") is None:

        valid = False

    else:

        energy = int(event.get("stopValue")) - int(event.get("startValue"))

        if energy < 0:

            valid = False

    if not valid:

        pprint("Invalid event data:")
        pprint(event)

    return valid