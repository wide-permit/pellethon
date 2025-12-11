import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    """Comprehensive test suite for LeafNode class"""

    # Initialization Tests
    def test_init_basic(self):
        """Test creating a basic leaf node"""
        node = LeafNode("p", "Hello World")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello World")
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_init_with_props(self):
        """Test creating a leaf node with props"""
        props = {"class": "text", "id": "main"}
        node = LeafNode("div", "Content", props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Content")
        self.assertEqual(node.props, props)
        self.assertIsNone(node.children)

    def test_init_none_tag(self):
        """Test creating a leaf node with None tag (for plain text)"""
        node = LeafNode(None, "Plain text")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Plain text")
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_init_none_tag_with_props(self):
        """Test creating a leaf node with None tag and props"""
        props = {"class": "text"}
        node = LeafNode(None, "Plain text", props)
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Plain text")
        self.assertEqual(node.props, props)

    def test_init_empty_string_tag(self):
        """Test creating a leaf node with empty string tag"""
        node = LeafNode("", "Content")
        self.assertEqual(node.tag, "")
        self.assertEqual(node.value, "Content")

    def test_init_empty_string_value(self):
        """Test creating a leaf node with empty string value"""
        node = LeafNode("p", "")
        self.assertEqual(node.value, "")

    def test_init_empty_props_dict(self):
        """Test creating a leaf node with empty props dict"""
        node = LeafNode("div", "Content", {})
        self.assertEqual(node.props, {})

    def test_init_children_not_set(self):
        """Test that children is not set (LeafNode doesn't accept children)"""
        node = LeafNode("p", "Content")
        # LeafNode doesn't set children, so it should be None from HTMLNode
        self.assertIsNone(node.children)

    def test_inheritance_from_htmlnode(self):
        """Test that LeafNode inherits from HTMLNode"""
        node = LeafNode("p", "Content")
        self.assertIsInstance(node, HTMLNode)
        self.assertIsInstance(node, LeafNode)

    # to_html Tests - Success Cases
    def test_to_html_basic_paragraph(self):
        """Test to_html with basic paragraph"""
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_to_html_bold_text(self):
        """Test to_html with bold tag"""
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_to_html_italic_text(self):
        """Test to_html with italic tag"""
        node = LeafNode("i", "Italic text")
        self.assertEqual(node.to_html(), "<i>Italic text</i>")

    def test_to_html_span(self):
        """Test to_html with span tag"""
        node = LeafNode("span", "Span content")
        self.assertEqual(node.to_html(), "<span>Span content</span>")

    def test_to_html_none_tag(self):
        """Test to_html with None tag returns raw value"""
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_to_html_empty_string_value(self):
        """Test to_html with empty string value"""
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_to_html_whitespace_value(self):
        """Test to_html with whitespace value"""
        node = LeafNode("p", "   ")
        self.assertEqual(node.to_html(), "<p>   </p>")

    def test_to_html_various_tags(self):
        """Test to_html with various HTML tags"""
        tags = ["div", "span", "p", "a", "code", "pre", "h1", "h2", "strong", "em"]
        for tag in tags:
            node = LeafNode(tag, "content")
            expected = f"<{tag}>content</{tag}>"
            self.assertEqual(node.to_html(), expected)

    def test_to_html_unicode_content(self):
        """Test to_html with Unicode characters"""
        node = LeafNode("p", "Hello 世界 🌍")
        self.assertEqual(node.to_html(), "<p>Hello 世界 🌍</p>")

    def test_to_html_special_html_chars(self):
        """Test to_html with special HTML characters (not escaped by implementation)"""
        node = LeafNode("p", "< > & \" '")
        # Note: The implementation doesn't escape HTML entities
        self.assertEqual(node.to_html(), "<p>< > & \" '</p>")

    def test_to_html_multiline_value(self):
        """Test to_html with multiline value"""
        node = LeafNode("pre", "Line 1\nLine 2\nLine 3")
        self.assertEqual(node.to_html(), "<pre>Line 1\nLine 2\nLine 3</pre>")

    def test_to_html_very_long_value(self):
        """Test to_html with very long value"""
        long_text = "a" * 10000
        node = LeafNode("p", long_text)
        expected = f"<p>{long_text}</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_empty_tag(self):
        """Test to_html with empty string tag"""
        node = LeafNode("", "content")
        self.assertEqual(node.to_html(), "<>content</>")

    # to_html Tests - Error Cases
    def test_to_html_none_value_raises_error(self):
        """Test that to_html raises ValueError when value is None"""
        node = LeafNode("p", "test")
        node.value = None  # Manually set to None after creation
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_none_value_with_none_tag(self):
        """Test that to_html raises ValueError even with None tag"""
        node = LeafNode(None, "test")
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_none_value_with_props(self):
        """Test that to_html raises ValueError even with props"""
        node = LeafNode("p", "test", {"class": "test"})
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

    # Props Integration Tests (inherited from HTMLNode)
    def test_props_to_html_inherited(self):
        """Test that props_to_html method is inherited"""
        props = {"class": "container", "id": "main"}
        node = LeafNode("div", "Content", props)
        result = node.props_to_html()
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)

    def test_props_to_html_none_props(self):
        """Test props_to_html with no props"""
        node = LeafNode("p", "Content")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        """Test props_to_html with empty dict"""
        node = LeafNode("p", "Content", {})
        self.assertEqual(node.props_to_html(), "")

    # Note: LeafNode doesn't override to_html to use props
    # This tests current behavior
    def test_to_html_ignores_props(self):
        """Test that to_html doesn't include props in output"""
        props = {"class": "test", "id": "main"}
        node = LeafNode("p", "Content", props)
        result = node.to_html()
        # Current implementation doesn't use props in to_html
        self.assertEqual(result, "<p>Content</p>")
        self.assertNotIn("class", result)
        self.assertNotIn("id", result)

    # __repr__ Tests (inherited from HTMLNode)
    def test_repr_basic(self):
        """Test string representation"""
        node = LeafNode("p", "Content")
        result = repr(node)
        self.assertIn("LeafNode", result)
        self.assertIn("p", result)
        self.assertIn("Content", result)

    def test_repr_with_props(self):
        """Test string representation with props"""
        props = {"class": "test"}
        node = LeafNode("div", "Content", props)
        result = repr(node)
        self.assertIn("LeafNode", result)
        self.assertIn("class", result)

    def test_repr_none_tag(self):
        """Test string representation with None tag"""
        node = LeafNode(None, "Plain text")
        result = repr(node)
        self.assertIn("LeafNode", result)
        self.assertIn("Plain text", result)

    # Edge Cases
    def test_single_character_value(self):
        """Test with single character value"""
        node = LeafNode("p", "a")
        self.assertEqual(node.to_html(), "<p>a</p>")

    def test_numeric_tag_name(self):
        """Test with numeric characters in tag"""
        node = LeafNode("h1", "Heading")
        self.assertEqual(node.to_html(), "<h1>Heading</h1>")

    def test_hyphenated_tag_name(self):
        """Test with hyphenated tag name (custom elements)"""
        node = LeafNode("my-element", "Content")
        self.assertEqual(node.to_html(), "<my-element>Content</my-element>")

    def test_tag_with_numbers(self):
        """Test with tags containing numbers"""
        for i in range(1, 7):
            node = LeafNode(f"h{i}", f"Heading {i}")
            self.assertEqual(node.to_html(), f"<h{i}>Heading {i}</h{i}>")

    def test_multiple_instances(self):
        """Test multiple instances don't interfere"""
        node1 = LeafNode("p", "First")
        node2 = LeafNode("div", "Second")
        node3 = LeafNode("span", "Third")

        self.assertEqual(node1.to_html(), "<p>First</p>")
        self.assertEqual(node2.to_html(), "<div>Second</div>")
        self.assertEqual(node3.to_html(), "<span>Third</span>")

    def test_modifying_value_after_creation(self):
        """Test modifying value after node creation"""
        node = LeafNode("p", "Original")
        self.assertEqual(node.to_html(), "<p>Original</p>")

        node.value = "Modified"
        self.assertEqual(node.to_html(), "<p>Modified</p>")

    def test_modifying_tag_after_creation(self):
        """Test modifying tag after node creation"""
        node = LeafNode("p", "Content")
        self.assertEqual(node.to_html(), "<p>Content</p>")

        node.tag = "div"
        self.assertEqual(node.to_html(), "<div>Content</div>")

    def test_setting_tag_to_none_after_creation(self):
        """Test setting tag to None after creation"""
        node = LeafNode("p", "Content")
        node.tag = None
        self.assertEqual(node.to_html(), "Content")

    def test_common_html_elements(self):
        """Test common HTML elements"""
        elements = {
            "p": "Paragraph text",
            "a": "Link text",
            "strong": "Strong text",
            "em": "Emphasized text",
            "code": "Code snippet",
            "span": "Span content",
            "div": "Division content",
            "h1": "Main heading",
            "li": "List item",
            "td": "Table cell",
        }

        for tag, content in elements.items():
            node = LeafNode(tag, content)
            expected = f"<{tag}>{content}</{tag}>"
            self.assertEqual(node.to_html(), expected)

    def test_value_with_tabs(self):
        """Test value containing tabs"""
        node = LeafNode("pre", "Code\twith\ttabs")
        self.assertEqual(node.to_html(), "<pre>Code\twith\ttabs</pre>")

    def test_value_with_special_whitespace(self):
        """Test value with various whitespace characters"""
        node = LeafNode("pre", "Line1\nLine2\rLine3\tTabbed")
        expected = "<pre>Line1\nLine2\rLine3\tTabbed</pre>"
        self.assertEqual(node.to_html(), expected)

    def test_props_modification_after_creation(self):
        """Test modifying props after creation"""
        props = {"class": "original"}
        node = LeafNode("div", "Content", props)

        # Modify props
        node.props["class"] = "modified"
        node.props["id"] = "new"

        result = node.props_to_html()
        self.assertIn('class="modified"', result)
        self.assertIn('id="new"', result)

    def test_case_sensitive_tags(self):
        """Test that tags are case-sensitive"""
        node_lower = LeafNode("div", "Content")
        node_upper = LeafNode("DIV", "Content")

        self.assertEqual(node_lower.to_html(), "<div>Content</div>")
        self.assertEqual(node_upper.to_html(), "<DIV>Content</DIV>")

    def test_value_only_spaces(self):
        """Test value containing only spaces"""
        node = LeafNode("p", "     ")
        self.assertEqual(node.to_html(), "<p>     </p>")

    def test_self_closing_tag_format(self):
        """Test that implementation doesn't create self-closing tags"""
        # Even for typically self-closing tags, this implementation uses full format
        node = LeafNode("br", "")
        self.assertEqual(node.to_html(), "<br></br>")

        node2 = LeafNode("img", "")
        self.assertEqual(node2.to_html(), "<img></img>")


if __name__ == "__main__":
    unittest.main()
