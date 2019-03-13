
import threading


def do_work():
    global timer
    # noinspection PyBroadException
    try:
        print('Hello')
    except:
        pass
    timer = threading.Timer(5, do_work)
    timer.start()


if __name__ == "__main__":
    do_work()


