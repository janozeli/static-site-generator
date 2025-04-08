class HTMLNode:
    def __init__(self, tag, value, children, props):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return f" {" ".join(
                list(
                    map(
                        lambda x: f'{x[0]}="{x[1]}"', self.props.items()
                    )
                )
            )}"
