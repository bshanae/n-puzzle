import argparse
import sys
from typing import List, Optional, Callable, Tuple
import random

from algo.n_puzzle.heuristics import HEURISTICS
from reader.constants import PUZZLE_MAP_TYPE
from reader.npuzzle_gen import make_puzzle

COMMENT_CHAR = '#'


def puzzle_repr(puzzle: PUZZLE_MAP_TYPE) -> str:
    return '\n'.join([' '.join(map(str, row)) for row in puzzle])


class ErrorTmpl:
    too_big_map = 'lines count ({len}) is bigger than map size ({size})\nGiven puzzle is:\n{pz}'
    too_short_map = 'lines count ({len}) is shorter than map size ({size})\nGiven puzzle is:\n{pz}'
    no_size = 'map size should be given before puzzle'
    inc_line_size = 'given map size is {size} but the line size is {len}'
    inc_numbers = 'map with size {size} should contain numbers from 0 to {max_nbr}'
    not_number = 'map should contain only numbers, {exc}'
    no_maps = 'No puzzles given! Please give me at least one map to solve!'


class ParserError(Exception):
    _sample = '\nCorrect sample is:\n# This puzzle is solvable\n3\n0 1 2\n3 4 8\n7 6 5\n'
    _tmpl = 'Incorrect input on "{token}": {msg}\n{sample}'

    def __init__(self, token, msg):
        self.message = self._tmpl.format(token=token, msg=msg, sample=self._sample)


class ArgParser:

    @property
    def parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file', help='Input file')
        parser.add_argument('-H', choices=HEURISTICS.keys(), default='manhattan', help='heuristic func')
        parser.add_argument('-s', '--size', type=int,  default=3, help='Size to generate random map: default 3',)
        parser.add_argument('-c', '--count', type=int, default=1, help='Count of maps to generate: default 1',)
        parser.add_argument('-i', type=int, default=10000, help='Number of passes to generator')
        parser.add_argument('-v', action='store_true', help='Enable visualizer')
        parser.add_argument('-q', action='store_true', help='Quiet mode')
        parser.add_argument('-g', action='store_true', help='Greedy search')
        parser.add_argument('-u', action='store_true', help='Uniform-cost search')
        parser.add_argument('-S', '--solvable', action='store_false', help='Is generated map solvable')
        parser.add_argument('-U', '--unsolvable', action='store_false', help='Is generated map unsolvable')

        return parser

    @property
    def args(self):
        return self.parser.parse_args()

    @property
    def h_function(self) -> Callable:
        return HEURISTICS[self.args.H]

    @property
    def greedy_and_uniform(self) -> Tuple[bool, bool]:
        """Greedy priority if both flags were chosen. :return greedy, uniform"""
        if self.args.g and self.args.u:
            return True, False
        return self.args.g, self.args.u

    @property
    def gui_and_console(self) -> Tuple[bool, bool]:
        """"Console disabled only in quiet mode :return gui, console"""
        if self.args.q:
            return False, False
        return self.args.v, True

    @property
    def puzzles(self) -> List[PUZZLE_MAP_TYPE]:
        args = self.args
        if args.file:
            return self._read_from_file(args.file)

        random.seed()
        solvable = True
        if not args.solvable and not args.unsolvable:
            solvable = random.choice([True, False])
        elif args.solvable:
            solvable = args.solvable
        elif args.unsolvable:
            solvable = args.unsolvable

        return self._generate_puzzle(args.count, args.size, solvable, args.i)

    def _read_from_file(self, filename: str) -> List[PUZZLE_MAP_TYPE]:
        """:except ParserError"""
        try:
            return self._parse_puzzles(filename)
        except ParserError as e:
            print(e.message)
            sys.exit(1)

    @staticmethod
    def _generate_puzzle(ct: int, size: int, solvable: bool, iterations: int) -> List[PUZZLE_MAP_TYPE]:
        print(f'start generate {ct} random puzzles with size {size}')
        puzzles = []
        for _ in range(ct):
            generated = make_puzzle(s=size, solvable=solvable, iterations=iterations)

            listed_puzzle = [generated[i: i + size] for i in range(0, size * size, size)]
            puzzles.append(listed_puzzle)

        print(f'successfully generate {ct} puzzles\n')
        return puzzles

    def _parse_puzzles(self, map_file: str) -> List[PUZZLE_MAP_TYPE]:
        """:raise ParserError"""
        puzzles = []
        one_puzzle = []
        size: Optional[int] = 0
        with open(map_file, 'r') as f:
            for row in f.read().splitlines():
                line = row.partition(COMMENT_CHAR)[0].strip(' ')
                if not line and not one_puzzle:
                    continue

                if not line and one_puzzle:
                    puzzle_len = len(one_puzzle)
                    if puzzle_len < size:
                        raise ParserError(
                            line,
                            ErrorTmpl.too_short_map.format(len=puzzle_len, size=size, pz=puzzle_repr(one_puzzle))
                        )
                    puzzles.append(one_puzzle)
                    one_puzzle = []
                    continue

                if line.isdigit():
                    size = int(line)

                elif line:
                    puzzle_row = self._check_parse_line(line, size)
                    one_puzzle.append(puzzle_row)
                    puzzle_len = len(one_puzzle)
                    if puzzle_len > size:
                        raise ParserError(
                            line,
                            ErrorTmpl.too_big_map.format(len=puzzle_len, size=size, pz=puzzle_repr(one_puzzle))
                        )
        if one_puzzle:
            puzzles.append(one_puzzle)
        if not puzzles:
            raise ParserError(token=map_file, msg=ErrorTmpl.no_maps)

        return puzzles

    @staticmethod
    def _check_parse_line(line: str, size: int) -> List[int]:
        """:raise ParserError"""
        if not size:
            raise ParserError(line, ErrorTmpl.no_size)
        spl = line.split()
        if len(spl) != size:
            raise ParserError(line, ErrorTmpl.inc_line_size.format(size=size, len=len(spl)))
        try:
            puzzle_row = list(map(int, spl))
            correct_elems = list(map(lambda x: bool(size * size - 1 >= x >= 0), puzzle_row))
            if not all(correct_elems):
                raise ParserError(line, ErrorTmpl.inc_numbers.format(size=size, max_nbr=size * size - 1))
        except ValueError as e:
            raise ParserError(line, ErrorTmpl.not_number.format(exc=e))

        return puzzle_row
