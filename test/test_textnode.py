import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_neq(self):
        node1 = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a not a text node", TextType.IMAGE)
        self.assertNotEqual(node1, node2)

    def test_init_text_text(self):
        """Test creating a text text node"""
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_init_with_url(self):
        """Test creating a node with URL"""
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Click here")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")

    def test_init_empty_string(self):
        """Test creating a node with empty string"""
        node = TextNode("", TextType.TEXT)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.TEXT)

    def test_init_all_text_types(self):
        """Test creating nodes with all text types"""
        for text_type in TextType:
            node = TextNode("test", text_type)
            self.assertEqual(node.text_type, text_type)

    # Equality Tests
    def test_eq_identical_nodes(self):
        """Test equality of identical nodes"""
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_identical_nodes_with_url(self):
        """Test equality of identical nodes with URLs"""
        node1 = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://example.com")
        self.assertEqual(node1, node2)

    def test_eq_different_text(self):
        """Test inequality when text differs"""
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("World", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_eq_different_text_type(self):
        """Test inequality when text type differs"""
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_eq_different_url(self):
        """Test inequality when URL differs"""
        node1 = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://different.com")
        self.assertNotEqual(node1, node2)

    def test_eq_one_url_none(self):
        """Test inequality when one URL is None"""
        node1 = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, None)
        self.assertNotEqual(node1, node2)

    def test_eq_both_urls_none(self):
        """Test equality when both URLs are None"""
        node1 = TextNode("Text", TextType.TEXT, None)
        node2 = TextNode("Text", TextType.TEXT, None)
        self.assertEqual(node1, node2)

    def test_eq_with_non_textnode(self):
        """Test inequality with non-TextNode objects"""
        node = TextNode("Hello", TextType.TEXT)
        self.assertNotEqual(node, "Hello")
        self.assertNotEqual(node, 42)
        self.assertNotEqual(node, None)
        self.assertNotEqual(node, {"text": "Hello"})

    def test_eq_reflexive(self):
        """Test that a node equals itself"""
        node = TextNode("Hello", TextType.BOLD)
        self.assertEqual(node, node)

    def test_eq_symmetric(self):
        """Test equality is symmetric"""
        node1 = TextNode("Hello", TextType.ITALIC)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertEqual(node1, node2)
        self.assertEqual(node2, node1)

    def test_eq_transitive(self):
        """Test equality is transitive"""
        node1 = TextNode("Code", TextType.CODE)
        node2 = TextNode("Code", TextType.CODE)
        node3 = TextNode("Code", TextType.CODE)
        self.assertEqual(node1, node2)
        self.assertEqual(node2, node3)
        self.assertEqual(node1, node3)

    # Representation Tests
    def test_repr_text_text(self):
        """Test string representation of text text node"""
        node = TextNode("Hello", TextType.TEXT)
        expected = "TextNode(Hello, text, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_url(self):
        """Test string representation with URL"""
        node = TextNode("Link", TextType.LINK, "https://example.com")
        expected = "TextNode(Link, link, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_repr_all_types(self):
        """Test representation for all text types"""
        test_cases = [
            (TextType.TEXT, "text"),
            (TextType.BOLD, "bold"),
            (TextType.ITALIC, "italic"),
            (TextType.CODE, "code"),
            (TextType.LINK, "link"),
            (TextType.IMAGE, "image"),
        ]
        for text_type, expected_value in test_cases:
            node = TextNode("test", text_type)
            self.assertIn(expected_value, repr(node))

    def test_repr_empty_string(self):
        """Test representation with empty string"""
        node = TextNode("", TextType.TEXT)
        expected = "TextNode(, text, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_special_characters(self):
        """Test representation with special characters"""
        node = TextNode("Hello\nWorld", TextType.TEXT)
        expected = "TextNode(Hello\nWorld, text, None)"
        self.assertEqual(repr(node), expected)

    # Edge Case Tests
    def test_unicode_text(self):
        """Test with Unicode characters"""
        node = TextNode("🚀 Hello 世界", TextType.TEXT)
        self.assertEqual(node.text, "🚀 Hello 世界")

    def test_very_long_text(self):
        """Test with very long text"""
        long_text = "a" * 10000
        node = TextNode(long_text, TextType.TEXT)
        self.assertEqual(node.text, long_text)

    def test_whitespace_text(self):
        """Test with various whitespace"""
        node = TextNode("   \t\n  ", TextType.TEXT)
        self.assertEqual(node.text, "   \t\n  ")

    def test_url_edge_cases(self):
        """Test various URL formats"""
        urls = [
            "",
            "https://example.com",
            "http://localhost:8080/path",
            "ftp://files.example.com",
            "//relative-url.com",
        ]
        for url in urls:
            node = TextNode("test", TextType.LINK, url)
            self.assertEqual(node.url, url)

    def test_multiple_nodes_independence(self):
        """Test that modifying one node doesn't affect others"""
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.TEXT)

        node1.text = "Modified"
        self.assertEqual(node2.text, "Hello")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
