import unittest

from .. import play
from ..utils import config


class Test(unittest.TestCase):

    def setUp(self):
        # Get config
        play.conf = config.getConfig()

    def test_showBank(self):
        play.currentBank = 10
        self.assertIsNone(play.showBank())

    def test_updateBank(self):
        play.currentBank = 10
        play.updateBank(10)
        self.assertEqual(play.currentBank, 20)

    def test_checkBankStatus(self):
        play.currentBank = 10
        self.assertIsNone(play.checkBankStatus())

    def test_checkBankStatus_2(self):
        play.currentBank = -10
        self.assertRaises(SystemExit, play.checkBankStatus)

    def test_amountToCurrency(self):
        self.assertEqual(play.amountToCurrency(10), '$10.00')

    def test_getMaxPossibleBet(self):
        play.currentBank = 10
        self.assertEqual(play.getMaxPossibleBet(10000), 10)
        play.currentBank = 999999
        self.assertEqual(play.getMaxPossibleBet(10000), 10000)

    def test_wheel(self):
        from ..vars.numbers import french
        from ..vars.bets import addColors

        play.withColors = addColors(french)
        self.assertIsInstance(play.wheel(), list)
