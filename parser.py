import re
from dom import Node, text, element

class Parser(object):
    # The parser stores its input string and a current position within the string.
    # The position is the index of the next character we haven't processed yet.
    def __init__(self, pos, input):
        self.pos = pos  #postition of already read character
        self.input = input  #input string to read

    def next_char(self):
        # Read the current character without consuming it.
        return self.input[self.pos]

    def consume_char(self):
        if (self.pos >= len(self.input)):
            ret_char = self.input[len(self.input) - 1]
            self.pos = len(self.input)
        else:
        # consume the next character
            ret_char = self.input[self.pos]
            self.pos += 1

        return ret_char

    def starts_with(self, start_string):
        # Do the next characters start with the given string?
        return self.input.startswith(start_string, self.pos)

    def eof(self):
        # // Return true if all input is consumed.
        if (self.pos >= len(self.input)): return True
        else: return False

    def consume_while(self, test_expression):
        # Consume characters until `test` returns false.
        ret_string = ''
        while (not self.eof()) and (test_expression.match(self.next_char())):
            ret_string += self.consume_char()
        return ret_string

    def consume_whitespace(self):
        # Consume and discard zero or more whitespace characters.
        test_expression = re.compile('[ ]')
        ret = self.consume_while(test_expression)
        return ret

    def parse_tag_name(self):
        # Parse a tag or attribute name.
        test_expression = re.compile('[0-9a-zA-Z]')
        return self.consume_while(test_expression)

    def parse_text(self):
        # returns NODE-TYPE TEXT
        test_expression = re.compile('[^<]')
        data = self.consume_while(test_expression)
        return text(data)

    def parse_element(self):
        # returns NODE-TYPE ELEMENT
        # Opening Tag
        assert(self.consume_char() == '<')
        tag_name = self.parse_tag_name()
        attributes = self.parse_attributes()
        assert(self.consume_char() == '>')

        # get all the children of the node
        children = self.parse_nodes()

        # Closing tag.
        assert(self.consume_char() == '<')
        assert(self.consume_char() == '/')
        assert(self.parse_tag_name() == tag_name)
        assert(self.consume_char() == '>')

        return element(name=tag_name, attributes=attributes, children=children)

    def parse_attr(self):
        # Parse a single name="value" pair.
        name = self.parse_tag_name()
        assert(self.consume_char() == '=')
        value = self.parse_attr_value()
        return(name, value)

    def parse_attr_value(self):
        # Parse a quoted value.
        test_expression = re.compile('[0-9a-zA-Z]')
        open_quote = self.consume_char()
        assert(open_quote == '"' or open_quote == '\'')
        value = self.consume_while(test_expression)
        # assert(self.consume_char() == open_quote)
        if (self.next_char() == open_quote):
            self.consume_char()
        else:
            raise("Closing Quote Not Found")
        return value

    def parse_attributes(self):
        # Parse a list of name="value" pairs, separated by whitespace.
        attr = {}
        do_parse = True
        while (True):
            self.consume_whitespace()
            if (self.next_char() == '>'):
                do_parse = False
                break
            (name, value) = self.parse_attr()
            attr[name] = value

        return attr

    def parse_node(self):
        # Parse a single node.
        if self.next_char() == "<":
            return self.parse_element()
        else:
            return self.parse_text()

    def parse_nodes(self):
        # Parse a sequence of sibling nodes.
        nodes = []
        do_parse = True
        while (do_parse):
            self.consume_whitespace()
            if (self.eof() or self.starts_with("</")):
                do_parse = False
                break
            nodes.append(self.parse_node())
        print(nodes)
        return nodes

def parse(source):
    print (f'STARTING: {source}')
    nodes = Parser(pos= 0, input= source).parse_nodes()
    print (nodes)

if __name__ == '__main__':
    test = [
        ' <html> <body><h1>Title</h1><div id="main" class="test"><p>Hello <em>world</em>!</p></div></body></html>',
        '<html><body><div id="main" class="test"><p>Hello <em>world</em>!</p></div></body></html>',
        '<html><body><h1>Title</h1></body></html>',
        '<html><body></body></html>'
    ]
    for t in test:
        parse(t)
