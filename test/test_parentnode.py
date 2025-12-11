import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    """Comprehensive test suite for ParentNode class"""

    # Initialization Tests
    def test_init_basic(self):
        """Test creating a basic parent node"""
        child = LeafNode("p", "Child content")
        node = ParentNode("div", [child])
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertIsNone(node.props)

    def test_init_with_props(self):
        """Test creating a parent node with props"""
        child = LeafNode("p", "Content")
        props = {"class": "container", "id": "main"}
        node = ParentNode("div", [child], props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.props, props)

    def test_init_multiple_children(self):
        """Test creating a parent node with multiple children"""
        child1 = LeafNode("p", "First")
        child2 = LeafNode("p", "Second")
        child3 = LeafNode("p", "Third")
        node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(len(node.children), 3)

    def test_init_empty_children_list(self):
        """Test creating a parent node with empty children list"""
        node = ParentNode("div", [])
        self.assertEqual(len(node.children), 0)

    def test_init_empty_props_dict(self):
        """Test creating a parent node with empty props dict"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child], {})
        self.assertEqual(node.props, {})

    def test_init_value_not_set(self):
        """Test that value is not set (ParentNode doesn't use value)"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child])
        self.assertIsNone(node.value)

    def test_inheritance_from_htmlnode(self):
        """Test that ParentNode inherits from HTMLNode"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child])
        self.assertIsInstance(node, HTMLNode)
        self.assertIsInstance(node, ParentNode)

    # to_html Tests - Success Cases
    def test_to_html_single_child(self):
        """Test to_html with single child"""
        child = LeafNode("p", "Hello")
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div><p>Hello</p></div>")

    def test_to_html_multiple_children(self):
        """Test to_html with multiple children"""
        child1 = LeafNode("p", "First")
        child2 = LeafNode("p", "Second")
        node = ParentNode("div", [child1, child2])
        expected = "<div><p>First</p><p>Second</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_nested_parent_nodes(self):
        """Test to_html with nested parent nodes"""
        grandchild = LeafNode("span", "Text")
        child = ParentNode("p", [grandchild])
        parent = ParentNode("div", [child])
        expected = "<div><p><span>Text</span></p></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_deeply_nested(self):
        """Test to_html with deeply nested structure"""
        leaf = LeafNode("b", "Bold")
        level3 = ParentNode("span", [leaf])
        level2 = ParentNode("p", [level3])
        level1 = ParentNode("div", [level2])
        expected = "<div><p><span><b>Bold</b></span></p></div>"
        self.assertEqual(level1.to_html(), expected)

    def test_to_html_mixed_children(self):
        """Test to_html with mixed LeafNode and ParentNode children"""
        leaf1 = LeafNode("p", "Paragraph")
        leaf2 = LeafNode("span", "Span")
        inner_parent = ParentNode("div", [leaf2])
        parent = ParentNode("section", [leaf1, inner_parent])
        expected = "<section><p>Paragraph</p><div><span>Span</span></div></section>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_empty_children_list(self):
        """Test to_html with empty children list"""
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_various_tags(self):
        """Test to_html with various HTML tags"""
        tags = [
            "div",
            "section",
            "article",
            "main",
            "header",
            "footer",
            "nav",
            "ul",
            "ol",
        ]
        for tag in tags:
            child = LeafNode("p", "Content")
            node = ParentNode(tag, [child])
            expected = f"<{tag}><p>Content</p></{tag}>"
            self.assertEqual(node.to_html(), expected)

    def test_to_html_list_structure(self):
        """Test to_html creating a list structure"""
        item1 = LeafNode("li", "Item 1")
        item2 = LeafNode("li", "Item 2")
        item3 = LeafNode("li", "Item 3")
        ul = ParentNode("ul", [item1, item2, item3])
        expected = "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        self.assertEqual(ul.to_html(), expected)

    def test_to_html_table_structure(self):
        """Test to_html creating a simple table structure"""
        cell1 = LeafNode("td", "Cell 1")
        cell2 = LeafNode("td", "Cell 2")
        row = ParentNode("tr", [cell1, cell2])
        table = ParentNode("table", [row])
        expected = "<table><tr><td>Cell 1</td><td>Cell 2</td></tr></table>"
        self.assertEqual(table.to_html(), expected)

    def test_to_html_complex_nested_structure(self):
        """Test to_html with complex nested structure"""
        # Create: <div><p><b>Bold</b> and <i>Italic</i></p><span>End</span></div>
        bold = LeafNode("b", "Bold")
        italic = LeafNode("i", "Italic")
        text = LeafNode(None, " and ")
        p = ParentNode("p", [bold, text, italic])
        span = LeafNode("span", "End")
        div = ParentNode("div", [p, span])
        expected = "<div><p><b>Bold</b> and <i>Italic</i></p><span>End</span></div>"
        self.assertEqual(div.to_html(), expected)

    def test_to_html_many_children(self):
        """Test to_html with many children"""
        children = [LeafNode("p", f"Paragraph {i}") for i in range(10)]
        node = ParentNode("div", children)
        result = node.to_html()
        self.assertTrue(result.startswith("<div>"))
        self.assertTrue(result.endswith("</div>"))
        for i in range(10):
            self.assertIn(f"<p>Paragraph {i}</p>", result)

    def test_to_html_unicode_content(self):
        """Test to_html with Unicode content in children"""
        child = LeafNode("p", "Hello 世界 🌍")
        node = ParentNode("div", [child])
        expected = "<div><p>Hello 世界 🌍</p></div>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_preserves_child_order(self):
        """Test that to_html preserves order of children"""
        children = [
            LeafNode("h1", "Title"),
            LeafNode("p", "First paragraph"),
            LeafNode("p", "Second paragraph"),
            LeafNode("footer", "Footer"),
        ]
        node = ParentNode("article", children)
        result = node.to_html()

        # Check order by finding positions
        h1_pos = result.find("<h1>")
        p1_pos = result.find("<p>First")
        p2_pos = result.find("<p>Second")
        footer_pos = result.find("<footer>")

        self.assertTrue(h1_pos < p1_pos < p2_pos < footer_pos)

    # to_html Tests - Error Cases
    def test_to_html_none_tag_raises_error(self):
        """Test that to_html raises ValueError when tag is None"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child])
        node.tag = None
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("missing tag attribute", str(context.exception))

    def test_to_html_none_children_raises_error(self):
        """Test that to_html raises ValueError when children is None"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child])
        node.children = None
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertIn("missing children attribute", str(context.exception))

    def test_to_html_none_tag_with_props(self):
        """Test that error is raised even with props"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child], {"class": "test"})
        node.tag = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_none_children_with_props(self):
        """Test that error is raised even with props"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child], {"class": "test"})
        node.children = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_child_raises_not_implemented(self):
        """Test behavior when child's to_html raises NotImplementedError"""
        raw_htmlnode = HTMLNode(tag="p", value="test")
        node = ParentNode("div", [raw_htmlnode])
        with self.assertRaises(NotImplementedError):
            node.to_html()

    # Props Integration Tests (inherited from HTMLNode)
    def test_props_to_html_inherited(self):
        """Test that props_to_html method is inherited"""
        child = LeafNode("p", "Content")
        props = {"class": "container", "id": "main"}
        node = ParentNode("div", [child], props)
        result = node.props_to_html()
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)

    def test_props_to_html_none_props(self):
        """Test props_to_html with no props"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child])
        self.assertEqual(node.props_to_html(), "")

    # Note: ParentNode doesn't override to_html to use props
    def test_to_html_ignores_props(self):
        """Test that to_html doesn't include props in output"""
        child = LeafNode("p", "Content")
        props = {"class": "test", "id": "main"}
        node = ParentNode("div", [child], props)
        result = node.to_html()
        # Current implementation doesn't use props in to_html
        self.assertEqual(result, "<div><p>Content</p></div>")
        self.assertNotIn("class", result)
        self.assertNotIn("id", result)

    # __repr__ Tests (inherited from HTMLNode)
    def test_repr_basic(self):
        """Test string representation"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child])
        result = repr(node)
        self.assertIn("ParentNode", result)
        self.assertIn("div", result)

    def test_repr_with_props(self):
        """Test string representation with props"""
        child = LeafNode("p", "Content")
        props = {"class": "test"}
        node = ParentNode("div", [child], props)
        result = repr(node)
        self.assertIn("ParentNode", result)
        self.assertIn("class", result)

    def test_repr_multiple_children(self):
        """Test string representation with multiple children"""
        child1 = LeafNode("p", "First")
        child2 = LeafNode("p", "Second")
        node = ParentNode("div", [child1, child2])
        result = repr(node)
        self.assertIn("ParentNode", result)

    # Edge Cases
    def test_empty_tag_string(self):
        """Test with empty string tag"""
        child = LeafNode("p", "Content")
        node = ParentNode("", [child])
        self.assertEqual(node.to_html(), "<><p>Content</p></>")

    def test_child_with_none_tag(self):
        """Test parent with child that has None tag (raw text)"""
        child = LeafNode(None, "Plain text")
        node = ParentNode("div", [child])
        self.assertEqual(node.to_html(), "<div>Plain text</div>")

    def test_multiple_children_with_none_tags(self):
        """Test parent with multiple text-only children"""
        child1 = LeafNode(None, "Hello ")
        child2 = LeafNode(None, "World")
        node = ParentNode("p", [child1, child2])
        self.assertEqual(node.to_html(), "<p>Hello World</p>")

    def test_alternating_parent_leaf_nodes(self):
        """Test alternating parent and leaf nodes"""
        leaf1 = LeafNode("b", "Bold")
        inner1 = ParentNode("span", [leaf1])
        leaf2 = LeafNode("i", "Italic")
        inner2 = ParentNode("span", [leaf2])
        parent = ParentNode("div", [inner1, leaf2, inner2])
        expected = (
            "<div><span><b>Bold</b></span><i>Italic</i><span><i>Italic</i></span></div>"
        )
        self.assertEqual(parent.to_html(), expected)

    def test_multiple_levels_of_nesting(self):
        """Test multiple levels of parent node nesting"""
        leaf = LeafNode("text", "content")
        level1 = ParentNode("p", [leaf])
        level2 = ParentNode("div", [level1])
        level3 = ParentNode("section", [level2])
        level4 = ParentNode("article", [level3])
        level5 = ParentNode("main", [level4])

        result = level5.to_html()
        self.assertTrue(result.startswith("<main>"))
        self.assertTrue(result.endswith("</main>"))
        self.assertIn("<text>content</text>", result)

    def test_sibling_parent_nodes(self):
        """Test multiple parent nodes as siblings"""
        leaf1 = LeafNode("p", "First")
        leaf2 = LeafNode("p", "Second")
        parent1 = ParentNode("div", [leaf1])
        parent2 = ParentNode("div", [leaf2])
        grandparent = ParentNode("section", [parent1, parent2])

        expected = "<section><div><p>First</p></div><div><p>Second</p></div></section>"
        self.assertEqual(grandparent.to_html(), expected)

    def test_modifying_children_after_creation(self):
        """Test modifying children list after creation"""
        child1 = LeafNode("p", "First")
        children = [child1]
        node = ParentNode("div", children)

        self.assertEqual(node.to_html(), "<div><p>First</p></div>")

        # Add another child
        child2 = LeafNode("p", "Second")
        children.append(child2)

        # Node should reflect the change
        self.assertEqual(node.to_html(), "<div><p>First</p><p>Second</p></div>")

    def test_modifying_tag_after_creation(self):
        """Test modifying tag after creation"""
        child = LeafNode("p", "Content")
        node = ParentNode("div", [child])

        self.assertEqual(node.to_html(), "<div><p>Content</p></div>")

        node.tag = "section"
        self.assertEqual(node.to_html(), "<section><p>Content</p></section>")

    def test_modifying_child_after_parent_creation(self):
        """Test modifying child content after parent creation"""
        child = LeafNode("p", "Original")
        node = ParentNode("div", [child])

        self.assertEqual(node.to_html(), "<div><p>Original</p></div>")

        # Modify child
        child.value = "Modified"
        self.assertEqual(node.to_html(), "<div><p>Modified</p></div>")

    def test_multiple_instances_independence(self):
        """Test that multiple instances don't interfere"""
        child1 = LeafNode("p", "First")
        child2 = LeafNode("p", "Second")
        node1 = ParentNode("div", [child1])
        node2 = ParentNode("section", [child2])

        self.assertEqual(node1.to_html(), "<div><p>First</p></div>")
        self.assertEqual(node2.to_html(), "<section><p>Second</p></section>")

    def test_common_html_structures(self):
        """Test common HTML structures"""
        # Navigation menu
        link1 = LeafNode("a", "Home")
        link2 = LeafNode("a", "About")
        nav = ParentNode("nav", [link1, link2])
        self.assertIn("<nav>", nav.to_html())

        # Ordered list
        item1 = LeafNode("li", "First")
        item2 = LeafNode("li", "Second")
        ol = ParentNode("ol", [item1, item2])
        self.assertEqual(ol.to_html(), "<ol><li>First</li><li>Second</li></ol>")

    def test_case_sensitive_tags(self):
        """Test that tags are case-sensitive"""
        child = LeafNode("p", "Content")
        node_lower = ParentNode("div", [child])

        child2 = LeafNode("p", "Content")
        node_upper = ParentNode("DIV", [child2])

        self.assertEqual(node_lower.to_html(), "<div><p>Content</p></div>")
        self.assertEqual(node_upper.to_html(), "<DIV><p>Content</p></DIV>")

    def test_whitespace_preservation(self):
        """Test that whitespace in children is preserved"""
        child1 = LeafNode("p", "  Leading spaces")
        child2 = LeafNode("p", "Trailing spaces  ")
        child3 = LeafNode("p", "  Both  ")
        node = ParentNode("div", [child1, child2, child3])

        result = node.to_html()
        self.assertIn("<p>  Leading spaces</p>", result)
        self.assertIn("<p>Trailing spaces  </p>", result)
        self.assertIn("<p>  Both  </p>", result)

    def test_props_modification_after_creation(self):
        """Test modifying props after creation"""
        child = LeafNode("p", "Content")
        props = {"class": "original"}
        node = ParentNode("div", [child], props)

        # Modify props
        node.props["class"] = "modified"
        node.props["id"] = "new"

        result = node.props_to_html()
        self.assertIn('class="modified"', result)
        self.assertIn('id="new"', result)

    def test_recursive_structure_integrity(self):
        """Test that recursive structure maintains integrity"""
        # Create: div > section > article > p > span > text
        text = LeafNode(None, "Deep text")
        span = ParentNode("span", [text])
        p = ParentNode("p", [span])
        article = ParentNode("article", [p])
        section = ParentNode("section", [article])
        div = ParentNode("div", [section])

        expected = "<div><section><article><p><span>Deep text</span></p></article></section></div>"
        self.assertEqual(div.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
