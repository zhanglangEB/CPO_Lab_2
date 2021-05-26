import unittest

from regex_parser import charset_parser
from regex_fa_construction import *


class RegexFaConstructionTest(unittest.TestCase):

    def test_extend_nodes(self):
        nfa1 = RegexFaConstruction('nfa1')
        nfa2 = RegexFaConstruction('nfa2')
        nfa2.add_normal_node(nfa2.input_port, nfa2.output_port, 'a')
        self.assertEqual(nfa1.get_node_list(), [])
        nfa1.extend_nodes(nfa2.get_node_list())
        self.assertEqual(nfa1.get_node_list(), nfa2.get_node_list())
        self.assertRaises(TypeError, lambda: nfa1.extend_nodes([1, 2, 3]))

    def test_get_node_list(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_normal_node(nfa.input_port, 'n1', 'a')
        nfa.add_normal_node('n1', nfa.output_port, 'b')
        nodes = nfa.get_node_list()
        self.assertEqual(len(nodes), 2)
        self.assertEqual('n1' in nodes[0].outputs, True)
        self.assertEqual('n1' in nodes[1].inputs, True)

    def test_get_input_node(self):
        nfa = RegexFaConstruction('nfa')
        self.assertEqual(nfa.get_input_node(), None)
        nfa.add_normal_node(nfa.input_port, 'n1', 'a')
        nfa.add_normal_node('n1', nfa.output_port, 'b')
        input_node = nfa.get_input_node()
        self.assertEqual(nfa.input_port in input_node.inputs, True)

    def test_set_input_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_normal_node(nfa.input_port, nfa.output_port, 'a')
        nfa.set_input_node('new_name')
        self.assertEqual(nfa.get_input_node(), None)
        nodes = nfa.get_node_list()
        self.assertEqual('new_name' in nodes[0].inputs, True)

    def test_get_output_node(self):
        nfa = RegexFaConstruction('nfa')
        self.assertEqual(nfa.get_output_node(), None)
        nfa.add_normal_node(nfa.input_port, 'n1', 'a')
        nfa.add_normal_node('n1', nfa.output_port, 'b')
        output_node = nfa.get_output_node()
        self.assertEqual(nfa.output_port in output_node.outputs, True)

    def test_set_output_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_normal_node(nfa.input_port, nfa.output_port, 'a')
        nfa.set_output_node('new_name')
        self.assertEqual(nfa.get_output_node(), None)
        nodes = nfa.get_node_list()
        self.assertEqual('new_name' in nodes[0].outputs, True)

    def test_add_da_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_da_node(nfa.input_port, nfa.output_port)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('1')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('_')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('%')
        self.assertEqual(nfa.is_matched(), False)

    def test_add_empty_char_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_empty_char_node(nfa.input_port, nfa.output_port)
        nfa.execute('\n')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('\t')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('\r')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('\f')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), False)

    def test_add_digit_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_digit_node(nfa.input_port, nfa.output_port)
        nfa.execute('1')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('9')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), False)

    def test_add_alpha_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_alpha_node(nfa.input_port, nfa.output_port)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('2')
        self.assertEqual(nfa.is_matched(), False)
        nfa.execute('_')
        self.assertEqual(nfa.is_matched(), False)

    def test_any_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_any_node(nfa.input_port, nfa.output_port)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('#')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('\\')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('1')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('\n')
        self.assertEqual(nfa.is_matched(), False)

    def test_normal_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_normal_node(nfa.input_port, nfa.output_port, 'a')
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('b')
        self.assertEqual(nfa.is_matched(), False)
        nfa.execute('\n')
        self.assertEqual(nfa.is_matched(), False)

    def test_add_charset_node(self):
        nfa = RegexFaConstruction('nfa')
        charset = charset_parser(r'\sa-zA-Z5-9')
        nfa.add_charset_node(nfa.input_port, nfa.output_port, charset, negative=False)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('z')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('\n')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('6')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('1')
        self.assertEqual(nfa.is_matched(), False)
        f = RegexFaConstruction('f')
        charset = charset_parser(r'2-9')
        f.add_charset_node(f.input_port, f.output_port, charset, negative=True)
        f.execute('a')
        self.assertEqual(f.is_matched(), True)
        f.execute('1')
        self.assertEqual(f.is_matched(), True)
        f.execute('2')
        self.assertEqual(f.is_matched(), False)
        f.execute('5')
        self.assertEqual(f.is_matched(), False)
        f.execute('9')
        self.assertEqual(f.is_matched(), False)

    def test_add_end_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_end_node(nfa.input_port, nfa.output_port)
        nfa.execute('')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), False)

    def test_add_all_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_all_node(nfa.input_port, nfa.output_port)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('1')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('_')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('^')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('#')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('\n')
        self.assertEqual(nfa.is_matched(), True)

    def test_add_null_11_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_null_11_node(nfa.input_port, 'n1')
        nfa.add_normal_node('n1', nfa.output_port, 'a')
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)

    def test_add_null_12_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_null_12_node(nfa.input_port, 'n1', 'n2')
        nfa.add_normal_node('n1', nfa.output_port, 'a')
        nfa.add_normal_node('n2', nfa.output_port, 'b')
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('b')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('c')
        self.assertEqual(nfa.is_matched(), False)

    def test_add_null_21_node(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_null_12_node(nfa.input_port, 'n1', 'n2')
        nfa.add_normal_node('n1', 'n3', 'a')
        nfa.add_normal_node('n2', 'n4', 'b')
        nfa.add_null_21_node('n3', 'n4', nfa.output_port)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('b')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('c')
        self.assertEqual(nfa.is_matched(), False)

    def test_visualize(self):
        nfa = RegexFaConstruction('nfa')
        nfa.add_null_12_node(nfa.input_port, 'n1', 'n2')
        nfa.add_normal_node('n1', 'n3', 'a')
        nfa.add_normal_node('n2', 'n4', 'b')
        nfa.add_null_21_node('n3', 'n4', nfa.output_port)
        graph = 'digraph G {' \
                '\n  rankdir=LR;' \
                '\n  Input[shape=rarrow];' \
                '\n  Output[shape=rarrow];' \
                '\n  n_0[label="null_12"];' \
                '\n  n_1[label="normal"];' \
                '\n  n_2[label="normal"];' \
                '\n  n_3[label="null_21"];' \
                '\n  Input -> n_0;' \
                '\n  n_0 -> n_1[label="n1"];' \
                '\n  n_0 -> n_2[label="n2"];' \
                '\n  n_1 -> n_3[label="n3"];' \
                '\n  n_2 -> n_3[label="n4"];' \
                '\n  n_3 -> Output;' \
                '\n}'
        self.assertEqual(nfa.visualize(), graph)


if __name__ == '__main__':
    unittest.main()