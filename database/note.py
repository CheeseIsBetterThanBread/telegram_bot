from database.constants import ID_COUNTER, SEPARATOR, WHITESPACES


def cut_head(text: str) -> str:
    index: int = 0
    while index < len(text) and text[index] in WHITESPACES:
        index += 1

    if index == len(text):
        return ""
    return text[index:]


def cut_tail(text: str) -> str:
    index: int = len(text) - 1
    while index >= 0 and text[index] in (WHITESPACES + ['.']):
        index -= 1

    if index < 0:
        return ""
    return text[:index + 1]


def cut(text: str) -> str:
    return cut_head(cut_tail(text))


class Note:
    text: str
    title: str
    note_id: str

    def __init__(self, data: str) -> None:
        if not len(data) or data.count(' ') == len(data):
            raise ValueError

        global ID_COUNTER
        self.note_id = f"note_{ID_COUNTER}"
        ID_COUNTER += 1

        global SEPARATOR
        index: int = data.find(SEPARATOR)

        if index == -1:
            self.text = data
            self.title = "Untitled"
        else:
            self.text = data[index + len(SEPARATOR + ' '):]
            self.title = data[:index]

        self.text = cut(self.text)
        if not len(self.text):
            raise ValueError

        self.title = cut(self.title)
        if not len(self.title):
            self.title = "Untitled"

    def __eq__(self, other) -> bool:
        return self.note_id == other.note_id

    def __lt__(self, other) -> bool:
        if self.title == other.title:
            return self.note_id < other.note_id
        return self.title < other.title

    def __str__(self) -> str:
        answer: str = (
            f"{self.title}  (id: {self.note_id})\n\n"
            f"{self.text}\n"
        )
        return answer

    def to_share(self) -> str:
        answer: str = f"{self.title}.\n\n{self.text}\n"
        return answer
