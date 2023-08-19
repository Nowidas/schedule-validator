from datetime import datetime


def get_working_days_in_month(year, month):
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


def main() -> None:
    filename = "harmonogram.csv"  # Wprowadź nazwę pliku z harmonogramem
    schedule = read_schedule(filename)


if __name__ == "__main__":
    main()
