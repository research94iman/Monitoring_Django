import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import configparser
from django.conf import settings
from apps.dataStoring.utils import JsonToDB

def readConfig(file_path=settings.CONFIG_FILE_PATH):
    print(file_path)
    time.sleep(1)
    config = configparser.ConfigParser()
    config.read(file_path)
    return  config

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.jsonToDB = JsonToDB()
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"New file created: {event.src_path}")
        self.jsonToDB.run(event.src_path)


def folderMonitoring(path):
    # path="D:/logJson"
    print(f"folder monitoring root = {path}")

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            a = 1
            time.sleep(0.1)
    except: #KeyboardInterrupt:
        observer.stop()

    observer.join()


