import unittest

from regex_parser import *


class RegexParserTest(unittest.TestCase):

    def test_process_trans(self):
        self.assertEqual(process_trans('$'), {'value': '$', 'type': 1, 'kind': Kind.NORMAL})
        self.assertEqual(process_trans('w'), {'value': 'w', 'type': 1, 'kind': Kind.TRANS})
        self.assertEqual(process_trans('s'), {'value': 's', 'type': 1, 'kind': Kind.TRANS})
        self.assertEqual(process_trans('d'), {'value': 'd', 'type': 1, 'kind': Kind.TRANS})

    def test_process_set(self):
        inc, d = process_set(r'[a-z\w0-9]')
        act_d = {'value': '[a-z\\w0-9]', 'type': 1, 'kind': 'charset',
                 'charset': [{'type': 'alpha_range', 'range': ['a', 'z']},
                             {'type': 'trans', 'value': 'w'}, {'type': 'digit_range', 'range': [0, 9]}]}
        self.assertEqual(d, act_d)
        self.assertRaises(TypeError, lambda: process_set(None))

    def test_process_range(self):
        inc, d = process_range('{5}')
        self.assertEqual(d, {'value': '{5}', 'type': 0, 'kind': 'range', 'range': [5, 5]})
        inc, d = process_range('{3,}')
        self.assertEqual(d, {'value': '{3,}', 'type': 0, 'kind': 'range', 'range': [3, -1]})
        inc, d = process_range('{3,5}')
        self.assertEqual(d, {'value': '{3,5}', 'type': 0, 'kind': 'range', 'range': [3, 5]})
        inc, d = process_range('{,5}')
        self.assertEqual(d, {'value': '{,5}', 'type': 0, 'kind': 'range', 'range': [0, 5]})
        self.assertRaises(TypeError, lambda: process_range(None))

    def test_charset_parser(self):
        charset = r'\w\.%-A-Za-z0-9'
        lst = charset_parser(charset)
        act_lst = [{'type': 'trans', 'value': 'w'},
                   {'type': 'normal', 'value': '.'},
                   {'type': 'normal', 'value': '%'},
                   {'type': 'normal', 'value': '-'},
                   {'type': 'alpha_range', 'range': ['A', 'Z']},
                   {'type': 'alpha_range', 'range': ['a', 'z']},
                   {'type': 'digit_range', 'range': [0, 9]}]
        self.assertEqual(lst, act_lst)
        self.assertRaises(TypeError, lambda: charset_parser(None))

    def test_regex_to_tokens(self):
        regex = r'(ab)*[^0-9]+\w\s{2,8}{2,}ac{,8}b{6}'
        tokens = regex_to_tokens(regex)
        act_tokens = [{'value': '(', 'type': 0, 'kind': 'normal'},
                      {'value': 'a', 'type': 1, 'kind': 'normal'},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': 'b', 'type': 1, 'kind': 'normal'},
                      {'value': ')', 'type': 0, 'kind': 'normal'},
                      {'value': '*', 'type': 0, 'kind': 'normal'},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': '[^0-9]', 'type': 1, 'kind': 'neg-charset',
                       'neg-charset': [{'type': 'normal', 'value': '^'},
                                       {'type': 'digit_range', 'range': [0, 9]}]},
                      {'value': '+', 'type': 0, 'kind': 'normal'},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': 'w', 'type': 1, 'kind': 'trans'},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': 's', 'type': 1, 'kind': 'trans'},
                      {'value': '{2,8}', 'type': 0, 'kind': 'range', 'range': [2, 8]},
                      {'value': '{2,}', 'type': 0, 'kind': 'range', 'range': [2, -1]},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': 'a', 'type': 1, 'kind': 'normal'},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': 'c', 'type': 1, 'kind': 'normal'},
                      {'value': '{,8}', 'type': 0, 'kind': 'range', 'range': [0, 8]},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': 'b', 'type': 1, 'kind': 'normal'},
                      {'value': '{6}', 'type': 0, 'kind': 'range', 'range': [6, 6]}]

        self.assertEqual(tokens, act_tokens)
        self.assertRaises(TypeError, lambda: regex_to_tokens(None))

    def test_add_concat(self):
        tokens = [{'value': 'a', 'type': 1, 'kind': 'normal'},
                  {'value': 'b', 'type': 1, 'kind': 'normal'},
                  {'value': '[^0-9]', 'type': 1, 'kind': 'neg-charset',
                   'neg-charset': [{'type': 'normal', 'value': '^'},
                                   {'type': 'digit_range', 'range': [0, 9]}]}]
        add_concat(tokens)
        act_tokens = [{'value': 'a', 'type': 1, 'kind': 'normal'},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': 'b', 'type': 1, 'kind': 'normal'},
                      {'value': 'concat', 'type': 0, 'kind': 'concat'},
                      {'value': '[^0-9]', 'type': 1, 'kind': 'neg-charset',
                       'neg-charset': [{'type': 'normal', 'value': '^'},
                                       {'type': 'digit_range', 'range': [0, 9]}]}]
        self.assertEqual(tokens, act_tokens)
        self.assertRaises(TypeError, lambda: add_concat(None))


if __name__ == '__main__':
    unittest.main()
