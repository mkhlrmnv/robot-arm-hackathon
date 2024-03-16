# from simulation import RobotArmSimulation
from tracker import HandTracker
import serial
import time

ser = serial.Serial('/dev/cu.usbserial-1110', 9600)  # Change 'COM3' to the appropriate port

def send_coordinates_to_arduino(ser):
    x, y = HandTracker.getPalmCoords()
    print(f"x: {x}, y: {y}")
    ser.write(f"{x},{y}\n".encode())
    print(f"Sent coordinates: {x}, {y}")

time.sleep(2)  # Wait for the serial connection to establish
calculator = HandTracker.getPalmCoords()

while True:
    calculator.send_coordinates_to_arduino(ser)
    time.sleep(1)  # Adjust the delay as needed