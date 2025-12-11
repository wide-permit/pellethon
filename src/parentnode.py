from typing import override

from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str | None] | None = None,
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("missing tag attribute")

        if self.children is None:
            raise ValueError("missing children attribute")

        html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html
