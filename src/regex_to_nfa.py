from regex_parser import *
from regex_fa_construction import RegexFaConstruction


def regex_to_nfa(regex: str):
    """ Convert regex expression to NFA """
    re_lst = regex_to_tokens(regex)
    nfa_stack = []
    op_stack = []
    node_index = 0
    for token in re_lst:
        # current token is operand
        if token.get('type') == 1:
            f = RegexFaConstruction()
            if token.get('kind') == Kind.NORMAL:
                f.add_normal_node(f.input_port, f.output_port, pattern_char=token.get('value'))
            else:
                if token.get('kind') == Kind.SET:
                    f.add_charset_node(f.input_port, f.output_port, charset=token.get(Kind.SET), negative=False)
                elif token.get('kind') == Kind.NEG_SET:
                    f.add_charset_node(f.input_port, f.output_port, charset=token.get(Kind.SET), negative=True)
                elif token.get('kind') == Kind.TRANS:
                    if token.get('value') == 'w':
                        f.add_da_node(f.input_port, f.output_port)
                    elif token.get('value') == 's':
                        f.add_empty_char_node(f.input_port, f.output_port)
                    else:
                        f.add_digit_node(f.input_port, f.output_port)
                elif token.get('kind') == Kind.DOT:
                    f.add_any_node(f.input_port, f.output_port)
            nfa_stack.append(f)
            node_index += 1
        # current token is operator
        else:
            if is_left_bracket(token):
                op_stack.append(token)
            elif is_repeat(token):
                f = nfa_stack.pop()
                if token.get('kind') == Kind.NORMAL:
                    if token.get('value') == '*':
                        f, inc = nodes_repeat_ge_zero(f, node_index)
                        node_index += inc
                    elif token.get('value') == '+':
                        f, inc = nodes_repeat_ge_one(f, node_index)
                        node_index += inc
                    nfa_stack.append(f)
                else:
                    r = token.get(Kind.RANGE)
                    if r[0] == r[1]:
                        new_f = nodes_repeat_eq(f, r[0])
                    else:
                        new_f, inc = nodes_repeat_range(f, node_index, r[0], r[1])
                    nfa_stack.append(new_f)
            elif is_prefix(token) or is_postfix(token):
                while len(op_stack) > 0 and not is_left_bracket(op_stack[-1]):
                    op = op_stack.pop()
                    if is_concat(op):
                        f1 = nfa_stack.pop()
                        f2 = nfa_stack.pop()
                        new_f = concat_nfa(f2, f1, 'con' + str(node_index))
                        nfa_stack.append(new_f)
                        node_index += 1
                    elif is_postfix(op):
                        f = nfa_stack.pop()
                        f, inc = nodes_postfix(f, node_index)
                        node_index += inc
                        nfa_stack.append(f)
                    elif is_prefix(op):
                        f = nfa_stack.pop()
                        f, inc = nodes_prefix(f, node_index)
                        node_index += inc
                        nfa_stack.append(f)
                op_stack.append(token)
            elif is_concat(token):
                while len(op_stack) > 0 and is_concat(op_stack[-1]):
                    op_stack.pop()
                    f1 = nfa_stack.pop()
                    f2 = nfa_stack.pop()
                    new_f = concat_nfa(f2, f1, 'con' + str(node_index))
                    nfa_stack.append(new_f)
                    node_index += 1
                op_stack.append(token)
            elif is_right_bracket(token):
                while len(op_stack) > 0 and not is_left_bracket(op_stack[-1]):
                    op = op_stack.pop()
                    if is_concat(op):
                        f1 = nfa_stack.pop()
                        f2 = nfa_stack.pop()
                        new_f = concat_nfa(f2, f1, 'con' + str(node_index))
                        nfa_stack.append(new_f)
                        node_index += 1
                    elif is_postfix(op):
                        f = nfa_stack.pop()
                        f, inc = nodes_postfix(f, node_index)
                        node_index += inc
                        nfa_stack.append(f)
                    elif is_prefix(op):
                        f = nfa_stack.pop()
                        f, inc = nodes_prefix(f, node_index)
                        node_index += inc
                        nfa_stack.append(f)
                op_stack.pop()
    while len(op_stack):
        op = op_stack.pop()
        if is_concat(op):
            f1 = nfa_stack.pop()
            f2 = nfa_stack.pop()
            new_f = concat_nfa(f2, f1, 'con' + str(node_index))
            nfa_stack.append(new_f)
            node_index += 1
        elif is_postfix(op):
            f = nfa_stack.pop()
            f, inc = nodes_postfix(f, node_index)
            node_index += inc
            nfa_stack.append(f)
        elif is_prefix(op):
            f = nfa_stack.pop()
            f, inc = nodes_prefix(f, node_index)
            node_index += inc
            nfa_stack.append(f)
    nfa = nfa_stack.pop()
    return nfa


