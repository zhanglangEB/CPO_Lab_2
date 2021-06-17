from regex_to_nfa import regex_to_nfa
from typing import Optional
from common import arg_type


@arg_type([0, 1], [str, str])
def match(regex: str, text: str) -> Optional[tuple]:
    """ Try to match a pattern from the beginning of the string.
    If the match is not successful at the beginning, match() returns none. """
    nfa = regex_to_nfa(regex)
    nfa.execute(text)
    if nfa.is_matched():
        res = (0, nfa.get_matched_index())
        return res
    return None


@arg_type([0, 1], [str, str])
def search(regex: str, text: str) -> Optional[tuple]:
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


@arg_type([0, 1, 2], [str, str, str])
def sub(regex: str, repl: str, text: str, count: int = 0) -> str:
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


@arg_type([0, 1], [str, str])
def split(regex: str, text: str, maxsplit: int = 0) -> list:
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
