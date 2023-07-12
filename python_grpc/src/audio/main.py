import os
import time
from threading import Thread
from recorder import Recorder
from listener import Listener
from audio_parser import AudioParser
from watchdog.observers import Observer

def watch_directory(path, listener):
    event_handler = AudioParser()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while listener.is_running: 
            time.sleep(0.01)
    finally: 
        observer.stop() 

    observer.join()  


r = Recorder("mic.wav")
l = Listener(r)
print('hold ctrl to record, press q to quit')
dirname = os.path.dirname(__file__)

watchdog_thread = Thread(target=watch_directory, args=(os.path.join(dirname, 'recordings/'), l))
watchdog_thread.start()

l.start_keyboard_listener() 

while l.is_running: 
    time.sleep(0.01)
