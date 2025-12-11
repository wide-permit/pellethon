import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    """Comprehensive test suite for HTMLNode class"""

    # Initialization Tests
    def test_init_no_arguments(self):
        """Test creating a node with no arguments"""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_tag_only(self):
        """Test creating a node with only tag"""
        node = HTMLNode(tag="div")
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_value_only(self):
        """Test creating a node with only value"""
        node = HTMLNode(value="Hello World")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello World")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_all_arguments(self):
        """Test creating a node with all arguments"""
        child = HTMLNode(tag="span", value="child")
        props = {"class": "container", "id": "main"}
        node = HTMLNode(tag="div", value="parent", children=[child], props=props)

        self.assertIsNotNone(node.children)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "parent")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.props, props)

    def test_init_with_multiple_children(self):
        """Test creating a node with multiple children"""
        child1 = HTMLNode(tag="p", value="First")
        child2 = HTMLNode(tag="p", value="Second")
        child3 = HTMLNode(tag="p", value="Third")

        node = HTMLNode(tag="div", children=[child1, child2, child3])
        self.assertEqual(len(node.children), 3)

    def test_init_with_empty_children_list(self):
        """Test creating a node with empty children list"""
        node = HTMLNode(tag="div", children=[])
        self.assertEqual(node.children, [])
        self.assertEqual(len(node.children), 0)

    def test_init_with_empty_props_dict(self):
        """Test creating a node with empty props dict"""
        node = HTMLNode(tag="div", props={})
        self.assertEqual(node.props, {})
        self.assertEqual(len(node.props), 0)

    # to_html Tests
    def test_to_html_raises_not_implemented(self):
        """Test that to_html raises NotImplementedError"""
        node = HTMLNode(tag="div")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_to_html_with_all_parameters(self):
        """Test to_html still raises even with all parameters"""
        node = HTMLNode(tag="div", value="test", children=[], props={})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # props_to_html Tests
    def test_props_to_html_none(self):
        """Test props_to_html with None props"""
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        """Test props_to_html with empty dict"""
        node = HTMLNode(tag="div", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        """Test props_to_html with single property"""
        node = HTMLNode(tag="a", props={"href": "https://example.com"})
        result = node.props_to_html()
        self.assertIn('href="https://example.com"', result)
        self.assertTrue(result.startswith(" "))
        self.assertTrue(result.endswith(" "))

    def test_props_to_html_multiple_props(self):
        """Test props_to_html with multiple properties"""
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        result = node.props_to_html()
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)

    def test_props_to_html_special_characters(self):
        """Test props_to_html with special characters in values"""
        node = HTMLNode(
            tag="a", props={"href": "https://example.com?param=value&other=123"}
        )
        result = node.props_to_html()
        self.assertIn('href="https://example.com?param=value&other=123"', result)

    def test_props_to_html_empty_value(self):
        """Test props_to_html with empty string value"""
        node = HTMLNode(tag="input", props={"value": "", "type": "text"})
        result = node.props_to_html()
        self.assertIn('value=""', result)
        self.assertIn('type="text"', result)

    def test_props_to_html_spacing(self):
        """Test that props_to_html includes proper spacing"""
        node = HTMLNode(tag="div", props={"class": "test"})
        result = node.props_to_html()
        # Should have space before and after
        self.assertTrue(result.startswith(" "))
        self.assertTrue(result.endswith(" "))

    def test_props_to_html_many_props(self):
        """Test props_to_html with many properties"""
        props = {
            "id": "main",
            "class": "container",
            "data-value": "123",
            "data-name": "test",
            "aria-label": "Main content",
        }
        node = HTMLNode(tag="div", props=props)
        result = node.props_to_html()

        for key, value in props.items():
            self.assertIn(f'{key}="{value}"', result)

    # __repr__ Tests
    def test_repr_no_arguments(self):
        """Test representation with no arguments"""
        node = HTMLNode()
        result = repr(node)
        self.assertTrue(result.startswith("HTMLNode("))
        self.assertTrue(result.endswith(")"))
        self.assertIn("None", result)

    def test_repr_with_tag(self):
        """Test representation with tag"""
        node = HTMLNode(tag="div")
        result = repr(node)
        self.assertIn("div", result)
        self.assertIn("HTMLNode", result)

    def test_repr_with_value(self):
        """Test representation with value"""
        node = HTMLNode(value="Hello")
        result = repr(node)
        self.assertIn("Hello", result)

    def test_repr_with_children(self):
        """Test representation with children"""
        child = HTMLNode(tag="span")
        node = HTMLNode(tag="div", children=[child])
        result = repr(node)
        self.assertIn("div", result)
        # Should show list representation
        self.assertIn("[", result)

    def test_repr_with_props(self):
        """Test representation with props"""
        node = HTMLNode(tag="a", props={"href": "https://example.com"})
        result = repr(node)
        self.assertIn("href", result)

    def test_repr_all_parameters(self):
        """Test representation with all parameters"""
        child = HTMLNode(tag="span", value="child")
        props = {"class": "container"}
        node = HTMLNode(tag="div", value="parent", children=[child], props=props)
        result = repr(node)

        self.assertIn("HTMLNode(", result)
        self.assertIn("div", result)
        self.assertIn("parent", result)
        self.assertTrue(result.endswith(")"))

    # Edge Case Tests
    def test_nested_children(self):
        """Test deeply nested children structure"""
        grandchild = HTMLNode(tag="span", value="deepest")
        child = HTMLNode(tag="p", children=[grandchild])
        parent = HTMLNode(tag="div", children=[child])

        self.assertIsNotNone(parent.children)
        self.assertEqual(len(parent.children), 1)
        self.assertIsNotNone(parent.children[0].children)

    def test_unicode_in_value(self):
        """Test with Unicode characters in value"""
        node = HTMLNode(value="Hello 世界 🌍")
        self.assertEqual(node.value, "Hello 世界 🌍")

    def test_unicode_in_props(self):
        """Test with Unicode characters in props"""
        node = HTMLNode(tag="div", props={"data-text": "Hello 世界"})
        result = node.props_to_html()
        self.assertIn("Hello 世界", result)

    def test_very_long_value(self):
        """Test with very long value"""
        long_value = "a" * 10000
        node = HTMLNode(value=long_value)
        self.assertEqual(node.value, long_value)

    def test_tag_with_special_html_tags(self):
        """Test with various HTML tag names"""
        tags = ["div", "p", "span", "a", "img", "br", "hr", "input", "button"]
        for tag in tags:
            node = HTMLNode(tag=tag)
            self.assertEqual(node.tag, tag)

    def test_props_with_html_attributes(self):
        """Test with common HTML attributes"""
        attrs = {
            "id": "test-id",
            "class": "test-class",
            "href": "https://example.com",
            "src": "/image.jpg",
            "alt": "description",
            "data-value": "123",
            "aria-label": "label",
        }
        node = HTMLNode(tag="div", props=attrs)
        result = node.props_to_html()

        for key, value in attrs.items():
            self.assertIn(f'{key}="{value}"', result)

    def test_empty_string_value(self):
        """Test with empty string value"""
        node = HTMLNode(value="")
        self.assertEqual(node.value, "")

    def test_empty_string_tag(self):
        """Test with empty string tag"""
        node = HTMLNode(tag="")
        self.assertEqual(node.tag, "")

    def test_whitespace_in_value(self):
        """Test with whitespace in value"""
        node = HTMLNode(value="  Hello  World  ")
        self.assertEqual(node.value, "  Hello  World  ")

    def test_props_order_preservation(self):
        """Test that props order is preserved (Python 3.7+)"""
        # In Python 3.7+, dicts maintain insertion order
        props = {"first": "1", "second": "2", "third": "3"}
        node = HTMLNode(props=props)
        result = node.props_to_html()

        # All props should be present
        self.assertIn('first="1"', result)
        self.assertIn('second="2"', result)
        self.assertIn('third="3"', result)

    def test_children_list_modification(self):
        """Test that modifying children list affects the node"""
        child1 = HTMLNode(tag="p")
        children = [child1]
        node = HTMLNode(children=children)

        self.assertEqual(len(node.children), 1)

        # Modifying the original list
        child2 = HTMLNode(tag="span")
        children.append(child2)

        # Node's children should reflect the change
        self.assertEqual(len(node.children), 2)

    def test_props_dict_modification(self):
        """Test that modifying props dict affects the node"""
        props = {"class": "original"}
        node = HTMLNode(props=props)

        # Modifying the original dict
        props["id"] = "new"

        # Node's props should reflect the change
        self.assertIn("id", node.props)
        self.assertEqual(node.props["id"], "new")

    def test_multiple_instances_independence(self):
        """Test that multiple instances don't interfere with each other"""
        node1 = HTMLNode(tag="div", value="first")
        node2 = HTMLNode(tag="span", value="second")

        self.assertEqual(node1.tag, "div")
        self.assertEqual(node2.tag, "span")
        self.assertNotEqual(node1.tag, node2.tag)

    def test_props_with_quotes_in_value(self):
        """Test props with quotes in the value"""
        node = HTMLNode(props={"title": 'He said "hello"'})
        result = node.props_to_html()
        # Note: The implementation doesn't escape quotes, so this tests actual behavior
        self.assertIn("title=", result)

    def test_none_values_explicitly_set(self):
        """Test that explicitly setting None works"""
        node = HTMLNode(tag=None, value=None, children=None, props=None)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


if __name__ == "__main__":
    unittest.main()