def nodes_repeat_ge_zero(nfa: RegexFaConstruction, node_index: int):
    """ Repeated operation, the number of repetitions is greater than or equal to 0.
     Corresponding to '*' function """
    if not nfa.get_node_list():
        raise ValueError('There is no node in nfa')
    nfa.set_input_node(str(node_index + 2))
    nfa.set_output_node(str(node_index + 3))
    nfa.add_null_12_node(nfa.input_port, str(node_index), str(node_index + 1))
    nfa.add_null_11_node(str(node_index + 1), nfa.output_port)
    nfa.add_null_21_node(str(node_index), str(node_index + 4), str(node_index + 2))
    nfa.add_null_12_node(str(node_index + 3), str(node_index + 4), nfa.output_port)
    node_inc = 5
    return nfa, node_inc


def nodes_repeat_ge_one(nfa: RegexFaConstruction, node_index: int):
    """ Repeated operation, the number of repetitions is greater than or equal to 1.
     Corresponding to '+' function """
    if not nfa.get_node_list():
        raise ValueError('There is no node in nfa')
    nfa.set_input_node(str(node_index + 1))
    nfa.set_output_node(str(node_index + 2))
    nfa.add_null_11_node(nfa.input_port, str(node_index))
    nfa.add_null_21_node(str(node_index), str(node_index + 3), str(node_index + 1))
    nfa.add_null_12_node(str(node_index + 2), str(node_index + 3), nfa.output_port)
    node_inc = 4
    return nfa, node_inc


def nodes_repeat_eq(nfa: RegexFaConstruction, times: int):
    """ Repeated operation, the times of repetition is equal to a specified number.
     Corresponding to '{n}' function """
    if not nfa.get_node_list():
        raise ValueError('There is no node in nfa')
    nfa = repeat_nfa(nfa, times)
    return nfa


def nodes_repeat_range(nfa: RegexFaConstruction, node_index: int, gt: int, lt: int):
    """ Repeated operation, the number of repetitions is in a specified range.
     Corresponding to '{m,n}' function """
    if not nfa.get_node_list():
        raise ValueError('There is no node in nfa')
    f1 = repeat_nfa(nfa, gt)
    if lt == -1:
        f1.set_output_node(str(node_index))
        f1.add_null_12_node(str(node_index), str(node_index + 1), str(node_index + 2))
        f1.add_null_21_node(str(node_index + 1), str(node_index + 5), str(node_index + 3))
        f1.add_null_12_node(str(node_index + 4), str(node_index + 5), nfa.output_port)
        f1.add_null_11_node(str(node_index + 2), nfa.output_port)
        nfa.set_input_node(str(node_index + 3))
        nfa.set_output_node(str(node_index + 4))
        node_inc = 6
        f1.extend_nodes(nfa.get_node_list())
    else:
        f2 = repeat_or_output_nfa(nfa, lt - gt)
        f1 = concat_nfa(f1, f2, 'con' + str(node_index))
        node_inc = 1
    return f1, node_inc


def nodes_prefix(nfa: RegexFaConstruction, node_index: int):
    """ Operation of matching header. Corresponding to '^' function """
    if not nfa.get_node_list():
        raise ValueError('There is no node in nfa')
    # nfa.set_output_node(str(node_index))
    # nfa.add_null_21_node(str(node_index), str(node_index + 3), str(node_index + 1))
    # nfa.add_any_node(str(node_index + 1), str(node_index + 2))
    # nfa.add_null_12_node(str(node_index + 2), str(node_index + 3), nfa.output_port)
    # node_inc = 4
    # nfa.set_output_node(str(node_index))
    # nfa.add_null_12_node(str(node_index), str(node_index + 1), nfa.output_port)
    # nfa.add_null_21_node(str(node_index + 1), str(node_index + 4), str(node_index + 2))
    # nfa.add_all_node(str(node_index + 2), str(node_index + 3))
    # nfa.add_null_12_node(str(node_index + 3), str(node_index + 4), nfa.output_port)
    nfa.set_output_node(str(node_index))
    nfa.add_null_11_node(str(node_index), nfa.output_port)
    node_inc = 1
    return nfa, node_inc


