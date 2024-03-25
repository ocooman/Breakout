import unittest
import pygame
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
        initial_x = self.paddle.rect.x
        self.paddle.update()
        self.assertNotEqual(initial_x, self.paddle.rect.x)

    def test_ball_movement(self):
        initial_x = self.ball.rect.x
        initial_y = self.ball.rect.y
        self.ball.update()
        self.assertNotEqual(initial_x, self.ball.rect.x)
        self.assertNotEqual(initial_y, self.ball.rect.y)

    def test_brick_creation(self):
        self.assertEqual(self.brick.rect.x, 0)
        self.assertEqual(self.brick.rect.y, 0)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

