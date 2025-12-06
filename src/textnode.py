from enum import Enum
from typing import override


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    @override
    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, TextNode):
            for key in self.__dict__.keys():
                if self.__dict__[key] != other.__dict__[key]:
                    return False
            return True

        return False

    @override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__['text']}, {self.__dict__['text_type'].value}, {self.__dict__['url']})"
