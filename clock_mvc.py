# type q to quit

import time
import threading


class Informer(object):

    """docstring for Informer"""

    def __init__(self):
        super(Informer, self).__init__()
        self.observers = []

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def delete_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()


class Observer(object):

    """docstring for Observer"""

    def __init__(self):
        super(Observer, self).__init__()

    def update(self):
        pass


class WatchModel(Informer):

    """docstring for WatchModel"""

    def __init__(self):
        super(WatchModel, self).__init__()
        self.running = False
        self.tick_time = 0
        self.last_time = 0

        t = threading.Thread(
            target=self.tick_timer, name='TimerThread')
        t.daemon = True
        t.start()

    def notify_observers(self, tick_time):
        for observer in self.observers:
            observer.update(tick_time)

    def tick_timer(self):
        while True:
            time.sleep(0.01)
            if self.running:
                now = time.time()
                self.tick_time += (now - self.last_time)
                self.last_time = now
                self.notify_observers(self.tick_time)

    def start_stop(self):
        self.last_time = time.time()
        self.running = not self.running


class WatchView(Observer):

    """docstring for WatchView"""

    def __init__(self, model):
        super(WatchView, self).__init__()
        model.add_observer(self)

    def update(self, tick_time):
        str_tick_time = "%02d.%02d" % (
            tick_time, (tick_time - int(tick_time)) * 100)
        print str_tick_time


class WatchController(object):

    """docstring for WatchController"""

    def __init__(self):
        super(WatchController, self).__init__()
        model = WatchModel()
        view = WatchView(model)
        view.update(model.tick_time)

        while True:
            std_in = raw_input('input something:')
            if std_in == 'q':
                break
            model.start_stop()

WatchController()
