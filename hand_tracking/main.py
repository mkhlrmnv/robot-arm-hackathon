import serial
import time
from tracker import HandTracker
from simulation import RobotArmSimulation

class CoordinateCalculator:
    def __init__(self):
        pass

if __name__ == "__main__":
    ser = serial.Serial(port='/dev/cu.usbserial-10',  baudrate=115200, timeout=.1)  # Change 'COM3' to the appropriate port
    # time.sleep(2)  # Wait for the serial connection to establish
    calculator = CoordinateCalculator()

    simulation = RobotArmSimulation(arm_length=44, max_x=176, max_y=88)
    tracker = simulation.getTracker()

    while True:
        cords = tracker.getPalmCoords()
        x, y = cords[0]
        realX, realY = simulation.getReal(x, y)

        dist = simulation.calcDis(cords[1][1], cords[1][0])

        ser.write(f"{round(realX)};{round(realY)};{dist}\r".encode())
        print(f"Sent coordinates: {round(realX)}, {round(realY)}, {dist}")
        # time.sleep(1)  # Adjust the delay as needed
        
"""
import serial
import time

arduino = serial.Serial(port='/dev/cu.usbserial-10',  baudrate=115200, timeout=.1)

while True:
    cmd = input("put something: ")
    cmd += '\r'
    arduino.write(cmd.encode())

"""

