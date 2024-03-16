"""import serial
import time
from tracker import HandTracker

class CoordinateCalculator:
    def __init__(self):
        pass

if __name__ == "__main__":
    ser = serial.Serial('/dev/cu.usbserial-110', 9600)  # Change 'COM3' to the appropriate port
    time.sleep(2)  # Wait for the serial connection to establish
    calculator = CoordinateCalculator()

    tracker = HandTracker()

    while True:
        x, y = tracker.getPalmCoords()
        ser.write(f"{x},{y}\n".encode())
        print(f"Sent coordinates: {x}, {y}")
        time.sleep(1)  # Adjust the delay as needed"""
import serial
import time

arduino = serial.Serial(port='/dev/cu.usbserial-110',  baudrate=115200, timeout=.1)

while True:
    cmd = input("put something: ")
    cmd += '\r'
    arduino.write(cmd.encode())

