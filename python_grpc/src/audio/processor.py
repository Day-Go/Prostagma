import queue

class Processor:
    def __init__(self, recorder, parser):
        self.recorder = recorder
        self.parser = parser
        self.queue = queue.Queue()

    def run(self):
        while True:
            signal = self.queue.get()
            if signal == 'start':
                self.recorder.start()
            elif signal == 'stop':
                self.recorder.stop()
                self.parser.process()
            elif signal == 'quit':
                break
