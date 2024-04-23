from fabrication_manager import Task
from .pump_client import PumpClient
import time

class PumpTask(Task):
    def __init__(self, ip="localhost", port=8888, com_port=4, state=0, speed=0, wait=0, key=None):
        super(PumpTask, self).__init__(key)

        self.ip = ip
        self.port = port
        self.com_port=com_port
        self.state = state
        self.speed = speed
        self.wait = wait

    def run(self, stop_thread):
        print(self.state)
        with PumpClient(self.ip, self.port) as pc:
            pc.connect_pump(self.com_port)
            time.sleep(0.5) # wait until connected

            if self.state != 1:
                pc.stop_pump()
                time.sleep(0.5) # wait for command to finish

            pc.set_pump_speed(self.speed)

            if self.state == 1:
                time.sleep(0.5) # wait for previous cmd to finish
                pc.start_pump()

        if self.wait > 0:
            time.sleep(self.wait) # wait for extrusion
        self.is_completed = True

if __name__ == "__main__":

    pt = PumpTask(state=1, speed=20, wait=1)
    pt.run(False)

    pt = PumpTask(state=1, speed=50, wait=1)
    pt.run(False)

    pt = PumpTask(state=0, speed=20, wait=1)
    pt.run(False)