from msilib.schema import Class
from typing import Any
from pprint import PrettyPrinter

pprint = PrettyPrinter().pprint

yaml_str = """\
name:
  model:
    a: 1
    b: 2
    c: 3
  init: test
  states:
  - name: hello
    on_enter: 
    - one
    - two
      - two is zero
    - three
  transitions:
  - name: hello
    sorces:
    - hello
    dest: world
    conditions:
    - a or
    - b or
    - - c and
      - d
"""


class Token:
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class Key(Token):
    def __init__(self, name="<Key>") -> None:
        self.name = name
        pass

    def __str__(self):
        return f"{self.name}:"

    def __repr__(self) -> str:
        return f'Key("{self.name}")'


class Expression(Token):
    def __init__(self, value="<Exp>") -> None:
        self.value = value
        pass

    def __str__(self):
        return f"{self.value}"

    def __repr__(self) -> str:
        return f'Expression("{self.value}")'


class NewLine(Token):
    def __str__(self) -> str:
        return "\n"

    def __repr__(self) -> str:
        return r"\n"


class Indent(Token):
    def __str__(self) -> str:
        return "  "


class ListToken(Token):
    def __str__(self) -> str:
        return "- "


class BlockStart(Token):
    def __str__(self) -> str:
        return "<BlockStart>\n"


class BlockEnd(Token):
    def __str__(self) -> str:
        return "<BlockEnd>\n"


class Comment(Token):
    def __init__(self, value="<Comment>") -> None:
        self.value = value
        pass

    def __str__(self):
        return f"# {self.value}"

    def __repr__(self):
        return f"Comment({self.value})"


class mylist(list):
    def __getitem__(self, index: int) -> Any:
        if index < 0:
            return None
        if index >= len(self):
            return None
        return super().__getitem__(index)


def check_stream(
    i: int,
    tokens: list[Token],
    checks: list[Class],
    direction: int = 1,
    include_self: bool = False,
):
    if direction == -1:
        checks = reversed(checks)
    for j, check in enumerate(checks):
        if not isinstance(tokens[i + direction * (j + 1 - include_self)], check):
            return False
    return True


def print_tokens():
    print()
    for token in tokens:
        print(token, end="")
    print()


test_list = [
    [Key("name"), NewLine()],
    [Indent(), Key("model"), NewLine()],
    [Indent(), Indent(), Key("a"), Expression("1"), NewLine()],
    [NewLine()],
    [Indent(), Comment("test comment"), NewLine()],
    [Indent(), Key("initial"), Expression("start"), NewLine()],
    [Indent(), Key("states"), NewLine()],
    [NewLine()],
    [Indent(), Comment("the start state"), NewLine()],
    [Indent(), ListToken(), Expression("a"), NewLine()],
    [Indent(), ListToken(), ListToken(), Expression("b = c"), NewLine()],
    [Indent(), Indent(), ListToken(), Expression("True"), NewLine()],
]


test_list = [item for sublist in test_list for item in sublist]
tokens = mylist()
for item in test_list:
    tokens.append(item)

indent_level = 0
i = -1
while True:
    i += 1
    if i == len(tokens):
        break
    if check_stream(i, tokens, [Key, NewLine], direction=-1, include_self=False):
        print(i)
        tokens.insert(i, BlockStart())
        indent_level += 1
    if check_stream(
        i,
        tokens,
        [NewLine] + [Indent] * (indent_level - 1),
        direction=1,
        include_self=True,
    ) and not check_stream(
        i, tokens, [NewLine] + [Indent] * indent_level, direction=1, include_self=True
    ):
        tokens.insert(i + 1, BlockEnd())
        indent_level -= 1
pprint(tokens)
print_tokens()


"<Indent>*<Key><Expression><NewLine>"
# return the start_index, the end_index, and the number of indents
# 5, 9

# block start
# the insides of blocks look the same as the outside recursive
"<Indent>*<Key><NewLine>[<NewLine>|<Indent>|<Comment>]*"

# first go through and delete Indents in front of comments
# we do want the author to have the abillity to leave empty lines where they are not enforced
