from textnode import TextNode, TextType


def main():
    node1 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    node2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    node3 = TextNode("This is some anchor text", TextType.IMAGE, "https://www.boot.dev")
    print(node1 == node2)
    print(node1 == node3)
    print(node1)
    print(node3)


main()
