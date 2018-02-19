import argparse
import re
import sys
from functools import reduce
from operator import add
from typing import Counter

import ostd
import pysrt as srt

from langstat import scrape

arg_parser = argparse.ArgumentParser(description='find the most used words in a language')
arg_parser.add_argument('--csv', help='output the results as csv', action='store_true')
arg_parser.add_argument('language_code', help='language code to use', type=str)
arg_parser.add_argument('word_count', help='the amount of most common words to summarize', nargs='?', type=int, default=100)
args = arg_parser.parse_args(sys.argv[1:])

CSV = args.csv
LANGUAGE = args.language_code
WORD_COUNT = args.word_count


def log(msg: object = ''):
    if not CSV:
        print(msg)


log("Looking for subtitles with language code: {}".format(LANGUAGE))

movies = scrape.scrape_movie_ids(LANGUAGE)
subtitles_per_movie = map(lambda movie: list(scrape.scrape_subtitle_id(movie)), movies)
subtitles = reduce(add, list(subtitles_per_movie), [])

total_words = 0
counter = Counter()

log("Connecting to OpenSubtitles.org ...")

with ostd.Downloader('lang-stat v1') as downloader:
    log("Downloading ...")

    for result in downloader.download(*list(subtitles)):
        try:
            subs = srt.SubRipFile.from_string(result.content)

            for sub in subs:
                words = re.sub(r'[^\w]', ' ', sub.text_without_tags.lower()).split()
                total_words += len(words)
                counter.update(words)
        except Exception as e:
            log(type(e))
            log('Error whilst processing subtitles with id {} (will be excluded from statistics): {}'.format(
                result.subtitle_id, e))

log()
log('--- Results ---')

most_common = counter.most_common(WORD_COUNT)
most_common_total_words = sum(map(lambda x: x[1], most_common))
amount_of_most_common = len(most_common)

if amount_of_most_common != WORD_COUNT:
    log('Warning: Cannot analyze top {:,} words because only {:,} were found'.format(WORD_COUNT,
                                                                                     amount_of_most_common))
    log()

log('Analyzed {:,} words'.format(total_words))
log('The top {:,} make up {:.2f} % of all words'.format(amount_of_most_common,
                                                        most_common_total_words / total_words * 100))

for pair in most_common:
    FACTOR = pair[1] / total_words
    WORD = pair[0]

    log('{:.2f} %: {}'.format(FACTOR * 100, WORD))

    if CSV:
        print('{},{}'.format(FACTOR, WORD))
