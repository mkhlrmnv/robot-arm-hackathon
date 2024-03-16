import cv2
import numpy as np
from tracker import HandTracker
import math
import matplotlib.pyplot as plt


tracker = HandTracker()

i = 0

list = []

armLength = 44 #cm
maxX = armLength * 4
maxY = armLength * 2
x0 = 0
y0 = 0

def calculateAngles(x, y):
    theta2 = np.arccos((x**2 + y**2 - armLength**2 - armLength**2) / (2 * armLength * armLength))
    theta1 = np.arctan2(y, x) - np.arctan2(armLength * np.sin(theta2), armLength + armLength * np.cos(theta2))
    # print(f"theta1: {theta1}, theta2 {theta2}")
    midY = y0 + armLength * np.sin(theta1)

    print(midY)

    print(theta1, theta2)

    if midY < 0:
        theta2 = -np.arccos((x**2 + y**2 - armLength**2 - armLength**2) / (2 * armLength * armLength))
        theta1 = np.arctan2(y, x) - np.arctan2(armLength * np.sin(theta2), armLength + armLength * np.cos(theta2))

    return theta1, theta2

def getReal(x, y):
    realX = (x * maxX) - (maxX / 2)
    realY = ((1 - y) * maxY)
    return realX, realY

while i < 1000:
    scaledCoords = tracker.get_palm_coords()

    coords = getReal(scaledCoords[0], scaledCoords[1])

    print(coords)

    if coords:
        theta1, theta2 = calculateAngles(coords[0], coords[1])

        x1 = x0 + armLength * np.cos(theta1)
        y1 = y0 + armLength * np.sin(theta1)
        
        x2 = x1 + armLength * np.cos(theta1 + theta2)
        y2 = y1 + armLength * np.sin(theta1 + theta2)

    plt.figure()
    plt.plot([0, x1], [0, y1], 'b-o')  # First link
    plt.plot([x1, x2], [y1, y2], 'r-o')  # Second link
    plt.plot(0, 0, 'ko')  # Base
    plt.axis('equal')
    plt.xlim(-armLength * 2, armLength * 2)
    plt.ylim(0, armLength)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Robot Arm Simulation')
    plt.grid(True)
    plt.show()

    i += 1


i = 0


while i < 1:
    coords = tracker.get_palm_coords()

    i += 1

    if coords:
        print(f"original: {coords}")
        list.append(coords)

        realX = (coords[0] * maxX) - (maxX / 2)
        realY = (coords[1] * maxY)

        realPair = (realX, realY)

        print(f"converted: {realPair}")

    else:
        pair = (0, maxY)
        print(pair)
        # list.append(pair)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

tracker.close()
print(f"max: {max(list)}")
print(f"min: {min(list)}")