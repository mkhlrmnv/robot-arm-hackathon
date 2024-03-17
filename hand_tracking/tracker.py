import mediapipe as mp
import cv2
import numpy as np

class HandTracker:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.5)
        # OpenCV setup
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Arm setupq
        self.arm_length = 150
        self.arm_thickness = 10
        self.arm_color = (0, 255, 0)
        self.arm_center = (self.width // 2, self.height // 2)
        self.angle1 = 0
        self.angle2 = 0

    def dist(self, list):
        res = 0
        for i in range(len(list) - 1):
            res += np.sqrt(np.power(list[i].x - list[i + 1].x, 2) + np.power(list[i].y - list[i + 1].y, 2))
        return res

    def getPalmCoords(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Flip on horizontal
        image = cv2.flip(image, 1)

        # Set flag
        image.flags.writeable = False

        # Detections
        results = self.hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow(":)", image)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                # Assuming you want coordinates of the first landmark
                palm_coords = hand.landmark[0].x, hand.landmark[0].y

                fingerList = [hand.landmark[8], hand.landmark[4]]
                fingerDist = self.dist(fingerList)
                # print(f"finger dist: {fingerDist}")

                indexList = [hand.landmark[5], hand.landmark[6], hand.landmark[7], hand.landmark[8]]
                indexLen = self.dist(indexList)
                # print(f"index len : {indexLen}")

                dists = fingerDist, indexLen

                return [palm_coords, dists]
        return [(0.5, 0), (1, 1)]

    def close(self):
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