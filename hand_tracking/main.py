import serial
from simulation import RobotArmSimulation
import cv2
"""
Imports libraries
serial <- sending signals through usb port
simulation <- own class for coords calculation
cv2 <- handling webcamera
"""

class CoordinateCalculator:
    """
    Class takes coordinates of the hand detected via camera and sends them to Arduino via usb
    """

    def __init__(self):
        pass

if __name__ == "__main__":
    """
    Main loop: That runs until 'q' is pressed
    Asks tracker class for coordinates -> calcs all properties with simulation class -> sends to Arduino -> AGAIN!
    """

    # tries to connect to arduino
    try:
        ser = serial.Serial(port='/dev/cu.usbserial-10',  baudrate=115200, timeout=.1)  # Change 'COM3' to the appropriate port
        print("Connected to Arduino")
    except:
        print("Couldn't access Arduino")
        ser = None

    # initialize main class
    calculator = CoordinateCalculator()

    # initializes tracer and simulation classes
    simulation = RobotArmSimulation(arm_length=44, max_x=176, max_y=88)
    tracker = simulation.getTracker()

    # while loop until 'q' is pressed
    while True:
        # takes palm coordinates from webcamera and converts them from scaled x and y to usable x and y 
        cords = tracker.getPalmCoords()
        x, y = cords[0]
        realX, realY = simulation.getReal(x, y)

        # calculates distance between fingers
        dist = simulation.calcDis(cords[1][1], cords[1][0])

        # if connected to arduino -> send to arduino
        if ser:
            ser.write(f"{round(realX)};{round(realY)};{dist}\r".encode())
            print(f"Sent coordinates: {round(realX)}, {round(realY)}, {dist}")
        else:
            print(f"Detected coords: {round(realX)}, {round(realY)}, {dist}")

        # Press 'q' to quit
        if cv2.waitKey(10) & 0xFF == ord('q'):  
            break
        
    # closes webcamera
    tracker.close()

