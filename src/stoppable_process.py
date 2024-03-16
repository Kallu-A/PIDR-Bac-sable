
import multiprocessing


class StoppableProcess(multiprocessing.Process):
    def __init__(self, target=None, args=()):
        super().__init__()
        self.target = target
        self.args = args

    def run(self):
        self.target()

    def stop(self):
        self.terminate()
