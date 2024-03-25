import unittest
import time
from BreakOut import Paddle, Ball, Brick

class TestBreakoutGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()

        self.paddle = Paddle()
        self.ball = Ball()
        self.brick = Brick(0, 0)

    def test_paddle_movement(self):
        timeout_seconds = 10  # Timeout duration in seconds
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            # Run the paddle movement test here
            initial_x = self.paddle.rect.x
            self.paddle.update()
            if initial_x != self.paddle.rect.x:
                break  # Exit loop if paddle movement detected

        # Add cleanup code to handle timeout
        self.addCleanup(self.handle_timeout)

    def handle_timeout(self):
        # This method will be called if the test times out (no movement detected within 10 seconds)
        self.assertTrue(False, msg='Test timed out without movement')

if __name__ == '__main__':
    unittest.main()
