from unittest import TestCase, main
from app.main import last_day_of_month
from datetime import date


class Test(TestCase):

    def test_last_day_of_month(self):
        self.assertEqual(last_day_of_month(date(2021, 1, 31)),
                         date(2021, 1, 31))

    def test_deposit(self):
        pass


if __name__ == '__main__':
    main()
