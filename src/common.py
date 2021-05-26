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
