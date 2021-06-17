from regex_fa_construction import *
from common import sp_chars, Kind, element_type
from typing import Tuple


@arg_type(0, str)
def regex_to_tokens(regex: str) -> list:
    """ Convert the regular expression to a token list.
    By analyzing the token list, we can get the semantics of metacharacter in regular expression. """

    tokens = []  # type 0 denotes operators, type 1 denotes normal operands
    lst = list(regex)
    i = 0
    while i < len(lst):
        if lst[i] == '\\':
            if i + 1 < len(lst):
                d = process_trans(lst[i + 1])
                i += 1
        elif lst[i] == '.':
            d = {'value': lst[i], 'type': 1, 'kind': Kind.DOT}
        elif lst[i] == '[':
            inc, d = process_set(regex[i:])
            i += inc
        elif lst[i] == '*' or lst[i] == '+' or lst[i] == '^' or lst[i] == '$' or lst[i] == '(' or lst[i] == ')':
            d = {'value': lst[i], 'type': 0, 'kind': Kind.NORMAL}
        elif lst[i] == '{':
            inc, d = process_range(regex[i:])
            i += inc
        else:
            d = {'value': lst[i], 'type': 1, 'kind': Kind.NORMAL}
        tokens.append(d)
        i += 1
    add_concat(tokens)
    return tokens


@arg_type(0, list)
@element_type(0, dict)
def add_concat(tokens: list) -> None:
    """ Adding concat operation to the regular expression token list """
    concat = {'value': 'concat', 'type': 0, 'kind': Kind.CONCAT}
    con_index = []
    for i in (range(len(tokens) - 1)):
        if (is_repeat(tokens[i]) and is_left_bracket(tokens[i + 1])) or \
                (is_repeat(tokens[i]) and tokens[i + 1].get('type') == 1):
            con_index.append(i + 1)
        elif (is_right_bracket(tokens[i]) and is_left_bracket(tokens[i + 1])) or \
                (is_right_bracket(tokens[i]) and tokens[i + 1].get('type') == 1):
            con_index.append(i + 1)
        elif (tokens[i].get('type') == 1 and is_left_bracket(tokens[i + 1])) or \
                (tokens[i].get('type') == 1 and tokens[i + 1].get('type') == 1):
            con_index.append(i + 1)
    for i in reversed(con_index):
        tokens.insert(i, concat)


@arg_type(0, dict)
def is_repeat(token: dict) -> bool:
    """ Judge whether the token is a repeated operation """
    if token.get('kind') == Kind.NORMAL:
        if token.get('value') == '*' or token.get('value') == '+':
            return True
    else:
        if token.get('kind') == Kind.RANGE:
            return True
    return False


@arg_type(0, dict)
def is_left_bracket(token: dict) -> bool:
    """ Judge whether the token is left bracket """
    if token.get('type') == 0 and token.get('value') == '(':
        return True
    return False


@arg_type(0, dict)
def is_right_bracket(token: dict) -> bool:
    """ Judge whether the token is right bracket """
    if token.get('type') == 0 and token.get('value') == ')':
        return True
    return False


@arg_type(0, dict)
def is_concat(token: dict) -> bool:
    """ Judge whether the token is concat """
    if token.get('kind') == Kind.CONCAT:
        return True
    return False


@arg_type(0, dict)
def is_prefix(token: dict) -> bool:
    """ Judge whether the token is a header match """
    if token.get('type') == 0 and token.get('value') == '^':
        return True
    return False


@arg_type(0, dict)
def is_postfix(token: dict) -> bool:
    """ Judge whether the token is a tail match """
    if token.get('type') == 0 and token.get('value') == '$':
        return True
    return False


@arg_type(0, str)
def process_trans(character: str) -> dict:
    """ Process characters after '\' """
    if character in sp_chars:
        d = {'value': character, 'type': 1, 'kind': Kind.NORMAL}
    elif character == 'w' or character == 's' or character == 'd':
        d = {'value': character, 'type': 1, 'kind': Kind.TRANS}
    return d


@arg_type(0, str)
def process_set(substr: str) -> Tuple[int, dict]:
    """ Process characters in '[]' """
    increment = 0
    while substr[increment] != ']': increment += 1
    if substr[1] == '^':
        d = {'value': substr[0:increment + 1], 'type': 1, 'kind': Kind.NEG_SET,
             Kind.NEG_SET: charset_parser(substr[1:increment])}
    else:
        d = {'value': substr[0:increment + 1], 'type': 1, 'kind': Kind.SET,
             Kind.SET: charset_parser(substr[1:increment])}
    return increment, d


