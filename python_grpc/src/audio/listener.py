from pynput import keyboard

class Listener:
    def __init__(self, recorder):
        self.recorder = recorder
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.is_running = False
    
    def on_press(self, key):
        if key is None:  # unknown event
            pass
        elif isinstance(key, keyboard.Key):  # special key event
            if key == keyboard.Key.ctrl_l:
                self.recorder.start()
        elif isinstance(key, keyboard.KeyCode):  # Alphanumeric key event
            if key.char == 'q':
                self.recorder.stop()
                self.listener.stop()  
                self.is_running = False
                return False 
                
    def on_release(self, key):
        if key is None:  # unknown event
            pass
        elif isinstance(key, keyboard.Key):  # special key event
            if key.ctrl:
                self.recorder.stop()
        elif isinstance(key, keyboard.KeyCode):  # alphanumeric key event
            pass

    def start_keyboard_listener(self):
        self.listener.start()
        self.is_running = True
