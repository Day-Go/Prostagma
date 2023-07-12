import os
import time
from threading import Thread
from recorder import Recorder
from listener import Listener
from audio_parser import AudioParser
from watchdog.observers import Observer

def watch_directory(path):
    event_handler = AudioParser()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

r = Recorder("mic.wav")
l = Listener(r)
print('hold ctrl to record, press q to quit')
dirname = os.path.dirname(__file__)

watchdog_thread = Thread(target=watch_directory, args=(os.path.join(dirname, 'recordings/'),))
watchdog_thread.start()

l.start_keyboard_listener() #keyboard listener is a thread so we start it here
l.join() #wait for the tread to terminate so the program doesn't instantly 