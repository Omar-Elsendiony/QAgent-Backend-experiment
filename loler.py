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


code = """import unittest
def lol():
    return lol()


class Testing(unittest.TestCase):
    def test_string(self):
        lol()

    def test_boolean(self):
        lol()


if __name__ == "__main__":
    unittest.main()"""


def runCode(code, myglobals):
    oldStdOUT = sys.stdout
    redirectedOutput = sys.stdout = StringIO()
    oldStdERR = sys.stderr
    redirectedOutput2 = sys.stderr = StringIO()
    result = ""
    thread = CustomThread()
    try:
        thread.start()
        exec(code, myglobals)
        result = redirectedOutput.getvalue()
    except Exception as e:
        # print(repr(e))
        result = repr(e)
    except SystemExit as s:
        # print(repr(s))
        result = redirectedOutput2.getvalue()
    except KeyboardInterrupt as k:
        result = "timed out"
    thread.stop()
    myglobals.popitem()
    sys.stdout = oldStdOUT
    sys.stderr = oldStdERR
    # print(result)
    # print("maaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    return result


print(runCode(code, globals()))
