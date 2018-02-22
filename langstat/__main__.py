import re
from functools import reduce
from operator import add
from typing import Counter

import ostd
import pysrt as srt

from langstat import scrape
from langstat.clargs import ArgParser

args = ArgParser().parse()


def log(msg: object = ''):
    if not args.csv:
        print(msg)


log("Looking for subtitles with language code: {}".format(args.language))

movies = scrape.scrape_movie_ids(args.language)
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

            # Process all subtitles
            for sub in subs:
                # Split the text into individual words
                words = re.sub(r'[^\w\'\-]+', ' ', sub.text_without_tags.lower()).split()

                # Keep track of the total amount of words
                total_words += len(words)

                # Update the word counter
                counter.update(words)
        except Exception as e:
            log(type(e))
            log('Error whilst processing subtitles with id {} (will be excluded from statistics): {}'.format(
                result.subtitle_id, e))

log()
log('--- Results ---')

# Get the most common words
most_common = counter.most_common(args.word_count)

# Summarize the total frequency of the most common words
most_common_total_words = sum(map(lambda x: x[1], most_common))

# Count the amount of words that were actually returned by the counter
# This could be less than the requested amount when not enough different words are available
amount_of_most_common = len(most_common)

if amount_of_most_common != args.word_count:
    log('Warning: Cannot analyze top {:,} words because only {:,} were found'.format(args.word_count,
                                                                                     amount_of_most_common))
    log()

log('Analyzed {:,} words'.format(total_words))
log('The top {:,} make up {:.2f} % of all words'.format(amount_of_most_common,
                                                        most_common_total_words / total_words * 100))

for pair in most_common:
    FACTOR = pair[1] / total_words
    WORD = pair[0]

    log('{:.2f} %: {}'.format(FACTOR * 100, WORD))

    if args.csv:
        print('{},{}'.format(FACTOR, WORD))
