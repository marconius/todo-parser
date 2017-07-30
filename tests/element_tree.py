from unittest import TestCase

from todo_parser.element_tree import Element, ElementTree


class ElementTestCase(TestCase):
    def setUp(self):
        pass

    def test_element_tag_is_html(self):
        element = Element()

        self.assertEqual(element.tag, 'html')

    def test_children(self):
        element = Element('section')
        element2 = Element('h2')

        element.append(element2)

        self.assertEqual(element.children[0], element)


class ElementTreeTestCase(TestCase):
    def test_root_is_a_list(self):
        tree = ElementTree()

        self.assertEqual(tree.root, [])
        # self.assertEqual(tree.root.tag, 'html')

    def test_element_set_text(self):
        e = Element(tag="dd")
        str = 'content is here'

        e.text = str

        self.assertEqual(e.text, str)

    def test_root(self):
        tree = ElementTree()
        element = Element('section')
        tree.root.append(element)

        self.assertEqual(tree.root[0], element)
