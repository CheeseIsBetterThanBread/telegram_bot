from datetime import datetime

from database.constants import (
    BASE_YEAR,
    DAYS_IN_MONTH,
    MINUTES_IN_MONTH,
    MINUTES_LEAP,
    MINUTES_USUAL
)


def is_date(text: str) -> bool:
    numbers: list[str] = text.split('/')
    if len(numbers) != 3:
        return False
    try:
        day: int = int(numbers[0])
        month: int = int(numbers[1])
        _: int = int(numbers[2])
        if 1 <= month <= 12 and 1 <= day <= DAYS_IN_MONTH[month]:
            return True
        return False
    except ValueError:
        return False


def is_time(text: str) -> bool:
    numbers: list[str] = text.split(':')
    if len(numbers) != 2:
        return False
    try:
        hours: int = int(numbers[0])
        minutes: int = int(numbers[1])
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return True
        return False
    except ValueError:
        return False


def is_leap(year: int) -> bool:
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


def convert(minutes: int) -> (str, str, str, str, str):
    minute_: int = minutes
    year_: int = BASE_YEAR
    while True:
        if (minute_ < MINUTES_USUAL or
                (minute_ < MINUTES_LEAP and is_leap(year_))):
            break
        if is_leap(year_):
            minute_ -= MINUTES_LEAP
        else:
            minute_ -= MINUTES_USUAL
        year_ += 1

    month_: int = 1
    while True:
        if minute_ < MINUTES_IN_MONTH[month_]:
            break
        minute_ -= MINUTES_IN_MONTH[month_]
        month_ += 1

    day_: int = minute_ // (24 * 60) + 1
    minute_ %= 24 * 60
    hour_: int = minute_ // 60
    minute_ %= 60

    minute: str = str(minute_) if minute_ > 9 else f"0{minute_}"
    hour: str = str(hour_) if hour_ > 9 else f"0{hour_}"
    day: str = str(day_) if day_ > 9 else f"0{day_}"
    month: str = str(month_) if month_ > 9 else f"0{month_}"
    year: str = str(year_) if year_ > 9 else f"0{year_}"

    return minute, hour, day, month, year


def extract(minute: int, hour: int, day: int, month: int, year: int) -> int:
    answer: int = minute + 60 * hour + 1440 * (day - 1)

    day = 0
    for index in range(1, month):
        day += DAYS_IN_MONTH[index]
    answer += 1440 * day

    for inbetween in range(BASE_YEAR, year):
        if is_leap(inbetween):
            answer += MINUTES_LEAP
        else:
            answer += MINUTES_USUAL

    return answer


class Time:
    minute: int

    def __init__(self, string: str) -> None:
        now: str = datetime.now().strftime("%H:%M %d/%m/%Y")
        values: list[str] = string.split(' ')
        actual: str = ""
        if not string:
            actual = now
        elif len(values) == 1:
            if is_date(values[0]):
                actual = now.split(' ')[0] + " " + values[0]
            elif is_time(values[0]):
                actual = values[0] + " " + now.split(' ')[1]
        elif len(values) == 2:
            if is_date(values[0]):
                actual = values[1] + " " + values[0]
            else:
                actual = values[0] + " " + values[1]
        values = actual.split(' ')
        hour, minute = map(int, values[0].split(':'))
        day, month, year = map(int, values[1].split('/'))

        self.minute = extract(minute, hour, day, month, year)

    def __str__(self) -> str:
        minute, hour, day, month, year = convert(self.minute)
        return f"{hour}:{minute} {day}/{month}/{year}"

    def __lt__(self, other) -> bool:
        return self.minute < other.minute

    def __eq__(self, other) -> bool:
        return self.minute == other.minute

    def __add__(self, other):
        answer: Time = Time("")
        answer.minute = self.minute + other.minute
        return answer

    def __sub__(self, other):
        answer: Time = Time("")
        answer.minute = self.minute - other.minute
        return answer

    def refactored(self) -> str:
        minute, hour, day, month, year = convert(self.minute)
        return f"{year}-{month}-{day} {hour}:{minute}:00"

    @classmethod
    def delta(cls, shift: int = 1):
        answer: Time = Time("")
        answer.minute = shift
        return answer
