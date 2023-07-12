from pynput import keyboard

class Listener(keyboard.Listener):
    def __init__(self, recorder):
        super().__init__(on_press = self.on_press, on_release = self.on_release)
        self.recorder = recorder
    
    def on_press(self, key):
        if key is None: #unknown event
            pass
        elif isinstance(key, keyboard.Key): #special key event
            if key.space:
                self.recorder.start()
        elif isinstance(key, keyboard.KeyCode): #alphanumeric key event
            if key.char == 'q': #press q to quit
                if self.recorder.recording:
                    self.recorder.stop()
                return False #this is how you stop the listener thread
                
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