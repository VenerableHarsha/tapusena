import argparse
from _typeshed import Incomplete

def main_inner(parser, argns): ...

class HelpFormatter(argparse.HelpFormatter):
    def __init__(
        self, prog, indent_increment: int = ..., max_help_position: int = ..., width: Incomplete | None = ...
    ) -> None: ...

def main(args=...): ...
