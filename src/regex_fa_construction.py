import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

from discrete_event import *
from common import empty_chars, Kind


class RegexFaConstruction:

    def __init__(self, name='NFA'):
        self.name = name
        self.m = DiscreteEvent(name)
        logging.info('Initialize a new NFA {}'.format(name))
        self.input_port = 'Input'
        self.output_port = 'Output'
        self.m.input_port(self.input_port, latency=1)
        self.m.output_port(self.output_port, latency=1)
        self.state = {}
        self._matched_str = None
        self._matched_index = 0

    def extend_nodes(self, nodes: list):
        """ Add nodes to the current NFA """
        logging.info('NFA {} adds nodes {}'.format(self.name, nodes))
        for node in nodes:
            if not isinstance(node, Node):
                raise TypeError('The type of element in list must be Node type')
        self.m.nodes.extend(nodes)

    def get_node_list(self):
        """ Get nodes list of current NFA """
        return self.m.nodes

    def get_input_node(self):
        """ Find the input node of NFA """
        for node in self.m.nodes:
            if self.input_port in node.inputs:
                logging.info('NFA {} gets its input node: {}'.format(self.name, node))
                return node
        return None

    def set_input_node(self, new_name: str, latency=1):
        """ Change the input port of the input node """
        for node in self.m.nodes:
            if self.input_port in node.inputs:
                node.inputs.pop(self.input_port)
                node.inputs[new_name] = latency
                logging.info('NFA {} rename the input port of its input node to {}'.format(self.name, new_name))

    def get_output_node(self):
        """ Find the output node of NFA """
        for node in self.m.nodes:
            if self.output_port in node.outputs:
                logging.info('NFA {} gets its output node: {}'.format(self.name, node))
                return node
        return None

    def set_output_node(self, new_name: str, latency=1):
        """ Change the output port of the input node """
        for node in self.m.nodes:
            if self.output_port in node.outputs:
                node.outputs.pop(self.output_port)
                node.outputs[new_name] = latency
                logging.info('NFA {} rename the input port of its input node to {}'.format(self.name, new_name))

    def add_da_node(self, a: str, b: str, c=None):
        """ Add nodes that recognize letters, numbers, and underscores.
        Corresponding to the regular expression of '\w' """

        def function(text):
            if text is None or len(text) < 1: return None
            if text[0].isdigit() or text[0].isalpha() or text[0] == '_':
                return text[1:] if len(text) else ''
            else:
                return None

        n = self.m.add_node('digit_alpha', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        if c is not None:
            n.output(c, latency=1)
            logging.info(r'NFA {} adds a "\w" node. input port: {} output port: {}, {}'.format(self.name, a, b, c))
        else:
            logging.info(r'NFA {} adds a "\w" node. input port: {} output port: {}'.format(self.name, a, b))

    def add_empty_char_node(self, a: str, b: str, c=None):
        """ Add nodes that recognize '\n', '\t', '\r' and '\f'.
        Corresponding to the regular expression of '\s' """

        def function(text):
            if text is None or len(text) < 1: return None
            if text[0] in empty_chars:
                return text[1:] if len(text) else ''
            else:
                return None

        n = self.m.add_node('empty_char', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        if c is not None:
            n.output(c, latency=1)
            logging.info(r'NFA {} adds a "\s" node. input port: {} output port: {}, {}'.format(self.name, a, b, c))
        else:
            logging.info(r'NFA {} adds a "\s" node. input port: {} output port: {}'.format(self.name, a, b))

    def add_digit_node(self, a: str, b: str, c=None):
        """ Add nodes that recognize numbers.
        Corresponding to the regular expression of '\d' """

        def function(text):
            if text is None or len(text) < 1: return None
            if text[0].isdigit():
                return text[1:] if len(text) else ''
            else:
                return None

        n = self.m.add_node('digit', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        if c is not None:
            n.output(c, latency=1)
            logging.info(r'NFA {} adds a "\d" node. input port: {} output port: {}, {}'.format(self.name, a, b, c))
        else:
            logging.info(r'NFA {} adds a "\d" node. input port: {} output port: {}'.format(self.name, a, b))

    def add_alpha_node(self, a: str, b: str, c=None):
        """ Add nodes that recognize letters. """

        def function(text):
            if text is None or len(text) < 1: return None
            if text[0].isalpha():
                return text[1:] if len(text) else ''
            else:
                return None

        n = self.m.add_node('alpha', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        if c is not None:
            n.output(c, latency=1)
            logging.info(r'NFA {} adds an "alpha" node. input port: {} output port: {}, {}'.format(self.name, a, b, c))
        else:
            logging.info(r'NFA {} adds an "alpha" node. input port: {} output port: {}'.format(self.name, a, b))

    def add_any_node(self, a: str, b: str, c=None):
        """ Add a node that can accept any input except for '\n'.
        Corresponding to the regular expression of '.' """

        def function(text):
            if text is None or len(text) < 1: return None
            if text[0] != '\n':
                return text[1:] if len(text) else ''
            else:
                return None

        n = self.m.add_node('any', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        if c is not None:
            n.output(c, latency=1)
            logging.info(r'NFA {} adds a "." node. input port: {} output port: {}, {}'.format(self.name, a, b, c))
        else:
            logging.info(r'NFA {} adds a "." node. input port: {} output port: {}'.format(self.name, a, b))

    def add_normal_node(self, a: str, b: str, pattern_char: str, c=None):
        """ Add a node that can recognize the specified character """

        if len(pattern_char) > 1: pattern_char = pattern_char[0]

        def normal_function(text):
            if text is None or len(text) < 1: return None
            if text[0] == pattern_char:
                return text[1:] if len(text) else ''
            else:
                return None

        n = self.m.add_node('normal', lambda text: normal_function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        if c is not None:
            n.output(c, latency=1)
            logging.info(r'NFA {} adds a "normal" node. pattern char: {} input port: {} output port: {}, {}'.format(self.name, pattern_char, a, b, c))
        else:
            logging.info(r'NFA {} adds a "normal" node. pattern char: {} input port: {} output port: {}'.format(self.name, pattern_char, a, b))

    def add_charset_node(self, a: str, b: str, charset: list, negative: bool, c=None):
        """ Adds a node that recognizes the specified character set.
         Corresponding to the regular expression of '[]' """

        def function(text):
            if text is None or len(text) < 1: return None
            # if (not negative and (text[0] in charset)) or (negative and (text[0] not in charset)):
            #     self._match_lst.append(text[0])
            #     return text[1:] if len(text) else ''
            # else:
            #     return None
            for token in charset:
                if token.get('type') == Kind.NORMAL:
                    if token.get('value') == text[0]:
                        return (text[1:] if len(text) else '') if not negative else None
                elif token.get('type') == Kind.TRANS:
                    if token.get('value') == 'w':
                        if text[0].isalpha() or text[0].isdigit() or text[0] == '_':
                            return (text[1:] if len(text) else '') if not negative else None
                    elif token.get('value') == 's':
                        if text[0] in empty_chars:
                            return (text[1:] if len(text) else '') if not negative else None
                    else:
                        if text[0].isdigit():
                            return (text[1:] if len(text) else '') if not negative else None
                elif token.get('type') == Kind.ALPHA_RANGE:
                    if not text[0].isalpha(): continue
                    l, r = token.get(Kind.RANGE)[0], token.get(Kind.RANGE)[1]
                    if l <= text[0] <= r:
                        return (text[1:] if len(text) else '') if not negative else None
                else:
                    if not text[0].isdigit(): continue
                    l, r = token.get(Kind.RANGE)[0], token.get(Kind.RANGE)[1]
                    if l <= int(text[0]) <= r:
                        return (text[1:] if len(text) else '') if not negative else None
            return (text[1:] if len(text) else '') if negative else None

        node_name = Kind.SET if not negative else Kind.NEG_SET
        n = self.m.add_node(node_name, lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        if c is not None:
            n.output(c, latency=1)
            logging.info(r'NFA {} adds a "charset" node. pattern char: {} input port: {} output port: {}, {}'.format(self.name, charset, a, b, c))
        else:
            logging.info(r'NFA {} adds a "charset" node. pattern char: {} input port: {} output port: {}'.format(self.name, charset, a, b))

    def add_end_node(self, a: str, b: str):
        """ Add a node that can recognize the end of text """

        def function(text):
            return '' if text == '' else None

        n = self.m.add_node('end', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        logging.info(r'NFA {} adds an "end" node. input port: {} output port: {}'.format(self.name, a, b))

    def add_all_node(self, a: str, b: str, c=None):
        """ Add a node that can recognize any input. """

        def function(text):
            if text is None or len(text) < 1: return None
            return text[1:] if len(text) else ''

        n = self.m.add_node('all', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        if c is not None:
            n.output(c, latency=1)
            logging.info(r'NFA {} adds an "all" node. input port: {} output port: {}, {}'.format(self.name, a, b, c))
        else:
            logging.info(r'NFA {} adds an "all" node. input port: {} output port: {}'.format(self.name, a, b))

    def add_null_11_node(self, a: str, b: str):
        """ Add an null node that has one input and one output """

        def function(text):
            return text

        n = self.m.add_node('null_11', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        logging.info(r'NFA {} adds a "null" node. input port: {} output port: {}'.format(self.name, a, b))

    def add_null_12_node(self, a: str, b: str, c: str):
        """ Add an null node that has one input and two outputs """

        def function(text):
            return text

        n = self.m.add_node('null_12', lambda text: function(text))
        n.input(a, latency=1)
        n.output(b, latency=1)
        n.output(c, latency=1)
        logging.info(r'NFA {} adds a "null" node. input port: {} output port: {}, {}'.format(self.name, a, b, c))

    def add_null_21_node(self, a: str, b: str, c: str):
        """ Add an null node that has two inputs and one output """

        def function(text):
            return text

        n = self.m.add_node('null_21', lambda text: function(text))
        n.input(a, latency=1)
        n.input(b, latency=1)
        n.output(c, latency=1)
        logging.info(r'NFA {} adds a "null" node. input port: {}, {} output port: {}'.format(self.name, a, b, c))

    def execute(self, text: str):
        """ Execute NFA and record matched string """

        logging.info(r'NFA {} execution'.format(self.name))
        self.state = self.m.execute(source_event(self.input_port, text, 0))
        if self.is_matched():
            output = self.state.get(self.output_port)
            if output == '':
                self._matched_index = len(text)
                self._matched_str = text
            else:
                for i in range(len(text)):
                    if text[i:] == output:
                        self._matched_index = i
                        break
                self._matched_str = text[0:self._matched_index]

    def visualize(self):
        """ Visualizing NFA """
        return self.m.visualize()

    def is_matched(self):
        """ Determine whether NFA matches text """
        if self.state.get(self.output_port) is None:
            return False
        else:
            return True

    def get_matched_str(self):
        """ Get the matched string """
        return self._matched_str

    def get_matched_index(self):
        """ Get the matched index """
        return self._matched_index
