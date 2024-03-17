import mediapipe as mp
import cv2
import numpy as np
"""
Imports all necessary libraries
Mediapipe is Google's ML that is being used to detect hands and fingers
cv2 is library for video capture
numpy is library for all math
"""


class HandTracker:
    """
    Tracks hand's and gives some parameters back depending on the function
    """

    def __init__(self):
        """
        Initializes everything up like:
            - like opening webcamera with cv2
            - initializes Mediapipe class

            :return: returns nothing
        """

        # Initialize MediaPipe Hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5)
        # OpenCV setup
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def dist(self, list):
        """
        Calculates total distance between list of points (x, y)

        :param list: list of hand landmarks => list[landmark]
        :return: returns total distance between all points / landmarks
        """

        # variable for result
        res = 0

        # goes through all list
        for i in range(len(list) - 1):
            # dist between p1 and p2 is sqrt((p1.x - p2.x)^2 + (p1.y - p2.y)^2)
            res += np.sqrt(np.power(list[i].x - list[i + 1].x, 2) + np.power(list[i].y - list[i + 1].y, 2))
        return res

    def getPalmCoords(self):
        """
        Function takes current view from webcamera and returns palm coords and distance between index and thumb fingers

        :return: Returns list[tuple(thumb x, thumb y), tuple(dist between index and thumb, total len of index finger)]
        """

        # reads current view from camera
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # next 3 steps are done cause cv2 and mp processes pictures in different color scales
        # cv2 is using BRG and mp RGB
        
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Flip on horizontal
        image = cv2.flip(image, 1)

        # Set flag
        image.flags.writeable = False

        # Passes pic to mp for detection
        results = self.hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # shows webcamera on the screen
        cv2.imshow(":)", image)

        # if there are any detection
        if results.multi_hand_landmarks:
            
            #for all detection
            for hand in results.multi_hand_landmarks:
                # Max amount of hands to be detected is 1, so we take first detection, because can't be more:)
                
                # Taking palm coords
                palm_coords = hand.landmark[0].x, hand.landmark[0].y

                # takes end of index and thumb fingers and passes it to dist function
                fingerList = [hand.landmark[8], hand.landmark[4]]
                fingerDist = self.dist(fingerList)

                # takes all points of index finger and passes them to dist function
                indexList = [hand.landmark[5], hand.landmark[6], hand.landmark[7], hand.landmark[8]]
                indexLen = self.dist(indexList)
                
                # makes tuple
                dists = fingerDist, indexLen

                #returns list all
                return [palm_coords, dists]
            
        # base case if there wan't any detections
        return [(0.5, 0), (1, 1)]

    def close(self):
        """
        closes webcam and all windows
        """
        self.cap.release()
        cv2.destroyAllWindows()




if __name__ == "__main__":
    hand_tracker = HandTracker()
    while True:
        coords = hand_tracker.getPalmCoords()
        if coords:
            print("Palm coordinates:", coords)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    hand_tracker.close()