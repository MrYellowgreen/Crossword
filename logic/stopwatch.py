import time


class Stopwatch:
    def __init__(self, message='', print_out=True):
        self._message = message
        self._print_out = print_out

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, ecx_value, traceback):
        if self._print_out:
            print('{}{:.3f} sec'.format(self._message,
                  time.time() - self.start))
