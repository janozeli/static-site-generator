import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        # Configuração comum para os testes
        self.node_com_props = HTMLNode(
            "a", "Link", None, {"href": "https://www.google.com", "target": "_blank"}
        )
        self.node_sem_props = HTMLNode("div", "Conteúdo", None, {})
        self.node_filho = HTMLNode("span", "texto filho", None, {"class": "destaque"})
        self.node_com_filhos = HTMLNode(
            "div", "", [self.node_filho], {"id": "container"}
        )
        self.node_vazio = HTMLNode("br", "", None, {})

    def test_init(self):
        # Testa inicialização básica
        self.assertEqual(self.node_com_props.tag, "a")
        self.assertEqual(self.node_com_props.value, "Link")
        self.assertIsNone(self.node_com_props.children)
        self.assertEqual(
            self.node_com_props.props,
            {"href": "https://www.google.com", "target": "_blank"},
        )

        # Testa inicialização com filhos
        self.assertEqual(len(self.node_com_filhos.children), 1)
        self.assertEqual(self.node_com_filhos.children[0].tag, "span")

        # Testa inicialização com propriedades vazias
        self.assertEqual(self.node_sem_props.props, {})

        # Testa inicialização com valor vazio
        self.assertEqual(self.node_vazio.value, "")

    def test_repr(self):
        # Testa representação com propriedades
        self.assertEqual(
            repr(self.node_com_props),
            "HTMLNode(a, Link, None, {'href': 'https://www.google.com', 'target': '_blank'})",
        )

        # Testa representação sem propriedades
        self.assertEqual(repr(self.node_sem_props), "HTMLNode(div, Conteúdo, None, {})")

        # Testa representação com filhos
        self.assertEqual(
            repr(self.node_com_filhos),
            f"HTMLNode(div, , [{repr(self.node_filho)}], {{'id': 'container'}})",
        )

        # Testa representação de nó vazio
        self.assertEqual(repr(self.node_vazio), "HTMLNode(br, , None, {})")

    def test_props_to_html(self):
        # Testa conversão de propriedades para HTML
        self.assertEqual(
            self.node_com_props.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

        # Testa conversão de propriedades vazias
        self.assertEqual(self.node_sem_props.props_to_html(), " ")

        # Testa conversão com uma única propriedade
        node_uma_prop = HTMLNode("p", "Texto", None, {"class": "paragrafo"})
        self.assertEqual(node_uma_prop.props_to_html(), ' class="paragrafo"')

        # Testa conversão com tipos especiais de valores
        node_props_especiais = HTMLNode(
            "input", "", None, {"type": "text", "disabled": "true", "data-id": "123"}
        )
        props_html = node_props_especiais.props_to_html()
        self.assertIn('type="text"', props_html)
        self.assertIn('disabled="true"', props_html)
        self.assertIn('data-id="123"', props_html)

    def test_to_html(self):
        # Testa que o método lança NotImplementedError conforme esperado
        with self.assertRaises(NotImplementedError):
            self.node_com_props.to_html()

        with self.assertRaises(NotImplementedError):
            self.node_sem_props.to_html()

        with self.assertRaises(NotImplementedError):
            self.node_com_filhos.to_html()

    def test_edge_cases(self):
        # Testa com valor None
        node_valor_none = HTMLNode("div", None, None, {})
        self.assertIsNone(node_valor_none.value)

        # Testa com valor numérico
        node_valor_numero = HTMLNode("span", 42, None, {})
        self.assertEqual(node_valor_numero.value, 42)

        # Testa com valor booleano
        node_valor_bool = HTMLNode("span", True, None, {})
        self.assertEqual(node_valor_bool.value, True)

        # Testa com lista vazia de filhos
        node_filhos_vazio = HTMLNode("ul", "", [], {})
        self.assertEqual(node_filhos_vazio.children, [])

        # Testa com múltiplos filhos
        filho1 = HTMLNode("li", "Item 1", None, {})
        filho2 = HTMLNode("li", "Item 2", None, {})
        node_multiplos_filhos = HTMLNode("ul", "", [filho1, filho2], {})
        self.assertEqual(len(node_multiplos_filhos.children), 2)


if __name__ == "__main__":
    unittest.main()
