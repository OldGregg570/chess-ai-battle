from src.Board import Board
from unittest import TestCase


class TestInit(TestCase):
    def test_init_no_gui(self):
        self.assertEqual(Board().clock, 0)

    # def test_init_with_gui(self):
    #     self.assertEqual(Board(True).clock, 0)

    def test_tick(self):
        b = Board()
        b.tick()
        self.assertEqual(b.clock, 1)

    def test_current_player(self):
        b = Board()

        self.assertEqual(b.current_player(), 'p1')
        b.tick()
        self.assertEqual(b.current_player(), 'p2')
        b.tick()
        self.assertEqual(b.current_player(), 'p1')