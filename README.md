# lang-stat

A simple Python app that downloads the most used subtitles in a certain language from
[OpenSubtitles.org](https://www.opensubtitles.org) and summarizes the top used words.

## Installation

```sh
pip install langstat
```

## Usage

```sh
py -m langstat [-h] [--csv] language_code [word_count]
```

**Note**: The OpenSubtitles login and download can be slow at times!

The language code has to be a [three-letter language code](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes).

## License

MIT.