def nodes_postfix(nfa: RegexFaConstruction, node_index: int):
    """ Operation of matching tail. Corresponding to '^' function """
    if not nfa.get_node_list():
        raise ValueError('There is no node in nfa')
    # nfa.set_input_node(str(node_index + 3))
    # nfa.add_null_21_node(nfa.input_port, str(node_index + 2), str(node_index))
    # nfa.add_any_node(str(node_index), str(node_index + 1))
    # nfa.add_null_12_node(str(node_index + 1), str(node_index + 2), str(node_index + 3))
    # node_inc = 4

    # nfa.set_input_node(str(node_index + 6))
    # nfa.set_output_node(str(node_index + 7))
    # nfa.add_null_12_node(nfa.input_port, str(node_index), str(node_index + 5))
    # nfa.add_null_21_node(str(node_index), str(node_index + 4), str(node_index + 1))
    # nfa.add_all_node(str(node_index + 1), str(node_index + 2))
    # nfa.add_null_12_node(str(node_index + 2), str(node_index + 3), str(node_index + 4))
    # nfa.add_null_21_node(str(node_index + 3), str(node_index + 5), str(node_index + 6))
    # nfa.add_end_node(str(node_index + 7), nfa.output_port)
    nfa.set_output_node(str(node_index))
    nfa.add_end_node(str(node_index), nfa.output_port)
    node_inc = 1
    return nfa, node_inc


def concat_nfa(nfa1: RegexFaConstruction, nfa2: RegexFaConstruction, node_index: str):
    """ Concat nfa2 to nfa1 """
    nfa1.set_output_node(node_index)
    nfa2.set_input_node(node_index)
    nfa1.extend_nodes(nfa2.get_node_list())
    return nfa1


def repeat_nfa(nfa: RegexFaConstruction, times: int):
    """ Repeat and concatenate NFA for a specified number of times """
    if not nfa.get_node_list():
        raise ValueError('There is no node in nfa')
    nodes = nfa.get_node_list()
    new_nodes = []
    new_nfa = RegexFaConstruction('nfa')
    if times <= 0:
        new_nfa.add_null_11_node(new_nfa.input_port, new_nfa.output_port)
        return new_nfa
    new_nodes.extend(copy.deepcopy(nodes))
    for i in range(times - 1):
        postfix = '_' + str(i + 1)
        tmp_nodes = copy.deepcopy(nodes)
        con = 'c' + postfix
        for t_node in tmp_nodes:
            for key_in, val_in in t_node.inputs.items():
                if key_in != nfa.input_port:
                    t_node.inputs[key_in + postfix] = val_in
                    t_node.inputs.pop(key_in)
            for key_out, val_out in t_node.outputs.items():
                if key_out != nfa.output_port:
                    t_node.outputs[key_out + postfix] = val_out
                    t_node.outputs.pop(key_out)
            if nfa.input_port in t_node.inputs:
                t_node.inputs.pop(nfa.input_port)
                t_node.inputs[con] = 1
        for node in new_nodes:
            if new_nfa.output_port in node.outputs:
                node.outputs.pop(new_nfa.output_port)
                node.outputs[con] = 1
        new_nodes.extend(tmp_nodes)
    new_nfa.extend_nodes(new_nodes)
    return new_nfa


def repeat_or_output_nfa(nfa: RegexFaConstruction, times: int):
    """ Repeat and concatenate NFA for a specified number of times.
     An output port is added at the beginning of each repeating unit """
    if not nfa.get_node_list():
        raise ValueError('There is no node in nfa')
    nodes = nfa.get_node_list()
    new_nodes = []
    new_nfa = RegexFaConstruction('nfa')
    if times <= 0:
        new_nfa.add_null_11_node(new_nfa.input_port, new_nfa.output_port)
        return new_nfa
    new_nodes.extend(copy.deepcopy(nodes))
    for i in range(times - 1):
        postfix = '_' + str(i + 1)
        tmp_nodes = copy.deepcopy(nodes)
        con = 'c' + postfix
        for t_node in tmp_nodes:
            for key_in, val_in in t_node.inputs.items():
                if key_in != nfa.input_port:
                    t_node.inputs[key_in + postfix] = val_in
                    t_node.inputs.pop(key_in)
            for key_out, val_out in t_node.outputs.items():
                if key_out != nfa.output_port:
                    t_node.outputs[key_out + postfix] = val_out
                    t_node.outputs.pop(key_out)
            if nfa.input_port in t_node.inputs:
                t_node.inputs.pop(nfa.input_port)
                t_node.inputs[con] = 1
        for node in new_nodes:
            if new_nfa.output_port in node.outputs:
                node.outputs[con] = 1
        new_nodes.extend(tmp_nodes)
    new_nfa.extend_nodes(new_nodes)
    new_nfa.add_null_11_node(new_nfa.input_port, new_nfa.output_port)
    return new_nfa
