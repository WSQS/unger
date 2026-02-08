import argparse
from dataclasses import dataclass, field
from typing import Any, Generator


def is_non_terminal(token: str):
    return token[0].isupper()


@dataclass
class Grammar:
    non_terminal: set[str] = field(default_factory=set[str])
    terminal: set[str] = field(default_factory=set[str])
    rule: list[tuple[str, list[str]]] = field(
        default_factory=list[tuple[str, list[str]]]
    )
    start_symbol: str = field(default_factory=str)


@dataclass
class Sentence:
    token: list[str]
    start_index: int = field(default=1)


def parse_grammar(s_grammer: str):
    grammar = Grammar()
    for l_id, lg in enumerate(s_grammer.splitlines(), start=1):
        if not lg.strip():
            continue
        sides = lg.split("->", 1)
        if len(sides) != 2:
            msg = f"{l_id}:Missing '->' in {lg!r}"
            raise ValueError(msg)
        l, r = sides[0].strip(), sides[1].strip()
        if len(l) == 0:
            msg = f"{l_id}:It's empty in left side:{lg!r}"
            raise ValueError(msg)
        # No need to check right side, if right side is empty, it means epsilon
        if not is_non_terminal(l):
            msg = f"{l_id}:It's not a non terminal in left:{l!r}"
            raise ValueError(msg)
        if not grammar.start_symbol:
            grammar.start_symbol = l
        grammar.non_terminal.add(l)
        rs = r.split()
        for ri in rs:
            if is_non_terminal(ri):
                grammar.non_terminal.add(ri)
            else:
                grammar.terminal.add(ri)
        grammar.rule.append((l, rs))
    return grammar


def group_into(n_element: int, n_group: int) -> Generator[list[int], Any, None]:
    if n_element < 0 or n_group < 0:
        msg = f"n_element = {n_element} < 0 or n_group = {n_group} < 0"
        raise ValueError(msg)
    if n_group == 0:
        return
    if n_group == 1:
        yield [n_element]
        return
    for i in range(1, n_element + 1):
        for l in group_into(n_element - i, n_group - 1):
            yield [i] + l


def parse_substring(g: Grammar, ts: Sentence, symbol: str):
    result = Grammar()
    for l, rs in g.rule:
        if l != symbol:
            continue
        print(f"rule:{l, rs}")
        for group_info in group_into(len(ts.token), len(rs)):
            print("group_info", group_info)
            group_grammar = Grammar()
            ts_copy = ts.token[:]
            substrings: list[list[str]] = []
            for substring_length in group_info:
                if substring_length == 0:
                    substrings.append([])
                    continue
                substrings.append(ts_copy[:substring_length])
                ts_copy = ts_copy[substring_length:]
            print("substring", substrings)
            new_rs: list[str] = []
            offset = 0
            for r, substring in zip(rs, substrings):
                if is_non_terminal(r):
                    subgrammar = parse_substring(
                        g, Sentence(substring, ts.start_index + offset), r
                    )
                    if not subgrammar.rule:
                        break
                    group_grammar.rule += subgrammar.rule
                else:
                    if len(substring) != 1 or substring[0] != r:
                        break
                    group_grammar.rule.append(
                        (f"{r}_{ts.start_index + offset}_{len(substring)}", [r])
                    )
                new_rs.append(f"{r}_{ts.start_index + offset}_{len(substring)}")
                offset += len(substring)
            else:
                # the group is match successfully
                result.rule += group_grammar.rule
                result.rule.append((f"{l}_{ts.start_index}_{len(ts.token)}", new_rs))
    return result


def parse(g: Grammar, ts: Sentence):
    return parse_substring(g, ts, g.start_symbol)


def main():
    parser = argparse.ArgumentParser(
        description="Python implementation for Unger's parsing method."
    )
    parser.add_argument("grammar", type=str, help="Grammar File")
    parser.add_argument("input", type=str, help="Input File")
    args = parser.parse_args()
    with open(args.grammar, "r", encoding="utf-8") as f:
        s_g = f.read()
    g = parse_grammar(s_g)
    print(g)
    with open(args.input, "r", encoding="utf-8") as f:
        s_i = f.read()
    tokens = s_i.split()
    for token in tokens:
        if token not in g.terminal:
            msg = f"It's not a non terminal in grammar:{token!r}"
            raise ValueError(msg)
    parse_tree_grammar = parse(g, Sentence(tokens))
    print(parse_tree_grammar)
    for l, rs in parse_tree_grammar.rule:
        for r in rs:
            print(l, "-->", r)


if __name__ == "__main__":
    main()
