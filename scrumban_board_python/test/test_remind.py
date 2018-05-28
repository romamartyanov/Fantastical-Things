import unittest
from dateutil.relativedelta import *

import test as _test
from scrumban_board import remind as _remind


class RemindTest(_test.TestCase):
    def test_get_repeating_remind_relativedelta(self):
        self.assertEqual(_remind.Remind.get_repeating_remind_relativedelta(None), (None, False))
        self.assertEqual(_remind.Remind.get_repeating_remind_relativedelta('years=2'), (relativedelta(years=2), True))

        try:
            self.assertRaises(_remind.Remind.get_repeating_remind_relativedelta('years==2'), ValueError)
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
