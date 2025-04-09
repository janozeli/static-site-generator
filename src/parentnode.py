from typing import Optional

from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        return f"<{
            self.tag}>{
            ''.join(
                list(
                    map(
                        lambda x: x.to_html(),
                        self.children)))}</{
            self.tag}>"
