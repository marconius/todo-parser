import re

from .element_tree import Element, ElementTree


class Parser:
    """ A Parser object takes rules

        The first rule in the list will be considered THE start rule (TODO: revise this statement)
        Rules will tried sequentially
    """
    def __init__(self, rules=[]):
        self.rules = rules

    def parse(self, expression, start=True, root='html'):
        tree = ElementTree(root)

        tail = expression

        if start:
            rule = self.rules[0]
            match = rule.search(expression)
        else:
            for rule in self.rules:
                match = rule.search(expression)
                if match:
                    break

        if match:
            text = match.groupdict()['text']

            # parse content of this node
            e = Element(tag=rule.tag_name)
            sub_tree = self.parse(text, start=False, root=rule.tag_name)
            if sub_tree.root.children:
                e.children = sub_tree.root.children
            else:
                e.text = text
            tree.root.children.append(e)

            # parse remainder
            tail = tail[match.end():] if match else None
            if tail:
                sub_tree2 = self.parse(tail, start=False) if tail else None
                if sub_tree2:
                    tree.root.children.extend(sub_tree2.root.children)

        return tree

    @classmethod
    def get_todo_parser(cls):
        section_rule = Rule(r'(?P<text>==.*==\n(\*.*\n)+)\n', 'section')
        header_rule = Rule(r'==(?P<text>.*)==', 'h2')
        list_rule = Rule(r'(?P<text>(\*.*\n)+)\n', 'ol')
        item_rule = Rule(r'\* (?P<text>.*)\n', 'li')

        return cls([
            section_rule,
            header_rule,
            list_rule,
            item_rule
        ])


class Rule:
    def __init__(self, pattern, tag_name):
        self.pattern = pattern
        self.tag_name = tag_name
        self.regex = re.compile(self.pattern, flags=re.MULTILINE)

    def __repr__(self):
        return "<Rule pattern=%s, tag=%s>" % (self.pattern, self.tag_name)

    def search(self, expression):
        return self.regex.search(expression)
