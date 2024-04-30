def convert_to_number(text: str) -> str:
    answer: str = ""
    for symbol in text:
        if symbol in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            answer += symbol
    answer = answer[-10:]
    if len(answer) != 10:
        raise ValueError

    answer = answer[0: 3] + "-" + answer[3: 6] + "-" + answer[6:]
    return answer


def extract_name(data: list[str]) -> (str, list[str]):
    answer: str = data[0]
    index: int = 1
    while len(data) > index and '@' not in data[index]:
        answer += " " + data[index]
        index += 1
    return answer, data[index:]


id_counter: int = 1


class Contact:
    telephone: str
    name: str
    email: str | None
    contact_id: str

    def __init__(self, data: list[str]) -> None:
        if len(data) < 2:
            raise ValueError

        self.telephone = convert_to_number(data[0])
        self.name, data = extract_name(data[1:])

        global id_counter
        self.contact_id = f"contact_{id_counter}"
        id_counter += 1

        if not len(data) or '@' not in data[0]:
            self.email = None
            return
        if len(data) > 1:
            raise ValueError
        self.email = data[0]

    def __eq__(self, other) -> bool:
        return self.contact_id == other.contact_id

    def __lt__(self, other) -> bool:
        if self.name == other.name:
            return self.contact_id < other.contact_id
        return self.name < other.name

    def __str__(self) -> str:
        current_email: str = ""
        if self.email:
            current_email = f"Email: {self.email}\n"
        answer: str = (
            f"{self.name}\n"
            f"Telephone number: {self.telephone}\n"
            f"{current_email}"
            f"With id: {self.contact_id}\n"
        )
        return answer

    def to_share(self) -> str:
        answer: str = (
            f"{self.name}\n"
            f"Telephone number: {self.telephone}\n"
        )
        if self.email:
            answer += f"Email: {self.email}\n"
        return answer
