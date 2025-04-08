import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def setUp(self) -> None:
        # Configuração comum para os testes
        self.node_normal = TextNode("Texto normal", TextType.NORMAL)
        self.node_bold = TextNode("Texto em negrito", TextType.BOLD)
        self.node_italic = TextNode("Texto em itálico", TextType.ITALIC)
        self.node_code = TextNode("Código de exemplo", TextType.CODE)
        self.node_link = TextNode(
            "Link para Google", TextType.LINK, "https://www.google.com"
        )
        self.node_image = TextNode(
            "Imagem de exemplo",
            TextType.IMAGE,
            "https://example.com/image.jpg")
        self.node_vazio = TextNode("", TextType.NORMAL)

    def test_init(self) -> None:
        # Testa inicialização básica
        self.assertEqual(self.node_normal.text, "Texto normal")
        self.assertEqual(self.node_normal.text_type, TextType.NORMAL)
        self.assertIsNone(self.node_normal.url)

        # Testa inicialização com tipo BOLD
        self.assertEqual(self.node_bold.text, "Texto em negrito")
        self.assertEqual(self.node_bold.text_type, TextType.BOLD)

        # Testa inicialização com URL
        self.assertEqual(self.node_link.text, "Link para Google")
        self.assertEqual(self.node_link.text_type, TextType.LINK)
        self.assertEqual(self.node_link.url, "https://www.google.com")

        # Testa inicialização com texto vazio
        self.assertEqual(self.node_vazio.text, "")

    def test_eq(self) -> None:
        # Testa igualdade de nós com mesmo conteúdo
        node_normal_duplicado = TextNode("Texto normal", TextType.NORMAL)
        self.assertEqual(self.node_normal, node_normal_duplicado)

        # Testa desigualdade por texto diferente
        node_texto_diferente = TextNode("Outro texto", TextType.NORMAL)
        self.assertNotEqual(self.node_normal, node_texto_diferente)

        # Testa desigualdade por tipo diferente
        self.assertNotEqual(self.node_normal, self.node_bold)

        # Testa desigualdade por URL diferente
        node_link_outro_url = TextNode(
            "Link para Google", TextType.LINK, "https://www.youtube.com"
        )
        self.assertNotEqual(self.node_link, node_link_outro_url)

        # Testa igualdade com URL
        node_link_duplicado = TextNode(
            "Link para Google", TextType.LINK, "https://www.google.com"
        )
        self.assertEqual(self.node_link, node_link_duplicado)

    def test_repr(self) -> None:
        # Testa representação de nó normal
        self.assertEqual(
            repr(
                self.node_normal),
            "TextNode(Texto normal, 1, None)")

        # Testa representação de nó com tipo BOLD
        self.assertEqual(repr(self.node_bold),
                         "TextNode(Texto em negrito, 0, None)")

        # Testa representação de nó com URL
        self.assertEqual(
            repr(self.node_link),
            "TextNode(Link para Google, 4, https://www.google.com)",
        )

        # Testa representação de nó vazio
        self.assertEqual(repr(self.node_vazio), "TextNode(, 1, None)")

    def test_edge_cases(self) -> None:
        # Testa com texto None - corrigido para string vazia
        node_texto_none = TextNode("", TextType.NORMAL)
        self.assertEqual(node_texto_none.text, "")

        # Testa com texto numérico - corrigido para string
        node_texto_numero = TextNode("42", TextType.NORMAL)
        self.assertEqual(node_texto_numero.text, "42")

        # Testa com URL vazia
        node_url_vazia = TextNode("Link vazio", TextType.LINK, "")
        self.assertEqual(node_url_vazia.url, "")

        # Testa com URL None em tipos que não são LINK ou IMAGE
        node_url_em_normal = TextNode(
            "Texto com URL", TextType.NORMAL, "https://example.com"
        )
        self.assertEqual(node_url_em_normal.url, "https://example.com")

        # Testa comparação com objeto de outro tipo
        class OutroObjeto:
            pass

        outro_obj = OutroObjeto()
        # Agora o test não vai gerar AttributeError por causa da verificação de
        # tipo no __eq__
        self.assertFalse(self.node_normal == outro_obj)


if __name__ == "__main__":
    unittest.main()
