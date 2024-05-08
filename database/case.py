from database.constants import ID_COUNTER
from database.time_and_date import is_date, is_time, Time


def construct(data: list[str], default: Time) -> (list[str], Time):
    current_time: Time = default
    if not len(data):
        return data, current_time
    if len(data) == 1:
        if not (is_date(data[0]) or is_time(data[0])):
            return data, current_time
        current_time = Time(data[0])
        return data[1:], current_time
    if not (is_date(data[0]) or is_time(data[0])):
        return data, current_time
    if ((is_date(data[0]) and is_time(data[1])) or
            (is_time(data[0]) and is_date(data[1]))):
        current_time = Time(data[0] + " " + data[1])
        return data[2:], current_time
    current_time = Time(data[0])
    return data[1:], current_time


class Case:
    start: Time
    end: Time
    description: str
    case_id: str

    def __init__(self, data: list[str]) -> None:
        now = Time("")
        data, self.start = construct(data, now)
        data, self.end = construct(data, self.start)
        if self.end < self.start:
            raise ValueError

        self.description = "Event!"
        if len(data):
            self.description = data[0]
            for index in range(1, len(data)):
                self.description += f" {data[index]}"

        global ID_COUNTER
        self.case_id = f"identify_{ID_COUNTER}"
        ID_COUNTER += 1

    def __eq__(self, other) -> bool:
        return self.case_id == other.case_id

    def __lt__(self, other) -> bool:
        if self.start == other.start:
            return self.end < other.end
        return self.start < other.start

    def __str__(self) -> str:
        answer: str = (
            f"{self.description}\n"
            f"- starts at: {self.start}\n"
            f"- ends at: {self.end}\n"
            f"- with id: {self.case_id}\n"
        )
        return answer

    def to_share(self) -> str:
        answer: str = (
            f"{self.description}:\n"
            f"- starts at: {self.start}\n"
            f"- ends at: {self.end}\n"
        )
        return answer
