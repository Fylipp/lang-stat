import sys
from functools import reduce
from operator import add
from typing import Counter
import re

import ostd
import pysrt as srt

from langstat import scrape

if len(sys.argv) not in (2, 3):
    print("Usage: {} <LANGUAGE CODE> [WORD COUNT = 100]".format(sys.argv[0]))
    sys.exit(1)

# Extract the command-line arguments
LANGUAGE = sys.argv[1]
WORD_COUNT = sys.argv[2] if len(sys.argv) > 2 else 100

print("Looking for subtitles with language code: {}".format(LANGUAGE))

movies = scrape.scrape_movie_ids(LANGUAGE)
subtitles_per_movie = map(lambda movie: list(scrape.scrape_subtitle_id(movie)), movies)
subtitles = reduce(add, list(subtitles_per_movie), [])

total_words = 0
counter = Counter()

print("Connecting to OpenSubtitles.org ...")

with ostd.Downloader('lang-stat v1') as downloader:
    print("Downloading ...")

    for result in downloader.download(*list(subtitles)):
        try:
            subs = srt.SubRipFile.from_string(result.content)

            for sub in subs:
                words = re.sub(r'[^\w]', ' ', sub.text_without_tags.lower()).split()
                total_words += len(words)
                counter.update(words)
        except Exception as e:
            print(type(e))
            print('Error whilst processing subtitles with id {} (will be excluded from statistics): {}'.format(
                result.subtitle_id, e))

print()
print('--- Results ---')

most_common = counter.most_common(WORD_COUNT)
most_common_total_words = sum(map(lambda x: x[1], most_common))
amount_of_most_common = len(most_common)

if amount_of_most_common != WORD_COUNT:
    print('Warning: Cannot analyze top {:,} words because only {:,} were found'.format(WORD_COUNT,
                                                                                       amount_of_most_common))
    print()

print('Analyzed {:,} words'.format(total_words))
print('The top {:,} make up {:.2f} % of all words'.format(amount_of_most_common,
                                                          most_common_total_words / total_words * 100))

for pair in most_common:
    print('{:.2f} %: {}'.format(pair[1] / total_words * 100, pair[0]))
