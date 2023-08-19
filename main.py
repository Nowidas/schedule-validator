from datetime import datetime


def get_working_days_in_month(year: int, month: int) -> int:
    num_days = (datetime(year, month + 1, 1) - datetime(year, month, 1)).days
    working_days = sum(
        1 for day in range(1, num_days + 1) if datetime(year, month, day).weekday() < 5
    )
    return working_days


def read_schedule(filename: str) -> dict:
    schedule = {}
    with open(filename, "r") as file:
        for line in file:
            day, hours = line.strip().split("\t")
            schedule[int(day)] = int(hours)
    return schedule


def validate_schedule(
    schedule: dict, month: int, year: int, work_start_time: int
) -> dict:
    total_working_days = get_working_days_in_month(year, month)
    total_working_hours = 8 * total_working_days
    total_hours = sum(schedule.values())

    has_weekend_work = any(
        datetime(year, month, day).weekday() >= 5 and hours
        for day, hours in schedule.items()
    )

    days_overtime = []
    for day, hours in schedule.items():
        if hours > 8 and datetime(year, month, day).weekday() < 6:
            days_overtime.append((day, hours - 8))
        elif hours > 0 and datetime(year, month, day).weekday() == 6:
            days_overtime.append((day, hours))

    days_with_insufficient_break = []
    for day in range(1, len(schedule.keys()) - 2):
        day_diff, hour_diff = divmod(
            work_start_time + schedule[day], 24
        )  # edge-case when work_end_time is on next day
        current_day = datetime(
            year,
            month,
            day + day_diff,
            hour_diff,
        )
        next_day = datetime(year, month, day + 1, work_start_time)
        if (next_day - current_day).total_seconds() < 11 * 3600:  # 11 hours in seconds
            days_with_insufficient_break.append(day)

    return {
        "gt_total_working_hours": total_hours >= total_working_hours,
        "has_weekend_work": has_weekend_work,
        "days_overtime": days_overtime,
        "days_with_insufficient_break": days_with_insufficient_break,
    }


def main() -> None:
    month, year = 8, 2023  # Wprowadź miesiąc harmonogramu
    work_start_time = 8  # Założenie stałej godziny startu pracy przy danyej w treści zadania strukturze danych (dzień_miesiąca, liczba_godzin) alternatywna opcja zmiana struktury danych na (dzien_miesiaca, godzina_startu, godzina_końca)
    filename = "harmonogram.csv"  # Wprowadź nazwę pliku z harmonogramem
    schedule = read_schedule(filename)
    validation_results = validate_schedule(schedule, month, year, work_start_time)
    print(validation_results)


if __name__ == "__main__":
    main()
