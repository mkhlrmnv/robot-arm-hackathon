import serial
from simulation import RobotArmSimulation
from tracker import HandTracker
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
        self.l1 = 44
        self.l2 = 44
        self.tot_x = (self.l1 + self.l2) * 2
        self.tot_y = self.l1 + self.l2
        self.x0 = 0
        self.y0 = 0
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
    main = CoordinateCalculator()

    # initializes tracer and simulation classes
    # simulation = RobotArmSimulation(arm_length=44, max_x=176, max_y=88)
    tracker = HandTracker()

    # while loop until 'q' is pressed
    while True:
        # takes palm coordinates from webcamera and converts them from scaled x and y to usable x and y 
        cords = tracker.getPalmCoords()
        x, y = cords[0]
        realX, realY = tracker.getReal(x, y, main.tot_x, main.tot_y)


        # calculates distance between fingers
        dist = tracker.calcDis(cords[1][1], cords[1][0])

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

