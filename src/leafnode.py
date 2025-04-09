from typing import Dict, Optional

from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str],
        value: str,
        props: Optional[Dict[str, str]] = None,
    ) -> None:
        if props is None:
            props = {}
        super().__init__(tag, value, [], props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode precisa ter um valor")

        if self.tag is None:
            return self.value

        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            props_html = self.props_to_html()
            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
