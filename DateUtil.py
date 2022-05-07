from datetime import datetime

def getCurrentDateString() -> str :
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    return dt_string
    