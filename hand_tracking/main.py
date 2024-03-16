import serial
import time
from tracker import HandTracker

class CoordinateCalculator:
    def __init__(self):
        pass

    def send_coordinates_to_arduino(self, ser):
        x, y = HandTracker.getPalmCoords()
        ser.write(f"{x},{y}\n".encode())
        print(f"Sent coordinates: {x}, {y}")

if __name__ == "__main__":
    ser = serial.Serial('/dev/cu.usbserial-110', 9600)  # Change 'COM3' to the appropriate port
    time.sleep(2)  # Wait for the serial connection to establish
    calculator = CoordinateCalculator()

    while True:
        calculator.send_coordinates_to_arduino(ser)
        time.sleep(1)  # Adjust the delay as needed
