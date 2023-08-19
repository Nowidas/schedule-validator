import unittest
from datetime import datetime

from main import validate_schedule


class TestScheduleValidator(unittest.TestCase):
    def test_regular_month_no_weekends(self):
        month = 8
        year = 2023
        work_start_time = 8

        # Tworzenie testowego harmonogramu (praca po 8 godzin tylko w dni robocze)
        schedule = {
            day: 8 if datetime(year, month, day).weekday() < 5 else 0
            for day in range(1, 32)
        }
        print(schedule)
        validation_results = validate_schedule(schedule, month, year, work_start_time)

        self.assertTrue(validation_results["gt_total_working_hours"])
        self.assertFalse(validation_results["has_weekend_work"])
        self.assertEqual(validation_results["days_overtime"], [])
        self.assertEqual(validation_results["days_with_insufficient_break"], [])

    def test_month_full_weekends(self):
        month = 8
        year = 2023
        work_start_time = 8

        # Tworzenie testowego harmonogramu (praca po 8 godzin cały miesiąc)
        schedule = {day: 8 for day in range(1, 32)}
        overtime_days = [
            (day, 8)
            for day in range(1, 32)
            if datetime(year, month, day).weekday() >= 6
        ]
        print(schedule)
        validation_results = validate_schedule(schedule, month, year, work_start_time)

        self.assertTrue(validation_results["gt_total_working_hours"])
        self.assertTrue(validation_results["has_weekend_work"])
        self.assertEqual(validation_results["days_overtime"], overtime_days)
        self.assertEqual(validation_results["days_with_insufficient_break"], [])

    def test_month_with_insufficient_break(self):
        month = 8
        year = 2023
        work_start_time = 8

        # Tworzenie testowego harmonogramu (jeden dzien z niewystarczającą przerwą)
        schedule = {
            day: 8 if datetime(year, month, day).weekday() < 5 else 0
            for day in range(1, 32)
        }
        schedule[1] = 16

        print(schedule)
        validation_results = validate_schedule(schedule, month, year, work_start_time)

        self.assertTrue(validation_results["gt_total_working_hours"])
        self.assertFalse(validation_results["has_weekend_work"])
        self.assertEqual(validation_results["days_overtime"], [(1, 8)])
        self.assertEqual(validation_results["days_with_insufficient_break"], [1])

    def test_month_with_insufficient_working_hours(self):
        month = 8
        year = 2023
        work_start_time = 8

        # Tworzenie testowego harmonogramu (polowa przepracowanego etatu)
        schedule = {
            day: 4 if datetime(year, month, day).weekday() < 5 else 0
            for day in range(1, 32)
        }

        print(schedule)
        validation_results = validate_schedule(schedule, month, year, work_start_time)

        self.assertFalse(validation_results["gt_total_working_hours"])
        self.assertFalse(validation_results["has_weekend_work"])
        self.assertEqual(validation_results["days_overtime"], [])
        self.assertEqual(validation_results["days_with_insufficient_break"], [])


if __name__ == "__main__":
    unittest.main()
