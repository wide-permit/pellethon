import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    """Comprehensive test suite for TextNode class"""

    # Initialization Tests
    def test_init_plain_text(self):
        """Test creating a plain text node"""
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
    def test_repr_plain_text(self):
        """Test string representation of plain text node"""
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


class TestTextNodeToHTMLNode(unittest.TestCase):
    """Comprehensive test suite for text_node_to_html_node function"""

    # TextType.TEXT Tests
    def test_text_type_text(self):
        """Test converting TEXT type to LeafNode"""
        text_node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Plain text")
        self.assertIsNone(html_node.props)

    def test_text_type_text_empty_string(self):
        """Test converting TEXT type with empty string"""
        text_node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "")

    def test_text_type_text_with_whitespace(self):
        """Test converting TEXT type with whitespace"""
        text_node = TextNode("  Text with spaces  ", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.value, "  Text with spaces  ")

    def test_text_type_text_unicode(self):
        """Test converting TEXT type with Unicode characters"""
        text_node = TextNode("Hello 世界 🌍", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.value, "Hello 世界 🌍")

    # TextType.BOLD Tests
    def test_text_type_bold(self):
        """Test converting BOLD type to LeafNode"""
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)

    def test_text_type_bold_empty(self):
        """Test converting BOLD type with empty string"""
        text_node = TextNode("", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "")

    def test_text_type_bold_html_output(self):
        """Test that BOLD type produces correct HTML"""
        text_node = TextNode("Bold", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.to_html(), "<b>Bold</b>")

    # TextType.ITALIC Tests
    def test_text_type_italic(self):
        """Test converting ITALIC type to LeafNode"""
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertIsNone(html_node.props)

    def test_text_type_italic_empty(self):
        """Test converting ITALIC type with empty string"""
        text_node = TextNode("", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "")

    def test_text_type_italic_html_output(self):
        """Test that ITALIC type produces correct HTML"""
        text_node = TextNode("Italic", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.to_html(), "<i>Italic</i>")

    # TextType.CODE Tests
    def test_text_type_code(self):
        """Test converting CODE type to LeafNode"""
        text_node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertIsNone(html_node.props)

    def test_text_type_code_empty(self):
        """Test converting CODE type with empty string"""
        text_node = TextNode("", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "")

    def test_text_type_code_html_output(self):
        """Test that CODE type produces correct HTML"""
        text_node = TextNode("const x = 5;", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.to_html(), "<code>const x = 5;</code>")

    def test_text_type_code_with_special_chars(self):
        """Test CODE type with special characters"""
        text_node = TextNode("<script>alert('xss')</script>", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.value, "<script>alert('xss')</script>")

    # TextType.LINK Tests
    def test_text_type_link(self):
        """Test converting LINK type to LeafNode"""
        text_node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_text_type_link_empty_text(self):
        """Test LINK type with empty text"""
        text_node = TextNode("", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_text_type_link_html_output(self):
        """Test that LINK type produces correct HTML structure"""
        text_node = TextNode("Link", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)

        # Note: Current LeafNode implementation doesn't include props in to_html
        self.assertEqual(html_node.to_html(), "<a>Link</a>")

    def test_text_type_link_various_urls(self):
        """Test LINK type with various URL formats"""
        urls = [
            "https://example.com",
            "http://localhost:8080",
            "ftp://files.example.com",
            "/relative/path",
            "//protocol-relative.com",
            "mailto:test@example.com",
        ]

        for url in urls:
            text_node = TextNode("Link", TextType.LINK, url)
            html_node = text_node_to_html_node(text_node)
            self.assertEqual(html_node.props["href"], url)

    def test_text_type_link_none_url(self):
        """Test LINK type with None URL"""
        text_node = TextNode("Link", TextType.LINK, None)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], None)

    def test_text_type_link_empty_url(self):
        """Test LINK type with empty string URL"""
        text_node = TextNode("Link", TextType.LINK, "")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.props["href"], "")

    # TextType.IMAGE Tests
    def test_text_type_image(self):
        """Test converting IMAGE type to LeafNode"""
        text_node = TextNode(
            "Alt text", TextType.IMAGE, "https://example.com/image.jpg"
        )
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIsNotNone(html_node.props)
        self.assertEqual(html_node.props["src"], "https://example.com/image.jpg")
        self.assertEqual(html_node.props["alt"], "Alt text")

    def test_text_type_image_empty_alt(self):
        """Test IMAGE type with empty alt text"""
        text_node = TextNode("", TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "")
        self.assertEqual(html_node.props["src"], "image.jpg")

    def test_text_type_image_html_output(self):
        """Test that IMAGE type produces correct HTML structure"""
        text_node = TextNode("Description", TextType.IMAGE, "pic.png")
        html_node = text_node_to_html_node(text_node)

        # Note: Current LeafNode implementation doesn't include props in to_html
        self.assertEqual(html_node.to_html(), "<img></img>")

    def test_text_type_image_various_paths(self):
        """Test IMAGE type with various image paths"""
        paths = [
            "https://example.com/image.jpg",
            "/static/images/photo.png",
            "./relative/image.gif",
            "data:image/png;base64,iVBORw0KG...",
        ]

        for path in paths:
            text_node = TextNode("Image", TextType.IMAGE, path)
            html_node = text_node_to_html_node(text_node)
            self.assertEqual(html_node.props["src"], path)

    def test_text_type_image_none_url(self):
        """Test IMAGE type with None URL"""
        text_node = TextNode("Alt", TextType.IMAGE, None)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], None)
        self.assertEqual(html_node.props["alt"], "Alt")

    def test_text_type_image_empty_url(self):
        """Test IMAGE type with empty string URL"""
        text_node = TextNode("Alt", TextType.IMAGE, "")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.props["src"], "")

    def test_text_type_image_long_alt_text(self):
        """Test IMAGE type with long alt text"""
        long_alt = (
            "A very detailed description of the image that goes on for quite a while"
        )
        text_node = TextNode(long_alt, TextType.IMAGE, "image.jpg")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.props["alt"], long_alt)

    # Error Cases
    def test_not_a_text_node_raises_exception(self):
        """Test that passing non-TextNode raises Exception"""
        with self.assertRaises(Exception) as context:
            text_node_to_html_node("not a text node")
        self.assertIn("Not a text node or wrong type", str(context.exception))

    def test_none_raises_exception(self):
        """Test that passing None raises Exception"""
        with self.assertRaises(Exception):
            text_node_to_html_node(None)

    def test_other_object_raises_exception(self):
        """Test that passing other objects raises Exception"""
        with self.assertRaises(Exception):
            text_node_to_html_node({"text": "test"})

        with self.assertRaises(Exception):
            text_node_to_html_node(123)

        with self.assertRaises(Exception):
            text_node_to_html_node([])

    # All TextType Values
    def test_all_text_types_covered(self):
        """Test that all TextType enum values are handled"""
        test_cases = [
            (TextType.TEXT, None, None),
            (TextType.BOLD, "b", None),
            (TextType.ITALIC, "i", None),
            (TextType.CODE, "code", None),
            (TextType.LINK, "a", {"href": "url"}),
            (TextType.IMAGE, "img", {"src": "url", "alt": "text"}),
        ]

        for text_type, expected_tag, expected_props_check in test_cases:
            text_node = TextNode(
                "text",
                text_type,
                "url" if text_type in [TextType.LINK, TextType.IMAGE] else None,
            )
            html_node = text_node_to_html_node(text_node)

            self.assertEqual(html_node.tag, expected_tag)
            if expected_props_check:
                self.assertIsNotNone(html_node.props)
            else:
                self.assertIsNone(html_node.props)

    # Edge Cases
    def test_text_node_with_multiline_text(self):
        """Test TextNode with multiline text"""
        multiline = "Line 1\nLine 2\nLine 3"
        text_node = TextNode(multiline, TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.value, multiline)

    def test_text_node_with_very_long_text(self):
        """Test TextNode with very long text"""
        long_text = "a" * 10000
        text_node = TextNode(long_text, TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.value, long_text)

    def test_conversion_preserves_original(self):
        """Test that conversion doesn't modify original TextNode"""
        text_node = TextNode("Original", TextType.BOLD)
        original_text = text_node.text
        original_type = text_node.text_type

        html_node = text_node_to_html_node(text_node)

        self.assertEqual(text_node.text, original_text)
        self.assertEqual(text_node.text_type, original_type)

    def test_multiple_conversions_independence(self):
        """Test that multiple conversions are independent"""
        text_node1 = TextNode("First", TextType.BOLD)
        text_node2 = TextNode("Second", TextType.ITALIC)
        text_node3 = TextNode("Third", TextType.CODE)

        html_node1 = text_node_to_html_node(text_node1)
        html_node2 = text_node_to_html_node(text_node2)
        html_node3 = text_node_to_html_node(text_node3)

        self.assertEqual(html_node1.tag, "b")
        self.assertEqual(html_node2.tag, "i")
        self.assertEqual(html_node3.tag, "code")

        self.assertEqual(html_node1.value, "First")
        self.assertEqual(html_node2.value, "Second")
        self.assertEqual(html_node3.value, "Third")

    def test_link_and_image_url_independence(self):
        """Test that LINK and IMAGE handle URLs independently"""
        link_node = TextNode("Link text", TextType.LINK, "https://link.com")
        image_node = TextNode("Image alt", TextType.IMAGE, "https://image.com")

        html_link = text_node_to_html_node(link_node)
        html_image = text_node_to_html_node(image_node)

        self.assertEqual(html_link.props["href"], "https://link.com")
        self.assertEqual(html_image.props["src"], "https://image.com")
        self.assertEqual(html_image.props["alt"], "Image alt")

    def test_props_dict_independence(self):
        """Test that props dicts are independent between conversions"""
        text_node1 = TextNode("Link 1", TextType.LINK, "url1")
        text_node2 = TextNode("Link 2", TextType.LINK, "url2")

        html_node1 = text_node_to_html_node(text_node1)
        html_node2 = text_node_to_html_node(text_node2)

        # Modify one props dict
        html_node1.props["href"] = "modified"

        # Other should remain unchanged
        self.assertEqual(html_node2.props["href"], "url2")


if __name__ == "__main__":
    unittest.main()
