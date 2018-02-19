from setuptools import setup

setup(
    name='langstat',
    version='1.1.0',

    description='Finds most common words for a language',
    author='Philipp Ploder',
    url='https://github.com/Fylipp/lang-stat',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='opensubtitles',

    packages=['langstat'],

    install_requires=[
        'pysrt',
        'requests',
        'lxml',
        'ostd'
    ]
)
