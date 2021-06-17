from typing import Union

empty_chars = ['\n', '\t', '\r', '\f']

sp_chars = ['\\', '*', '+', '.', '^', '$', '[', ']', '{', '}', '(', ')']


class Kind:
    NORMAL = 'normal'
    CONCAT = 'concat'
    RANGE = 'range'
    TRANS = 'trans'
    DOT = 'dot'
    SET = 'charset'
    NEG_SET = 'neg-charset'
    ALPHA_RANGE = 'alpha_range'
    DIGIT_RANGE = 'digit_range'


def arg_type(arg_index: Union[int, list], arg_type):
    lst_index = [arg_index] if not isinstance(arg_index, list) else arg_index
    lst_type = [arg_type] if not isinstance(arg_type, list) else arg_type

    def trace(f):
        def traced(*args, **kwargs):
            flag: bool = True
            arg = None
            tp = None
            for i, t in zip(lst_index, lst_type):
                if not isinstance(args[i], t):
                    flag = False
                    arg = args[i]
                    tp = t
            if flag:
                return f(*args, **kwargs)
            else:
                raise TypeError('The type of argument {} is not {}'.format(arg, tp))
        return traced

    return trace


def arg_callable(arg_index: int):
    def trace(f):
        def traced(*args, **kwargs):
            if callable(args[arg_index]):
                return f(*args, **kwargs)
            else:
                raise TypeError('The type of argument {} is not callable'.format(args[arg_index]))

        return traced

    return trace


def element_type(arg_index: int, elem_type):
    def trace(f):
        def traced(*args, **kwargs):
            for elem in args[arg_index]:
                if not isinstance(elem, elem_type):
                    raise TypeError('The type of element in list must be {} type'.format(elem_type))

            return f(*args, **kwargs)

        return traced

    return trace
