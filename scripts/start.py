from os import name as osname, system
from time import gmtime, strftime, sleep
from datetime import datetime
from subprocess import Popen, PIPE
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def clear():
    unused = system("cls" if osname == "nt" else "clear")

def autorun(message):
    clear()
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), " - ", message)
    print("make autorun", end="\n>>>\n")
    start = datetime.now()
    output = Popen("make autorun --no-print-directory", shell=True, stdout=PIPE).stdout.read()
    delta = datetime.now() - start
    print(output.decode("utf-8"), end="")
    delta = int(delta.total_seconds() * 1000)
    unit = "ms" if delta < 1000 else "s"
    delta = delta if delta < 1000 else delta / 1000
    print("<<< " + str(delta) + unit)

class AutoRunHandler(FileSystemEventHandler):
    def on_modified(self, event):
        autorun(event.event_type + " " + event.src_path)

if __name__ == "__main__":
    autorun("make start")
    event_handler = AutoRunHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
