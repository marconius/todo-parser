from unittest import TestCase

from todo_parser.element_tree import ElementTree
from todo_parser.parser import Parser, Rule


class ParserTestCase(TestCase):
    def setUp(self):
        self.section_rule = Rule(r'(?P<text>==.*==\n(\*.*\n)+)\n', 'section')
        self.header_rule = Rule(r'==(?P<text>.*)==', 'h2')
        list_rule = Rule(r'(?P<text>(\*.*\n)+)\n', 'ol')
        item_rule = Rule(r'\* (?P<text>.*)\n', 'li')

        self.parser = Parser([
            self.section_rule,
            self.header_rule,
            list_rule,
            item_rule
        ])

    # Integration

    def test_integration(self):
        tree = self.parser.parse(
            "== Fix a bug ==\n"
            "* Understand bug report\n"
            "* Write code\n"
            "* Test\n"
            "\n"
            "== WIP: QA ==\n"
            "* Verify fix in beta cluster\n"
            "* Resolve Bug?\n"
            "* Something more?\n"
            "\n"
        )

        self.assertEqual(len(tree.root.children), 2)
        self.assertEqual(len(tree.root.children[0].children), 4)
        self.assertEqual(len(tree.root.children[1].children), 4)
        xml_root = tree.build()
        from xml.etree import ElementTree as ET
        self.assertEqual(ET.tostring(xml_root), '<html />')
        # import ipdb; ipdb.set_trace()

    # Rules

    def test_rule(self):
        match = self.header_rule.search("== Section 1 ==")

        self.assertEqual(match.groupdict()['text'], " Section 1 ")

    # Parser

    def test_parse_an_empty_expression(self):
        tree = Parser([Rule('__(?P<text>.*)__', 'em')]).parse("")

        self.assertIsInstance(tree, ElementTree)
        self.assertEqual(tree.root.children, [])

    def test_parser_rule(self):
        parser = Parser(rules=[self.header_rule])

        tree = parser.parse("==Section 1==")

        self.assertEqual(tree.root.children[0].tag, 'h2')
        self.assertEqual(tree.root.children[0].text, "Section 1")

    def test_parser_with_multiple_lines(self):
        parser = Parser([self.header_rule])
        tree = parser.parse(
            "\n"
            "==Section 2=="
        )

        self.assertEqual(tree.root.children[0].text, "Section 2")

    def test_parser_with_multiple_matching(self):
        parser = Parser([self.header_rule])
        tree = parser.parse(
            "==Section 3==\n"
             "\n"
             "==Section 4=="
        )

        self.assertEqual(tree.root.children[0].text, "Section 3")
        self.assertEqual(tree.root.children[1].text, "Section 4")

    def test_parser_recursion(self):
        # parser = Parser([self.section_rule, self.header_rule])
        parser = Parser([Rule('(?P<text>==.*==)\n', 'section'), self.header_rule])
        todo_markdown = (
            "==Section 5==\n"
            "==Section 6==\n"
        )

        tree = parser.parse(todo_markdown)


        self.assertEqual(tree.root.children[0].tag, 'section')
        self.assertEqual(tree.root.children[0].children[0].tag, 'h2')
        self.assertEqual(tree.root.children[0].children[0].text, 'Section 5')
        # import ipdb; ipdb.set_trace()
        self.assertEqual(tree.root.children[1].children[0].text, 'Section 6')
