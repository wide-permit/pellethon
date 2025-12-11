from enum import Enum
from typing import override

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
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


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node, TextNode) or text_node.text_type not in TextType:
        raise Exception("Not a text node or wrong type")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
