from time import sleep
import threading
from _thread import interrupt_main
import sys
from io import StringIO

class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(CustomThread, self).__init__(*args, **kwargs)
        self._stopper = threading.Event()

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()

    def run(self):
        sleep(5)
        while not self.stopped():
            interrupt_main()

def runCode(code, myglobals):
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    oldstderr = sys.stderr
    redirected_output2 = sys.stderr = StringIO()
    result = ""
    thread = CustomThread()
    try:
        thread.start()
        exec(code, myglobals)
        result = redirected_output.getvalue()
    except Exception as e:
        # print(repr(e))
        result = repr(e)
    except SystemExit as s:
        # print(repr(s))
        result = redirected_output2.getvalue()
    except KeyboardInterrupt as k:
        result = "timed out"
    thread.stop()
    myglobals.popitem()
    sys.stdout = old_stdout
    sys.stderr = oldstderr
    # print(result)
    # print("maaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    return result