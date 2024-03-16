import mediapipe as mp
import cv2
import numpy as np

class HandTracker:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
        # OpenCV setup
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Arm setup
        self.arm_length = 150
        self.arm_thickness = 10
        self.arm_color = (0, 255, 0)
        self.arm_center = (self.width // 2, self.height // 2)
        self.angle1 = 0
        self.angle2 = 0

    def get_palm_coords(self):
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

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                # Assuming you want coordinates of the first landmark
                palm_coords = hand.landmark[0].x, hand.landmark[0].y
                return palm_coords
        return None

    def update_arm_angles(self, palm_coords):
        x, y = palm_coords
        x = int(x * self.width)
        y = int(y * self.height)
        dx = x - self.arm_center[0]
        dy = y - self.arm_center[1]
        self.angle1 = np.arctan2(dy, dx)

    def draw_arm(self, image):
        arm_segment1_end = (int(self.arm_center[0] + self.arm_length * np.cos(self.angle1)),
                            int(self.arm_center[1] + self.arm_length * np.sin(self.angle1)))
        arm_segment2_end = (int(arm_segment1_end[0] + self.arm_length * np.cos(self.angle1 + self.angle2)),
                            int(arm_segment1_end[1] + self.arm_length * np.sin(self.angle1 + self.angle2)))
        cv2.line(image, self.arm_center, arm_segment1_end, self.arm_color, self.arm_thickness)
        cv2.line(image, arm_segment1_end, arm_segment2_end, self.arm_color, self.arm_thickness)

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()

# Example usage:
if __name__ == "__main__":
    hand_tracker = HandTracker()
    while True:
        coords = hand_tracker.get_palm_coords()
        if coords:
            print("Palm coordinates:", coords)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    hand_tracker.close()