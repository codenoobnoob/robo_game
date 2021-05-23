import unittest
from gamemodules import controls
import pygame


class ControlsTestCase(unittest.TestCase):

    def test_get_vector(self):
        control = controls.Controls(5)
