import argparse
import sys
from logic.lexicon import Lexicon
import logic.word
from logic.word import Word
from logic.geometry import Geometry
from logic.solver import Solver
from logic.stopwatch import Stopwatch


def get_options():
    parser = argparse.ArgumentParser(
        add_help=True, description="Solving of crosswords")
    parser.add_argument('-w', '--words', type=str, default=None,
                        help="File with list of words")
    parser.add_argument('-g', '--grid', type=str, default=None,
                        help="File with description of grid")
    parser.add_argument('-o', '--output', type=str, default=None,
                        help="File for output")
    parser.add_argument('-c', '--encoding', type=str, default='utf-8',
                        help="Encoding for files")
    parser.add_argument('-a', '--answers', type=int, default=1,
                        help="Amount of answers to output (1 by default)")
    parser.add_argument('-t', '--time', action='store_true', default=False,
                        help="Watch time of work of program")
    parser.add_argument('-ni', '--net_in', action='store_true', default=False,
                        help="Input grid in form of net. " +
                        "Only for second dimension")
    parser.add_argument('-no', '--net_out', action='store_true', default=False,
                        help="Output answer in form of net. " +
                        "Only for second dimension")
    parser.add_argument('-p', '--progressbar', action='store_true',
                        default=False, help="Progress bar for lexicon")
    return vars(parser.parse_args())


def main():
    options = get_options()
    words = get_words(options)
    grid = get_grid(options)
    with Stopwatch('Lexicon got in ', options['time']):
        lexicon = Lexicon(words, progress_output(options))
    with Stopwatch('Geometry got in ', options['time']):
        geometry = Geometry(grid)
    with Stopwatch('Crossword solved in ', options['time']):
        solver = Solver(geometry, lexicon)
        answers = solver.solve(options['answers'])
    output_answers(answers, options)
    if len(answers) < options['answers']:
        sys.exit(1)


def get_words(options):
    try:
        res = []
        if options['words'] is not None:
            with open(options['words'], encoding=options['encoding']) as f:
                for line in f.readlines():
                    res.append(line.strip())
        else:
            while True:
                next_line = input()
                if next_line == '':
                    break
                res.append(next_line)
        return res
    except Exception:
        print('Words: incorrect notation', file=sys.stderr)
        sys.exit(10)


def get_grid(options):
    try:
        res = []
        if options['grid'] is not None:
            with open(options['grid'], encoding=options['encoding']) as f:
                for line in f.readlines():
                    res.append(line.strip())
        else:
            while True:
                next_line = input()
                if next_line == '':
                    break
                res.append(next_line)
        if options['net_in']:
            return logic.word.WordsFromGridGetter(res).get_words()
        return list(map(get_empty_word, res))
    except Exception:
        print('Grid: incorrect notation', file=sys.stderr)
        sys.exit(10)


def get_empty_word(string):
    args = list(map(int, string.split()))
    return Word(args[:-2], args[-2], args[-1])


def output_answers(answers, options):
    if not answers:
        print('No solution')
    if options['output'] is not None:
        with open(options['output'], 'w', encoding=options['encoding']) as f:
            for answer in answers:
                f.write(answer.string(in_grid=options['net_out']))
                f.write('\n')
    else:
        for answer in answers:
            print(answer.string(in_grid=options['net_out']))
            print()


def progress_output(options):
    if options['progressbar']:
        return print
    return None


if __name__ == '__main__':
    main()
