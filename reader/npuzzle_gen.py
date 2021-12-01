#!/usr/bin/env python

import sys
import os
import argparse
import random
from pathlib import Path
from typing import List

PUZZLES_DIR = '../puzzles_generated'


def make_puzzle(s, solvable, iterations):
    def swap_empty(p):
        idx = p.index(0)
        poss = []
        if idx % s > 0:
            poss.append(idx - 1)
        if idx % s < s - 1:
            poss.append(idx + 1)
        if idx / s > 0 and idx - s >= 0:
            poss.append(idx - s)
        if idx / s < s - 1:
            poss.append(idx + s)
        swi = random.choice(poss)
        p[idx] = p[swi]
        p[swi] = 0

    p = make_goal(s)
    for i in range(iterations):
        swap_empty(p)

    if not solvable:
        if p[0] == 0 or p[1] == 0:
            p[-1], p[-2] = p[-2], p[-1]
        else:
            p[0], p[1] = p[1], p[0]

    return p


def make_goal(s):
    ts = s * s
    puzzle = [-1 for i in range(ts)]
    cur = 1
    x = 0
    ix = 1
    y = 0
    iy = 0
    while True:
        puzzle[x + y * s] = cur
        if cur == 0:
            break
        cur += 1
        if x + ix == s or x + ix < 0 or (ix != 0 and puzzle[x + ix + y * s] != -1):
            iy = ix
            ix = 0
        elif y + iy == s or y + iy < 0 or (iy != 0 and puzzle[x + (y + iy) * s] != -1):
            ix = -iy
            iy = 0
        x += ix
        y += iy
        if cur == s * s:
            cur = 0

    return puzzle


def save_puzzles_to_file(
    puzzles_list: List[list],
    puzzles_count: int,
    is_solvable: bool,
    size: int,
) -> None:
    Path(PUZZLES_DIR).mkdir(parents=True, exist_ok=True)
    files = os.listdir(f'./{PUZZLES_DIR}')
    existed_counts = []

    for one in files:
        if one.startswith('puzzle'):
            existed_counts.append(int(one.split('_')[1].split('.')[0]))
    file_ct = max(existed_counts) + 1 if len(existed_counts) else 1
    filename = f'puzzle(x{puzzles_count})_{file_ct}.txt'

    with open(f'{PUZZLES_DIR}/{filename}', 'w') as f:
        f.write(f'# This puzzle is {"solvable" if is_solvable else "unsolvable"}\n')
        f.write(f'{size}\n')
        for one_puzzle in puzzles_list:
            for y in range(size):
                string = ' '.join(map(str, one_puzzle[(y*size):(y + 1) * size]))
                f.write(f'{string}\n')
            f.write('\n')

    print(f"Results saved to file {filename}")


def print_puzzles(puzzles_list: List[list], is_solvable: bool, size: int) -> None:
    print("# This puzzle is %s" % ("solvable" if is_solvable else "unsolvable"))
    print("%d" % size)
    for one_puzzle in puzzles_list:
        for i in range(0, size * size, size):
            print(' '.join(map(str, one_puzzle[i : i + size])))
        print('')


if __name__ == "__main__":
    """
        Добавлены кастомные флаги генератора
        -c количество пазлов для генерации
        -f запись в файл
        -p печать на экран
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("size", type=int, help="Size of the puzzle's side. Must be >3.")
    parser.add_argument("-s", "--solvable", action="store_true", default=False,
                        help="Forces generation of a solvable puzzle. Overrides -u.")
    parser.add_argument("-u", "--unsolvable", action="store_true", default=False,
                        help="Forces generation of an unsolvable puzzle")
    parser.add_argument("-i", "--iterations", type=int, default=10000, help="Number of passes")
    parser.add_argument("-c", "--count", type=int, default=1, help="Number of puzzles to generate")
    parser.add_argument("-p", "--print", action='store_true', default=False, help="Print generated maps")
    parser.add_argument("-f", "--file", action='store_true', default=False, help="Save generated maps to file")

    args = parser.parse_args()

    random.seed()

    if not args.print and not args.file:
        print("Please tell me what to do: print result (-p) or save to file (-f)")
        sys.exit(1)

    if args.solvable and args.unsolvable:
        print("Can't be both solvable AND unsolvable, dummy !")
        sys.exit(1)

    if args.size < 3:
        print("Can't generate a puzzle with size lower than 2. It says so in the help. Dummy.")
        sys.exit(1)

    if not args.solvable and not args.unsolvable:
        solv = random.choice([True, False])
    elif args.solvable:
        solv = True
    elif args.unsolvable:
        solv = False

    s = args.size
    puzzles_ct = args.count

    puzzles = []
    for _ in range(puzzles_ct):
        puzzle = make_puzzle(s, solvable=solv, iterations=args.iterations)
        puzzles.append(puzzle)

    if args.print:
        print_puzzles(puzzles_list=puzzles, is_solvable=solv, size=s)

    elif args.file:
        save_puzzles_to_file(puzzles_list=puzzles, puzzles_count=puzzles_ct, is_solvable=solv, size=s)
