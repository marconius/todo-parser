from xml.etree.ElementTree import TreeBuilder, dump


def build_tree(element, builder):
    builder.start(element.tag)
    if not len(element.children):
        builder.data(element.text)
    for child in element.children:
        build_tree(child, builder)
    return builder.end(element.tag)


class ElementTree:
    def __init__(self, root='html'):
        self.root = Element(tag=root)

    def build(self):
        builder = TreeBuilder()
        return build_tree(self.root, builder)


class Element:
    def __init__(self, tag='html'):
        self.tag = tag
        self.children = []

    def __repr__(self):
        text = getattr(self, 'text', None)
        return "<Element tag=%s, text=%s>" % (self.tag, text)

    def append(self, el):
        self.children.append(el)
