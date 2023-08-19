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
