import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def setUp(self) -> None:
        # Configuração comum para os testes
        self.node_simples = LeafNode("p", "Hello, world!")
        self.node_com_props = LeafNode(
            "a", "Click me!", {"href": "https://www.google.com"}
        )
        self.node_sem_tag = LeafNode(None, "Raw text")
        self.node_sem_valor = LeafNode("p", "")
        self.node_props_multiplas = LeafNode(
            "button",
            "Submit",
            {"type": "submit", "class": "btn", "id": "submit-btn"},
        )
        self.node_props_vazias = LeafNode("span", "Empty props", {})

    def test_init(self) -> None:
        # Testa inicialização básica
        self.assertEqual(self.node_simples.tag, "p")
        self.assertEqual(self.node_simples.value, "Hello, world!")
        self.assertEqual(self.node_simples.props, {})
        self.assertEqual(self.node_simples.children, [])

        # Testa inicialização com propriedades
        self.assertEqual(self.node_com_props.tag, "a")
        self.assertEqual(self.node_com_props.value, "Click me!")
        props = {"href": "https://www.google.com"}
        self.assertEqual(self.node_com_props.props, props)

        # Testa inicialização sem tag
        self.assertIsNone(self.node_sem_tag.tag)
        self.assertEqual(self.node_sem_tag.value, "Raw text")

        # Testa inicialização com múltiplas propriedades
        self.assertEqual(self.node_props_multiplas.tag, "button")
        expected_props = {"type": "submit", "class": "btn", "id": "submit-btn"}
        self.assertEqual(self.node_props_multiplas.props, expected_props)

    def test_to_html_p(self) -> None:
        self.assertEqual(self.node_simples.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_props(self) -> None:
        expected_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(self.node_com_props.to_html(), expected_html)

        # Testa com múltiplas propriedades
        html = self.node_props_multiplas.to_html()
        self.assertIn("<button", html)
        self.assertIn('type="submit"', html)
        self.assertIn('class="btn"', html)
        self.assertIn('id="submit-btn"', html)
        self.assertIn(">Submit</button>", html)

    def test_to_html_no_tag(self) -> None:
        self.assertEqual(self.node_sem_tag.to_html(), "Raw text")

    def test_to_html_no_value(self) -> None:
        self.node_sem_valor.value = None
        with self.assertRaises(ValueError):
            self.node_sem_valor.to_html()

    def test_to_html_empty_props(self) -> None:
        # Testa que props vazias são tratadas corretamente
        expected_html = "<span>Empty props</span>"
        self.assertEqual(self.node_props_vazias.to_html(), expected_html)

    def test_repr(self) -> None:
        # Testa representação de string do objeto
        expected_simple = "HTMLNode(p, Hello, world!, [], {})"
        self.assertEqual(repr(self.node_simples), expected_simple)

        # Uso string literal para evitar problemas com formatadores
        props_str = "{'href': 'https://www.google.com'}"
        expected_repr = f"HTMLNode(a, Click me!, [], {props_str})"
        self.assertEqual(repr(self.node_com_props), expected_repr)


if __name__ == "__main__":
    unittest.main()
