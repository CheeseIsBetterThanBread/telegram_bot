ID_COUNTER: int = 1

WHITESPACES: list[str] = [' ', '\t', '\n', '\r', '\v']
SEPARATOR: str = "!#"

DAYS_IN_MONTH: list[int] = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MINUTES_IN_MONTH: list[int] = [24 * 60 * days for days in DAYS_IN_MONTH]
MINUTES_USUAL: int = 365 * 24 * 60
MINUTES_LEAP: int = 366 * 24 * 60
BASE_YEAR: int = 2020
