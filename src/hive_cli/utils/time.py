import datetime

def humanize_time(timestamp: str) -> str:
    if timestamp:
        creation_time = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        t = datetime.datetime.now() - creation_time
        if t.days > 0:
            age = f"{t.days}d"
        elif t.seconds >= 3600:
            age = f"{t.seconds // 3600}h"
        elif t.seconds >= 60:
            age = f"{t.seconds // 60}m"
        else:
            age = f"{t.seconds}s"
    else:
        age = None

    return age