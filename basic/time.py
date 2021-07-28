from datetime import *

init_time = datetime.now()


def reset_time():
    global init_time
    init_time = datetime.now()


def elasped_time():
    return datetime.now() - init_time


def elasped_sec(x, *args, **kwargs):
    t1 = datetime.now()
    return x(*args, **kwargs), datetime.now() - t1


def get_now(fmt='%Y%m%d_%H%M%S'):
    return datetime.strftime(datetime.now(), fmt)


def str_delta(x: timedelta):
    mm, ss = divmod(x.seconds, 60)
    hh, mm = divmod(mm, 60)
    return f"{hh:02d}:{mm:02d}:{ss:02d}"


class StopWatch:
    def __init__(self):
        self.t1 = datetime.now()

    def __enter__(self):
        self.t1 = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t2 = datetime.now()
        self.td = self.t2 - self.t1

    def elasped(self):
        return self.td


stop_watch = StopWatch()


class TimeJob:
    def __init__(self, name, mt=0, mb=1):
        self.name = name
        self.mt = mt
        self.mb = mb

    def __enter__(self):
        if self.mt > 0:
            for _ in range(self.mt):
                print()
        print(f'[{get_now(fmt="%H:%M:%S")}] [INIT] {self.name}')
        self.t1 = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t2 = datetime.now()
        print(f'[{get_now(fmt="%H:%M:%S")}] [EXIT] {self.name} ($={str_delta(self.t2 - self.t1)})')
        if self.mb > 0:
            for _ in range(self.mb):
                print()
