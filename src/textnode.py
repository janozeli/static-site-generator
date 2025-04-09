from enum import Enum
from typing import Any, Optional


class TextType(Enum):
    BOLD = 0
    NORMAL = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5


class TextNode:
    def __init__(
        self, text: str, text_type: TextType, url: Optional[str] = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
