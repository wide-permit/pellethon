from __future__ import annotations

from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str | None] | None = None,
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str | None] | None = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        html_str = ""
        if self.props is None:
            return html_str

        for key in self.props.keys():
            html_str += f' {key}="{self.props[key]}" '

        return html_str

    @override
    def __repr__(self):
        rep = f"{self.__class__.__name__}("
        items = list(self.__dict__.items())
        for i in range(len(items) - 1):
            rep += f"{items[i][1]}, "
        rep += f"{items[-1][1]})"

        return rep
