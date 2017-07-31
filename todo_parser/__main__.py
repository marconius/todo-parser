import argparse
import sys
from xml.etree import ElementTree as ET

from .parser import Parser


def cli():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--toHtml', help="markup file")

    namespace = arg_parser.parse_args(sys.argv[1:])

    with open(namespace.toHtml, 'r') as f:
        markup = f.read()

    parser = Parser.get_todo_parser()
    tree = parser.parse(markup)
    xml_root = tree.build()

    ET.dump(xml_root)


if __name__ == "__main__":
    cli()