@arg_type(0, str)
def charset_parser(charset: str) -> list:
    """ Analyze the string in '[]' and convert it to token list """
    set_token_lst = []

    alp_nfa = RegexFaConstruction('alpha')
    alp_nfa.add_alpha_node(alp_nfa.input_port, 'n1')
    alp_nfa.add_normal_node('n1', 'n2', '-')
    alp_nfa.add_alpha_node('n2', alp_nfa.output_port)

    dig_nfa = RegexFaConstruction('digit')
    dig_nfa.add_digit_node(dig_nfa.input_port, 'n1')
    dig_nfa.add_normal_node('n1', 'n2', '-')
    dig_nfa.add_digit_node('n2', dig_nfa.output_port)

    i = 0
    while i < len(charset):
        if charset[i] == '\\' and i + 1 < len(charset):
            if charset[i + 1] in sp_chars:
                d = {'type': Kind.NORMAL, 'value': charset[i + 1]}
                i += 1
            elif charset[i + 1] in ['w', 's', 'd']:
                d = {'type': Kind.TRANS, 'value': charset[i + 1]}
                i += 1
        elif charset[i].isalpha() and i + 2 < len(charset) and charset[i + 1] == '-':
            alp_nfa.execute(charset[i:i + 3])
            if alp_nfa.is_matched():
                d = {'type': 'alpha_' + Kind.RANGE, Kind.RANGE: [charset[i], charset[i + 2]]} # type: ignore
                i += 2
        elif charset[i].isdigit() and i + 2 < len(charset) and charset[i + 1] == '-':
            dig_nfa.execute(charset[i:i + 3])
            if dig_nfa.is_matched():
                d = {'type': 'digit_' + Kind.RANGE, Kind.RANGE: [int(charset[i]), int(charset[i + 2])]} # type: ignore
                i += 2
        else:
            d = {'type': Kind.NORMAL, 'value': charset[i]}
        set_token_lst.append(d)
        i += 1
    return set_token_lst


@arg_type(0, str)
def process_range(substr: str) -> Tuple[int, dict]:
    """ Process repeated operation with '{}' """
    increment = 0
    while substr[increment] != '}': increment += 1

    m1 = RegexFaConstruction('{n}')
    m1.add_normal_node(m1.input_port, 'n1', '{')
    m1.add_digit_node('n1', 'n2')
    m1.add_normal_node('n2', m1.output_port, '}')

    m2 = RegexFaConstruction('{min,}')
    m2.add_normal_node(m2.input_port, 'n1', '{')
    m2.add_digit_node('n1', 'n2')
    m2.add_normal_node('n2', 'n3', ',')
    m2.add_normal_node('n3', m2.output_port, '}')

    m3 = RegexFaConstruction('{,max}')
    m3.add_normal_node(m3.input_port, 'n1', '{')
    m3.add_normal_node('n1', 'n2', ',')
    m3.add_digit_node('n2', 'n3')
    m3.add_normal_node('n3', m3.output_port, '}')

    m4 = RegexFaConstruction('{min,max}')
    m4.add_normal_node(m4.input_port, 'n1', '{')
    m4.add_digit_node('n1', 'n2')
    m4.add_normal_node('n2', 'n3', ',')
    m4.add_digit_node('n3', 'n4')
    m4.add_normal_node('n4', m4.output_port, '}')

    input_str = substr[0:increment + 1]
    m1.execute(input_str)
    m2.execute(input_str)
    m3.execute(input_str)
    m4.execute(input_str)

    if m1.is_matched():
        d = {'value': substr[0:increment + 1], 'type': 0, 'kind': Kind.RANGE,
             Kind.RANGE: [int(substr[1]), int(substr[1])]}
    elif m2.is_matched():
        # -1 denotes infinity
        d = {'value': substr[0:increment + 1], 'type': 0, 'kind': Kind.RANGE, Kind.RANGE: [int(substr[1]), -1]}
    elif m3.is_matched():
        d = {'value': substr[0:increment + 1], 'type': 0, 'kind': Kind.RANGE, Kind.RANGE: [0, int(substr[2])]}
    elif m4.is_matched():
        d = {'value': substr[0:increment + 1], 'type': 0, 'kind': Kind.RANGE,
             Kind.RANGE: [int(substr[1]), int(substr[3])]}
    return increment, d

