from fabrication_manager import Task
from .pump_client import PumpClient
import time

class PumpTask(Task):
    def __init__(self, ip="localhost", port=8888, com_port=6, state=0, speed=0, key=None):
        super(PumpTask, self).__init__(key)

        self.ip = ip
        self.port = port
        self.com_port=com_port
        self.state = state
        self.speed = speed

    def run(self, stop_thread):
        with PumpClient(self.ip, self.port) as pc:
            pc.connect_pump(self.com_port)
            pc.set_pump_speed(self.speed)
            if self.state == 1:
                pc.start_pump()
            else:
                pc.stop_pump()

        time.sleep(3)
        self.is_completed = True

              
class PumpOnTask(Task):
    def __init__(self, ip="localhost", port=8888, com_port=6, state=0, speed=0, key=None):
        super(PumpTask, self).__init__(key)

        self.ip = ip
        self.port = port
        self.com_port=com_port
        self.state = state
        self.speed = speed

    def run(self, stop_thread):
        with PumpClient(self.ip, self.port) as pc:
            pc.connect_pump(self.com_port)
            pc.set_pump_speed(self.speed)
            pc.start_pump()
                
        time.sleep(3)
        self.is_completed = True

class PumpOffTask(Task):
    def __init__(self, ip="localhost", port=8888, com_port=6, state=0, speed=0, key=None):
        super(PumpTask, self).__init__(key)

        self.ip = ip
        self.port = port
        self.com_port=com_port
        self.state = state
        self.speed = speed

    def run(self, stop_thread):
        with PumpClient(self.ip, self.port) as pc:
            pc.connect_pump(self.com_port)
            pc.set_pump_speed(self.speed)
            pc.stop_pump()
                
        time.sleep(3)
        self.is_completed = True

class PumpSpeedTask(Task):
    def __init__(self, ip="localhost", port=8888, com_port=6, state=0, speed=0, key=None):
        super(PumpTask, self).__init__(key)

        self.ip = ip
        self.port = port
        self.com_port=com_port
        self.state = state
        self.speed = speed

    def run(self, stop_thread):
        with PumpClient(self.ip, self.port) as pc:
            pc.connect_pump(self.com_port)
            pc.set_pump_speed(self.speed)
                
        time.sleep(3)
        self.is_completed = True

class PumpBackwardsTask(Task):
    def __init__(self, ip="localhost", port=8888, com_port=6, state=0, speed=0, key=None):
        super(PumpTask, self).__init__(key)

        self.ip = ip
        self.port = port
        self.com_port=com_port
        self.state = state
        self.speed = speed

    def run(self, stop_thread):
        with PumpClient(self.ip, self.port) as pc:
            pc.connect_pump(self.com_port)
            self.speed = -abs(self.speed)
            pc.set_pump_speed(self.speed)
                
        time.sleep(3)
        self.is_completed = True