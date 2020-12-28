import datetime

def format_text(text):
    now = datetime.datetime.now()
    return f"[{now.isoformat()[:10]}][{now.isoformat()[11:19]}] : {text}\n"

class DebugLogger:
    _first_use = True

    

    @staticmethod
    def log(text):
        if DebugLogger._first_use:
            arg = "w"
            DebugLogger._first_use = False
        else:
            arg = "a"
        with open("debub.log", arg) as file:
            file.write(format_text(text))