import unittest
from typing import List, cast

from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def setUp(self) -> None:
        # Configuração comum para os testes
        self.filho1 = HTMLNode("p", "Parágrafo 1", [], {})
        self.filho2 = HTMLNode("p", "Parágrafo 2", [], {"class": "destaque"})
        self.node_simples = ParentNode("div", [self.filho1, self.filho2])
        self.node_com_props = ParentNode(
            "section",
            [self.filho1, self.filho2],
            {"id": "conteudo", "class": "container"},
        )
        self.node_sem_filhos = ParentNode("span", [])
        self.node_sem_tag = ParentNode("", [self.filho1])

    def test_init(self) -> None:
        # Testa inicialização básica
        self.assertEqual(self.node_simples.tag, "div")
        self.assertIsNone(self.node_simples.value)

        # Cast para garantir tipagem correta
        children = cast(List[HTMLNode], self.node_simples.children)
        self.assertEqual(len(children), 2)
        self.assertEqual(children[0], self.filho1)
        self.assertEqual(children[1], self.filho2)

        # Quando props não é fornecido, pode ser None
        self.assertIsNone(self.node_simples.props)

        # Testa inicialização com propriedades
        self.assertEqual(self.node_com_props.tag, "section")
        self.assertIsNone(self.node_com_props.value)

        # Usamos cast para verificador de tipos
        children = cast(List[HTMLNode], self.node_com_props.children)
        self.assertEqual(len(children), 2)

        props = {"id": "conteudo", "class": "container"}
        self.assertEqual(self.node_com_props.props, props)

    def test_to_html(self) -> None:
        # Mock para simular o comportamento dos filhos
        class MockNode(HTMLNode):
            def to_html(self) -> str:
                return f"<{self.tag}>{self.value}</{self.tag}>"

        mock_filho1 = MockNode("p", "Texto 1", [], {})
        mock_filho2 = MockNode("p", "Texto 2", [], {})
        node = ParentNode("div", [mock_filho1, mock_filho2])

        expected_html = "<div><p>Texto 1</p><p>Texto 2</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_props(self) -> None:
        # Mock para simular o comportamento dos filhos
        class MockNode(HTMLNode):
            def to_html(self) -> str:
                return f"<{self.tag}>{self.value}</{self.tag}>"

        mock_filho = MockNode("p", "Texto", [], {})
        props = {"class": "container", "id": "main"}
        node = ParentNode("div", [mock_filho], props)

        html = node.to_html()
        expected_html = "<div><p>Texto</p></div>"
        # O to_html atual não usa props
        self.assertEqual(html, expected_html)

    def test_to_html_exceptions(self) -> None:
        # Testa exceção quando não há tag
        with self.assertRaises(ValueError):
            self.node_sem_tag.to_html()

        # Testa exceção quando não há filhos
        with self.assertRaises(ValueError):
            self.node_sem_filhos.to_html()

    def test_repr(self) -> None:
        # Testa representação de string do objeto
        filho1_repr = repr(self.filho1)
        filho2_repr = repr(self.filho2)

        # Quebrar a string em partes menores para evitar linha longa
        filhos_str = f"[{filho1_repr}, {filho2_repr}]"
        expected = f"HTMLNode(div, None, {filhos_str}, None)"
        self.assertEqual(repr(self.node_simples), expected)

        # String literal para evitar problemas com formatadores
        props_dict_str = "{'id': 'conteudo', 'class': 'container'}"
        base = f"HTMLNode(section, None, {filhos_str}, "
        expected_repr = f"{base}{props_dict_str})"
        self.assertEqual(repr(self.node_com_props), expected_repr)

    def test_hierarquia_multipla(self) -> None:
        # Teste com múltiplos níveis hierárquicos (filhos e netos)
        # Netos (nível mais profundo)
        neto1 = LeafNode("span", "Neto 1")
        neto2 = LeafNode("span", "Neto 2")
        neto3 = LeafNode("span", "Neto 3")
        neto4 = LeafNode("span", "Neto 4")

        # Filhos intermediários que contêm netos
        filho1 = ParentNode("div", [neto1, neto2])
        filho2 = ParentNode("div", [neto3, neto4])
        filho3 = LeafNode("p", "Filho simples")

        # Nó pai que contém todos os filhos
        node_raiz = ParentNode("section", [filho1, filho2, filho3])

        # Verificar HTML gerado
        html_esperado = (
            "<section>"
            "<div>"
            "<span>Neto 1</span>"
            "<span>Neto 2</span>"
            "</div>"
            "<div>"
            "<span>Neto 3</span>"
            "<span>Neto 4</span>"
            "</div>"
            "<p>Filho simples</p>"
            "</section>"
        )
        self.assertEqual(node_raiz.to_html(), html_esperado)

    def test_hierarquia_complexa_com_props(self) -> None:
        # Teste com múltiplos níveis e propriedades
        # Criar uma estrutura mais complexa com propriedades
        item1 = LeafNode("li", "Item 1", {"class": "item"})
        item2 = LeafNode("li", "Item 2", {"class": "item destacado"})
        item3 = LeafNode("li", "Item 3", {"class": "item"})

        # Lista não ordenada com itens
        lista = ParentNode(
            "ul",
            [item1, item2, item3],
            {"class": "lista-itens"},
        )

        # Título e parágrafo
        titulo = LeafNode("h2", "Título da Seção")
        paragrafo = LeafNode("p", "Descrição da seção", {"class": "texto"})

        # Container que combina título, parágrafo e lista
        container = ParentNode(
            "div",
            [titulo, paragrafo, lista],
            {"id": "container-principal", "class": "conteudo"},
        )

        html_esperado = (
            "<div>"
            "<h2>Título da Seção</h2>"
            '<p class="texto">Descrição da seção</p>'
            "<ul>"
            '<li class="item">Item 1</li>'
            '<li class="item destacado">Item 2</li>'
            '<li class="item">Item 3</li>'
            "</ul>"
            "</div>"
        )
        self.assertEqual(container.to_html(), html_esperado)


if __name__ == "__main__":
    unittest.main()
