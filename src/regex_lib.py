from regex_to_nfa import regex_to_nfa


def match(regex: str, text: str):
    """ Try to match a pattern from the beginning of the string.
    If the match is not successful at the beginning, match() returns none. """
    nfa = regex_to_nfa(regex)
    nfa.execute(text)
    if nfa.is_matched():
        res = (0, nfa.get_matched_index())
        return res
    return None


def search(regex: str, text: str):
    """ Scan the entire string and return the first successful match. """
    nfa = regex_to_nfa(regex)
    if regex[0] == '^':
        nfa.execute(text)
        if nfa.is_matched():
            res = (0, nfa.get_matched_index())
            return res
    else:
        for i in range(len(text)):
            nfa.execute(text[i:])
            if nfa.is_matched():
                res = (i, i + nfa.get_matched_index())
                return res
    return None


def sub(regex: str, repl: str, text: str, count=0):
    """ Replace matches in string """
    nfa = regex_to_nfa(regex)
    repl_len = len(repl)
    res = "".join(text)
    t_count = count if count != 0 else repl_len
    i = 0
    j = 0
    if regex[0] == '^':
        nfa.execute(res)
        if nfa.is_matched():
            mst = nfa.get_matched_str()
            res = res.replace(mst, repl, 1)
    else:
        while i < len(res) and j < t_count:
            nfa.execute(res[i:])
            if nfa.is_matched():
                mst = nfa.get_matched_str()
                res = res[0:i] + res[i:].replace(mst, repl, 1)
                i += repl_len
                j += 1
            i += 1
    return res


def split(regex: str, text: str, maxsplit=0):
    """ The method divides the string according to the substring that can be matched and returns the list """
    nfa = regex_to_nfa(regex)
    res_lst = []
    t_count = maxsplit if maxsplit != 0 else len(text)
    i = 0
    j = 0
    if regex[0] == '^':
        nfa.execute(text)
        if nfa.is_matched():
            mst = nfa.get_matched_str()
            tmp = text.replace(mst, '', 1)
            res_lst.append('')
            res_lst.append(tmp)
    else:
        k = 0
        while i < len(text) and j < t_count:
            nfa.execute(text[i:])
            if nfa.is_matched():
                res_lst.append(text[k:i])
                i += nfa.get_matched_index()
                k = i
                j += 1
            else:
                i += 1
        res_lst.append(text[i:])
    return res_lst