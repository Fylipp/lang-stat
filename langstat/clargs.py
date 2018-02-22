import argparse
import sys
from collections import namedtuple

Arguments = namedtuple('Arguments', ('csv', 'language', 'word_count'))


class ArgParser:
    def __init__(self):
        arg_parser = argparse.ArgumentParser(description='find the most used words in a language')
        arg_parser.add_argument('--csv', help='output the results as csv', action='store_true')
        arg_parser.add_argument('language_code', help='language code to use', type=str)
        arg_parser.add_argument('word_count', help='the amount of most common words to summarize', type=int,
                                nargs='?', default=100)

        self._arg_parser = arg_parser

    def parse(self, args=sys.argv[1:]):
        args = self._arg_parser.parse_args(args)
        return Arguments(args.csv, args.language_code, args.word_count)
