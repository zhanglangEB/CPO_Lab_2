import unittest

from regex_to_nfa import *


class RegexToNfaTest(unittest.TestCase):

    def test_repeat_nfa(self):
        nfa = RegexFaConstruction('nfa')
        self.assertRaises(TypeError, lambda: repeat_nfa(1, 2))
        self.assertRaises(ValueError, lambda: repeat_nfa(nfa, 2))
        nfa.add_normal_node(nfa.input_port, '0', 'w')
        nfa.add_normal_node('0', '1', 'x')
        nfa.add_normal_node('1', nfa.output_port, 'x')
        new_nfa = repeat_nfa(nfa, 2)
        new_nfa.execute('wxxwxx')
        self.assertEqual(new_nfa.get_matched_str(), 'wxxwxx')
        new_nfa.execute('wxx')
        self.assertEqual(new_nfa.is_matched(), False)

    def test_repeat_or_output_nfa(self):
        nfa = RegexFaConstruction('nfa')
        self.assertRaises(TypeError, lambda: repeat_or_output_nfa(1, 2))
        self.assertRaises(ValueError, lambda: repeat_or_output_nfa(nfa, 2))
        nfa.add_normal_node(nfa.input_port, '0', 'w')
        nfa.add_normal_node('0', '1', 'x')
        nfa.add_normal_node('1', nfa.output_port, 'x')
        new_nfa = repeat_or_output_nfa(nfa, 2)
        new_nfa.execute('wxxwxx')
        self.assertEqual(new_nfa.get_matched_str(), 'wxxwxx')
        new_nfa.execute('')
        self.assertEqual(new_nfa.is_matched(), True)

    def test_nodes_repeat_ge_zero(self):
        nfa = RegexFaConstruction('nfa')
        self.assertRaises(TypeError, lambda: nodes_repeat_ge_zero(1, 2))
        self.assertRaises(ValueError, lambda: nodes_repeat_ge_zero(nfa, 0))
        nfa.add_normal_node(nfa.input_port, nfa.output_port, 'a')
        nfa, inc = nodes_repeat_ge_zero(nfa, 0)
        nfa.execute('')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('aaaaaa')
        self.assertEqual(nfa.is_matched(), True)

    def test_nodes_repeat_ge_one(self):
        nfa = RegexFaConstruction('nfa')
        self.assertRaises(TypeError, lambda: nodes_repeat_ge_one(1, 2))
        self.assertRaises(ValueError, lambda: nodes_repeat_ge_one(nfa, 0))
        nfa.add_normal_node(nfa.input_port, nfa.output_port, 'a')
        nfa, inc = nodes_repeat_ge_one(nfa, 0)
        nfa.execute('')
        self.assertEqual(nfa.is_matched(), False)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('aaaaaa')
        self.assertEqual(nfa.get_matched_str(), 'aaaaaa')

    def test_nodes_repeat_eq(self):
        nfa = RegexFaConstruction('nfa')
        self.assertRaises(TypeError, lambda: nodes_repeat_eq(1, 2))
        self.assertRaises(ValueError, lambda: nodes_repeat_eq(nfa, 3))
        nfa.add_normal_node(nfa.input_port, nfa.output_port, 'a')
        nfa = nodes_repeat_eq(nfa, 3)
        nfa.execute('')
        self.assertEqual(nfa.is_matched(), False)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), False)
        nfa.execute('aaa')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('aaaa')
        self.assertEqual(nfa.get_matched_str(), 'aaa')

    def test_nodes_repeat_range(self):
        nfa = RegexFaConstruction('nfa')
        self.assertRaises(TypeError, lambda: nodes_repeat_range(1, 0, 2, 5))
        self.assertRaises(ValueError, lambda: nodes_repeat_range(nfa, 0, 1, 3))
        nfa.add_normal_node(nfa.input_port, nfa.output_port, 'a')
        nfa, inc = nodes_repeat_range(nfa, 0, 1, 3)
        nfa.execute('')
        self.assertEqual(nfa.is_matched(), False)
        nfa.execute('a')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('aa')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('aaa')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('aaaa')
        self.assertEqual(nfa.get_matched_str(), 'aaa')

    def test_nodes_prefix(self):
        nfa = RegexFaConstruction('nfa')
        self.assertRaises(TypeError, lambda: nodes_prefix(1, 2))
        self.assertRaises(ValueError, lambda: nodes_prefix(nfa, 0))
        nfa.add_normal_node(nfa.input_port, 'n1', 'a')
        nfa.add_normal_node('n1', nfa.output_port, 'b')
        nfa, inc = nodes_prefix(nfa, 0)
        nfa.execute('ab')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('abcd')
        self.assertEqual(nfa.get_matched_str(), 'ab')
        nfa.execute('bb')
        self.assertEqual(nfa.is_matched(), False)

    def test_nodes_postfix(self):
        nfa = RegexFaConstruction('test')
        self.assertRaises(TypeError, lambda: nodes_postfix(1, 2))
        self.assertRaises(ValueError, lambda: nodes_postfix(nfa, 0))
        nfa.add_normal_node(nfa.input_port, 'n1', 'a')
        nfa.add_normal_node('n1', nfa.output_port, 'b')
        nfa, inc = nodes_postfix(nfa, 0)
        nfa.execute('ab')
        self.assertEqual(nfa.is_matched(), True)
        nfa.execute('cdab')
        self.assertEqual(nfa.is_matched(), False)

    def test_regex_to_nfa(self):
        regex = r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
        self.assertRaises(TypeError, lambda: regex_to_nfa(1))
        nfa = regex_to_nfa(regex)
        nfa.execute('wangxin@hdu.edu.com')
        self.assertEqual(nfa.get_matched_str(), 'wangxin@hdu.edu.com')


if __name__ == '__main__':
    unittest.main()