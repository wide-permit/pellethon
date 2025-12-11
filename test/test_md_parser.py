import unittest

from md_parser import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    # all text types
    def test_all_text_types(self):
        bold = "This is a **bold** text"
        italic = "This is a _italic_ text"
        code = "This is a `code` text"

        bold_node = TextNode(bold, TextType.TEXT)
        italic_node = TextNode(italic, TextType.TEXT)
        code_node = TextNode(code, TextType.TEXT)

        bold_new_nodes = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        italic_new_nodes = split_nodes_delimiter([italic_node], "_", TextType.ITALIC)
        code_new_nodes = split_nodes_delimiter([code_node], "`", TextType.CODE)

        test_bold = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        test_italic = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        test_code = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertListEqual(bold_new_nodes, test_bold)
        self.assertListEqual(italic_new_nodes, test_italic)
        self.assertListEqual(code_new_nodes, test_code)

    # Raise Exception invalid md syntax
    def test_invalid_syntax(self):
        with self.assertRaises(Exception):
            (
                split_nodes_delimiter(
                    [TextNode("This **is **invalid** markdown syntax", TextType.TEXT)],
                    "**",
                    TextType.BOLD,
                ),
                "Invalid markdown",
            )

    # delimiter @ beginning or end
    def test_delimiter_edge(self):
        node1 = TextNode("*This should* be italic", TextType.TEXT)
        node2 = TextNode("This should be `code`", TextType.TEXT)
        test_node1 = [
            TextNode("This should", TextType.ITALIC),
            TextNode(" be italic", TextType.TEXT),
        ]
        test_node2 = [
            TextNode("This should be ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertListEqual(
            split_nodes_delimiter([node1], "*", TextType.ITALIC), test_node1
        )
        self.assertListEqual(
            split_nodes_delimiter([node2], "`", TextType.CODE), test_node2
        )

    # empty -> returns empty
    def test_empty(self):
        node = TextNode("", TextType.TEXT)
        test_node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "", TextType.TEXT), [test_node])

    # mutliple inline same delimiter-> should only parse the the given delimiter code
    def test_multi_inline_same_delimiter(self):
        node = TextNode("This __should__ have __two__ bold words", TextType.TEXT)
        test_node = [
            TextNode("This ", TextType.TEXT),
            TextNode("should", TextType.BOLD),
            TextNode(" have ", TextType.TEXT),
            TextNode,
        ]


# multiple inline different delimiter -> ""
# multiple nested
#

if __name__ == "__main__":
    unittest.main()
