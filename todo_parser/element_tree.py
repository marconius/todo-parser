from xml.etree.ElementTree import TreeBuilder, dump


class ElementTree:
    def __init__(self, root='html'):
        self.root = Element(tag=root)

    def build(self):
        builder = TreeBuilder()

        builder.start(self.root.tag)
        builder.end(self.root.tag)
        return builder.close()


class Element:
    def __init__(self, tag='html'):
        self.tag = tag
        self.children = []

    def __repr__(self):
        text = getattr(self, 'text', None)
        return "<Element tag=%s, text=%s>" % (self.tag, text)

    def append(self, el):
        self.children.append(el)
