from serial import Serial


class ArduinoComm:

    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.cxn = Serial(port, baudrate=baudrate)

    def approve(self):
        print('Sending approval')
        self._send_msg('a')

    def reject(self):
        self._send_msg('r')

    def _send_msg(self, msg):
        self.cxn.write(msg.encode('utf-8'))
