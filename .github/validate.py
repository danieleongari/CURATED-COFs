#!/usr/bin/env python
"""Check consistency of CURATED COF database"""

import os
import sys
import pandas
import click
import collections

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]
ROOT_DIR = os.path.join(SCRIPT_PATH, os.pardir)

FRAMEWORKS_CSV = os.path.join(ROOT_DIR, 'cof-frameworks.csv')
PAPERS_CSV = os.path.join(ROOT_DIR, 'cof-papers.csv')

FRAMEWORKS_DF = pandas.read_csv(FRAMEWORKS_CSV)
PAPERS_DF = pandas.read_csv(PAPERS_CSV)

@click.group()
def cli():
    pass


@cli.command('unique-dois')
def validate_unique_dois():
    """Check that paper DOIs are unique."""
    dois = PAPERS_DF['DOI'].str.lower()

    duplicates = [item for item, count in collections.Counter(list(dois)).items() if count > 1]

    if duplicates:
        print('Error: Duplicate DOIs detected: {}'.format(duplicates))
        sys.exit(1)

    print('No duplicate DOIs found.')


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
