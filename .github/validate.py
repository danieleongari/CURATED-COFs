#!/usr/bin/env python
"""Check consistency of CURATED COF database"""

import os
import sys
import pandas
import click
import collections

from ase import io, geometry

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

@cli.command('unique-cof-ids')
def validate_unique_cof_ids():
    """Check that CURATED-COF IDs are unique."""
    ids = FRAMEWORKS_DF['CURATED-COFs ID'].str.lower()

    duplicates = [item for item, count in collections.Counter(list(ids)).items() if count > 1]

    if duplicates:
        print('Error: Duplicate CURATED-COF IDs detected: {}'.format(duplicates))
        sys.exit(1)

    print('No duplicate CURATED-COF IDs found.')


@cli.command('unique-cof-names')
def validate_unique_cof_names():
    """Check that CURATED-COF names are unique."""
    names = FRAMEWORKS_DF['Name'].str.lower()
    names = names.str.replace('-',' ')

    duplicates = [item for item, count in collections.Counter(list(names)).items() if count > 1]

    if duplicates:
        print('Warning: Duplicate CURATED-COF names detected: {}'.format(duplicates))
        sys.exit(1)

    print('No duplicate CURATED-COF names found.')

@cli.command('duplicates-marked-reciprocally')
def duplicates_marked_reciprocally():
    """Check that marking of rows with "Duplicate found" is reciprocal."""
    ids = FRAMEWORKS_DF['CURATED-COFs ID'].str
    messages = []

    for _index, row in FRAMEWORKS_DF.iterrows():
        if row['Duplicate found'] != 'none':
            original_id = row['CURATED-COFs ID']
            duplicate_id = row['Duplicate found']
            duplicate_row = FRAMEWORKS_DF.loc[FRAMEWORKS_DF['CURATED-COFs ID'] == duplicate_id ]
            if not len(duplicate_row) == 1:
                messages.append(f'Found row without reciprocal duplicate mark:\n{row}')

            duplicate_row_original_id = duplicate_row['Duplicate found'].values[0]
            if not duplicate_row['Duplicate found'].values[0] == original_id:
                messages.append(f'Duplicate row lists ID {duplicate_row_original_id}, expected {original_id}')

    if messages:
       print(messages)
       sys.exit(1)

    print('Rows marked as duplicates go both ways.')


@cli.command('overlapping-atoms')
@click.argument('cifs', type=str, nargs=-1)
def overlapping_atoms(cifs):
    """Check that there are no overlapping atoms."""
    messages = []

    for cif in cifs:
        try:
            atoms = io.read(cif)
        except Exception as exc:
            raise ValueError(f'Unable to parse file {cif}') from exc
        overlaps = geometry.get_duplicate_atoms(atoms, cutoff=0.1)
        if len(overlaps) != 0:
            messages.append(f'Overlapping atoms detected in {cif}')
    
    if messages:
       print(messages)
       sys.exit(1)

    print('No overlapping atoms found.')


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
