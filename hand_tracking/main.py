import serial
from simulation import RobotArmSimulation
import cv2

class CoordinateCalculator:
    def __init__(self):
        pass

if __name__ == "__main__":

    try:
        ser = serial.Serial(port='/dev/cu.usbserial-10',  baudrate=115200, timeout=.1)  # Change 'COM3' to the appropriate port
        print("Connected to Arduino")
    except:
        print("Couldn't access Arduino")
        ser = None
    # time.sleep(2)  # Wait for the serial connection to establish
    calculator = CoordinateCalculator()

    simulation = RobotArmSimulation(arm_length=44, max_x=176, max_y=88)
    tracker = simulation.getTracker()

    while True:
        cords = tracker.getPalmCoords()
        x, y = cords[0]
        realX, realY = simulation.getReal(x, y)

        dist = simulation.calcDis(cords[1][1], cords[1][0])

        if ser:
            ser.write(f"{round(realX)};{round(realY)};{dist}\r".encode())
            print(f"Sent coordinates: {round(realX)}, {round(realY)}, {dist}")
        else:
            print(f"Detected coords: {round(realX)}, {round(realY)}, {dist}")

        if cv2.waitKey(10) & 0xFF == ord('q'):  # Press 'q' to quit
            break
    
    tracker.close()

        # time.sleep(1)  # Adjust the delay as needed

