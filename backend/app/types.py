from typing import TypedDict, Literal


class InputText(TypedDict):
    Text: str


Language = Literal["english", "french"]
