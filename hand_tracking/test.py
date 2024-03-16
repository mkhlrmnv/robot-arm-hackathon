import unittest
from simulation import RobotArmSimulation

class TestRobotArmSimulation(unittest.TestCase):
    def setUp(self):
        self.robot_arm = RobotArmSimulation(arm_length=44, max_x=176, max_y=88)

    def testCalculateAngles(self):
        # Test when x and y are within valid range
        x, y = 44, 44
        theta1, theta2 = self.robot_arm.calculateAngles(x, y)
        self.assertAlmostEqual(theta1, 0, places=2)
        self.assertAlmostEqual(theta2, 1.5707963267948966, places=2)

        # Test when x and y are outside valid range
        x, y = 32, -42
        theta1, theta2 = self.robot_arm.calculateAngles(x, y)
        self.assertAlmostEqual(theta1, 0.007554090747718956, places=2)
        self.assertAlmostEqual(theta2, -1.8545473921962716, places=2)

    def testGetReal(self):
        # Test when x and y are within valid range
        x, y = 0.5, 0.5
        real_x, real_y = self.robot_arm.getReal(x, y)
        self.assertAlmostEqual(real_x, 0, places=2)
        self.assertAlmostEqual(real_y, 44, places=2)

        # Test when x and y are outside valid range
        x, y = 0.75, 0.1
        real_x, real_y = self.robot_arm.getReal(x, y)
        self.assertAlmostEqual(real_x, 44, places=2)
        self.assertAlmostEqual(real_y, 79.2, places=2)

if __name__ == '__main__':
    unittest.main()