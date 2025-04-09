from typing import Dict, List, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str],
        value: Optional[str],
        children: Optional[List["HTMLNode"]],
        props: Optional[Dict[str, str]],
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({
            self.tag}, {
            self.value}, {
            self.children}, {
            self.props})"

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return " "
        return f" {" ".join(
            list(
                map(
                    lambda x: f'{x[0]}="{x[1]}"', self.props.items()
                )
            )
        )}"
