import time

class CurrentTime:
    YYYYMMDDHHMMSS = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    YYYYMMDD = time.strftime("%Y%m%d", time.localtime())

    def __init__(self, YYYYMMDDHHMMSS, YYYYMMDD):
        self.YYYYMMDDHHMMSS = YYYYMMDDHHMMSS
        self.YYYYMMDD = YYYYMMDD