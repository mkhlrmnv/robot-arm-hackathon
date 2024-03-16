import unittest
from simulation import RobotArmSimulation

class TestRobotArmSimulation(unittest.TestCase):
    def setUp(self):
        self.robot_arm = RobotArmSimulation(arm_length=44, max_x=176, max_y=88)

    def test_calculate_angles(self):
        # Test when x and y are within valid range
        x, y = 44, 44
        theta1, theta2 = self.robot_arm.calculate_angles(x, y)
        self.assertAlmostEqual(theta1, 0, places=2)
        self.assertAlmostEqual(theta2, 0, places=2)

        # Test when x and y are outside valid range
        x, y = 100, 100
        theta1, theta2 = self.robot_arm.calculate_angles(x, y)
        self.assertAlmostEqual(theta1, 0, places=2)
        self.assertAlmostEqual(theta2, 0, places=2)

    def test_get_real(self):
        # Test when x and y are within valid range
        x, y = 0.5, 0.5
        real_x, real_y = self.robot_arm.get_real(x, y)
        self.assertAlmostEqual(real_x, 0, places=2)
        self.assertAlmostEqual(real_y, 44, places=2)

        # Test when x and y are outside valid range
        x, y = 1.5, 1.5
        real_x, real_y = self.robot_arm.get_real(x, y)
        self.assertAlmostEqual(real_x, 132, places=2)
        self.assertAlmostEqual(real_y, 0, places=2)

if __name__ == '__main__':
    unittest.main()