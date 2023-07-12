from threading import Thread, Lock
from pynput import keyboard
import pyaudio
import wave

class player:
    def __init__(self, wavfile):
        self.wavfile = wavfile
        self.playing = 0 #flag so we don't try to record while the wav file is in use
        self.lock = Lock() #muutex so incrementing and decrementing self.playing is safe
    
    #contents of the run function are processed in another thread so we use the blocking
    # version of pyaudio play file example: http://people.csail.mit.edu/hubert/pyaudio/#play-wave-example
    def run(self):
        with self.lock:
            self.playing += 1
        with wave.open(self.wavfile, 'rb') as wf:
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(8192)
            while data != b'':
                stream.write(data)
                data = wf.readframes(8192)

            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()
        with self.lock:
            self.playing -= 1
        

class recorder:
    def __init__(self, 
                 wavfile, 
                 chunksize=8192, 
                 dataformat=pyaudio.paInt16, 
                 channels=1, 
                 rate=44100):
        self.filename = wavfile
        self.chunksize = chunksize
        self.dataformat = dataformat
        self.channels = channels
        self.rate = rate
        self.recording = False
        self.pa = pyaudio.PyAudio()

    def start(self):
        # we call start and stop from the keyboard listener, so we use the asynchronous 
        # version of pyaudio streaming. The keyboard listener must regain control to 
        # begin listening again for the key release.
        if not self.recording:
            self.wf = wave.open(f'{time.time_ns()}.wav', 'wb')
            self.wf.setnchannels(self.channels)
            self.wf.setsampwidth(self.pa.get_sample_size(self.dataformat))
            self.wf.setframerate(self.rate)
            
            def callback(in_data, frame_count, time_info, status):
                #file write should be able to keep up with audio data stream (about 1378 Kbps)
                self.wf.writeframes(in_data) 
                return (in_data, pyaudio.paContinue)
            
            self.stream = self.pa.open(format = self.dataformat,
                                       channels = self.channels,
                                       rate = self.rate,
                                       input = True,
                                       stream_callback = callback)
            self.stream.start_stream()
            self.recording = True
            print('recording started')
    
    def stop(self):
        if self.recording:         
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            
            self.recording = False
            print('recording finished')

class listener(keyboard.Listener):
    def __init__(self, recorder, player):
        super().__init__(on_press = self.on_press, on_release = self.on_release)
        self.recorder = recorder
        self.player = player
    
    def on_press(self, key):
        if key is None: #unknown event
            pass
        elif isinstance(key, keyboard.Key): #special key event
            if key.space and self.player.playing == 0:
                self.recorder.start()
        elif isinstance(key, keyboard.KeyCode): #alphanumeric key event
            if key.char == 'q': #press q to quit
                if self.recorder.recording:
                    self.recorder.stop()
                return False #this is how you stop the listener thread
            if key.char == 'p' and not self.recorder.recording:
                self.player.start()
                
    def on_release(self, key):
        if key is None: #unknown event
            pass
        elif isinstance(key, keyboard.Key): #special key event
            if key.ctrl:
                self.recorder.stop()
        elif isinstance(key, keyboard.KeyCode): #alphanumeric key event
            pass

    def start_keyboard_listener(self):
        # put your keyboard listener logic here
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

from threading import Thread
from pynput import keyboard

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time

import openai
import os



key = os.environ.get('OPENAI_API_KEY')
openai.api_key = key


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.wav"]

    def on_created(self, event):
        print(f"{event.src_path} has been added")
        
        time.sleep(10)
        audio_file= open(f"{event.src_path}", "rb")


        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcript)

def watch_directory(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.01)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    r = recorder("mic.wav")
    p = player("mic.wav")
    l = listener(r, p)
    print('hold ctrl to record, press p to playback, press q to quit')
    watchdog_thread = Thread(target=watch_directory, args=('F:\\024_prostagma\\prostagma\\blazor_app',))
    watchdog_thread.start()

    l.start_keyboard_listener() #keyboard listener is a thread so we start it here
    l.join() #wait for the tread to terminate so the program doesn't instantly 
    