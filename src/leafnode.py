from typing import override

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str | None] | None = None
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        return f"<{self.tag}>{self.value}</{self.tag}>"
