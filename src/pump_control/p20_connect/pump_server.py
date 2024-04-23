import sys
import threading
import struct
import socket
import serial
import time
if sys.version_info[0] == 2:
    import SocketServer as ss
elif sys.version_info[0] == 3:
    import socketserver as ss

from mtecConnectModbus import mtecConnectModbus

MSG_CONNECT = 0
MSG_STATE = 1
MSG_SPEED = 2

class PumpHandler(ss.BaseRequestHandler):
    def handle(self):
        print("Connected to client at {}".format(self.client_address[0]))
        # data = self.request.recv(1024)
        # msg_type, value = struct.unpack_from("ii", data)
        # print("Message of type {} received with value {}".format(msg_type, value))
        # if msg_type in [MSG_CONNECT, MSG_STATE, MSG_SPEED]:
        #     self.server.command(msg_type, value)    

        # def handle(self):
        # print("Connected to client at {}".format(self.client_address[0]))
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            msg_type, value = struct.unpack_from("ii", data)
            print("Message of type {} received with value {}".format(msg_type, value))
            if msg_type in [MSG_CONNECT, MSG_STATE, MSG_SPEED] and value is not None:
                self.server.command(msg_type, value)
                time.sleep(0.1)
        print("Client disconnected")
        self.request.close()   

class PumpController(ss.TCPServer):
    def __init__(self, ip="localhost", port=8888, handler=PumpHandler):
        super(PumpController, self).__init__((ip,port), handler)
        self.name = "PumpController"
        self.pump = mtecConnectModbus('01')
        self.pump_state = 0
        self.pump_speed = 0
        self.pump.settings_keepAlive_active = True
        self.pump.settings_keepAlive_callback = self.updatedValue
        self.func = {
            0: self.set_connect,
            1: self.set_state,
            2: self.set_speed
        }

    def __enter__(cls):
        cls.start()
        print("Entered context: Pump Controller")
        return cls

    def __exit__(cls, typ, val, tb):
        cls.stop()
        print("Exit context: Pump Controller")

    def start(self):
        self.t = threading.Thread(target=self.serve_forever)
        self.t.start()
        print("Pump controller started...")
    
    def stop(self):
        self.shutdown()
        self.server_close()
        self.t.join()

    def command(self, msg_type, value):
        self.func[msg_type](value)

    def set_connect(self, value):
        print("Attempting connection to serial device at COM{}".format(value))
        self.pump.serial_port = "COM{}".format(int(value))
        if hasattr(self.pump, "serial"):
            print("Connection still available")
            return
        try:
            self.pump.connect()
            print("Connection established!")
        except FileNotFoundError:
            print("No device found at COM{}...".format(value))


    def set_state(self, value):
        if value == 0:
            # stop the pump
            self.pump.speed = 0
            self.pump_state = 0
            if hasattr(self.pump.settings_keepAlive_loop, 'cancel') and callable(self.pump.settings_keepAlive_loop.cancel):
                self.pump.settings_keepAlive_loop.cancel()
            # self.pump.settings_keepAlive_active = False
            print("Pump stopped")
        if value == 1:
            # run the pump at the last known speed setting
            # self.pump.settings_keepAlive_active = True
            self.pump_state = 1
            self.pump.speed = int(self.pump_speed)
            print("Pump resumed, running at speed: {} Hz".format(self.pump_speed/100))

    def set_speed(self, value):
        """ value/100 = Hz """
        if value >= -20 and value <= 100:
            self.pump_speed = value
            if self.pump_state == 1:
                self.pump.speed = int(value)
                print("Pump speed set: {} Hz".format(value/100))
            else:
                print("Pump disabled, speed upon (re)start: {} Hz".format(value/100))

    def updatedValue(self, newValue):
        if newValue is not None:
            print(str(newValue/100) + "Hz")


if __name__ == "__main__":
    with PumpController() as pc:
        print("""
                ---------------------------------------              
                ---- PUMP CONTROLLER SERVER WINDOW ----
                ---------------------------------------              
        Ready for client connections and to receive control commands

                ***************************************              
                -- LEAVE WINDOW OPEN TO CONTROL PUMP --
                ***************************************
                  To stop the controller press CTRL+C
        """)
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Closing the controller... Please wait")
            pc.stop()

            
            

