import unittest
from simulation import RobotArmSimulation
from tracker import HandTracker

class TestRobotArmSimulation(unittest.TestCase):
    def setUp(self):
        self.tracker = HandTracker()
        self.robot_arm = RobotArmSimulation(arm_length=44, max_x=176, max_y=88)

    def testCalculateAngles(self):
        # Test when x and y are within valid range
        x, y = 44, 44
        y0 = 0
        l1, l2 = 44, 44
        theta1, theta2 = self.tracker.calculateAngles(x, y, y0, l1, l2)
        self.assertAlmostEqual(theta1, 0, places=2)
        self.assertAlmostEqual(theta2, 1.5707963267948966, places=2)

        # Test when x and y are outside valid range
        x, y = 32, -42
        theta1, theta2 = self.tracker.calculateAngles(x, y, y0, l1, l2)
        self.assertAlmostEqual(theta1, 0.007554090747718956, places=2)
        self.assertAlmostEqual(theta2, -1.8545473921962716, places=2)

    def testGetReal(self):
        # Test when x and y are within valid range
        x, y = 0.5, 0.5
        max_x = 176
        max_y = 88
        real_x, real_y = self.tracker.getReal(x, y, max_x, max_y)
        self.assertAlmostEqual(real_x, 0, places=2)
        self.assertAlmostEqual(real_y, 44, places=2)

        # Test when x and y are outside valid range
        x, y = 0.75, 0.1
        real_x, real_y = self.tracker.getReal(x, y, max_x, max_y)
        self.assertAlmostEqual(real_x, 44, places=2)
        self.assertAlmostEqual(real_y, 79.2, places=2)

    """ NEEDS TO ME MODIFIED TO BE TESTED
    def testIndexLength(self):
        list = [(0.27, 0.56), (0.30, 0.49), (0.30, 0.43), (0.31, 0.38)]
        list2 = [(0.31, 0.38), (0.34, 0.52)]
        res = self.tracker.dist(list)
        res2 = self.tracker.dist(list2)
        self.assertAlmostEqual(res, 0.187148, places=2)
        self.assertAlmostEqual(res2, 0.143178, places=2)
    """
    

if __name__ == '__main__':
    unittest.main()