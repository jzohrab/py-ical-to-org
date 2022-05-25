import unittest
import sys
import os
from datetime import datetime
from dateutil.parser import parse

sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from utils import org_scheduled_dates

class TestUtils_make_org_scheduled_dates(unittest.TestCase):

    def test_start_and_end_on_same_day(self):
        start = parse('2022-06-02 18:00:00+00:00')
        end = parse('2022-06-02 18:30:00+00:00')
        actual = org_scheduled_dates(start, end, False)
        expected = '<2022-06-02 Thu 11:00-11:30>'
        self.assertEqual(actual, expected)

    def test_start_and_end_on_different_days(self):
        start = parse('2022-06-02 18:00:00+00:00')
        end = parse('2022-06-03 18:30:00+00:00')
        actual = org_scheduled_dates(start, end, False)
        expected = '<2022-06-02 Thu 11:00>-<2022-06-03 Fri 11:30>'
        self.assertEqual(actual, expected)

    def test_full_day_single_day(self):
        # Note the dates don't have a time zone specified,
        # and the end date = start + 1
        start = parse('2022-05-25 00:00:00')
        end = parse('2022-05-26 00:00:00')
        actual = org_scheduled_dates(start, end, True)
        expected = '<2022-05-25 Wed>'
        self.assertEqual(actual, expected)

    def test_full_day_multiple_days(self):
        # Note the dates don't have a time zone specified.
        start = parse('2022-05-25 00:00:00')
        end = parse('2022-05-27 00:00:00')
        actual = org_scheduled_dates(start, end, True)
        expected = '<2022-05-25 Wed>-<2022-05-26 Thu>'
        self.assertEqual(actual, expected)
