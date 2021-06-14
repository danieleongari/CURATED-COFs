#!/usr/bin/env python
"""Check consistency of CURATED COF database"""

import sys
import pandas
import click
import collections
import warnings
from pathlib import Path

from ase import io, geometry
from pymatgen.io.cif import CifParser
from mofchecker import MOFChecker

SCRIPT_PATH = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_PATH.parent
CIFS_DIR = ROOT_DIR / 'cifs'

FRAMEWORKS_CSV = ROOT_DIR /  'cof-frameworks.csv'
FRAMEWORKS_DISCARDED_CSV = ROOT_DIR / 'cof-discarded.csv'
PAPERS_CSV = ROOT_DIR / 'cof-papers.csv'

FRAMEWORKS_DF = pandas.read_csv(FRAMEWORKS_CSV)
FRAMEWORKS_DISCARDED_DF = pandas.read_csv(FRAMEWORKS_DISCARDED_CSV)
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

@cli.command('consistent-paper-ids')
def consistent_paper_ids():
    """Check that papers corresponding to CURATED-COF-IDs are all deposited.
    
    Also check whether any of the papers in cof-papers.csv have no associated structure.
    """
    paper_ids = PAPERS_DF['CURATED-COFs paper ID'].str.lower()
    cof_ids = list(FRAMEWORKS_DF['CURATED-COFs ID'].str.lower()) + list(FRAMEWORKS_DISCARDED_DF['CURATED-COFs ID'].str.lower())
    cof_ids_paper_ids = { cof_id: f'p{cof_id[:4]}' for cof_id in cof_ids }
    paper_ids_set = set(cof_ids_paper_ids.values())
    
    if  paper_ids_set == set(paper_ids):
        print('Set of paper IDs from cof-papers.csv and cof-frameworks.csv (+ cof-discarded.csv) agree.')
        return

    messages = []
    for paper_id in paper_ids:
        if paper_id not in paper_ids_set:
            messages.append(f'Paper {paper_id} has no associated structure.')
        else:
            paper_ids_set.remove(paper_id)

    for paper_id in paper_ids_set:
        messages.append(f'Paper {paper_id} is missing in cof-papers.csv.')

    if messages:
       print('\n'.join(messages))
       sys.exit(1)

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

@cli.command('match-cifs')
def validate_matching_cifs():
    """Check that all frameworks have a matching CIF."""
    ids = list(FRAMEWORKS_DF['CURATED-COFs ID'].values) + list(FRAMEWORKS_DISCARDED_DF['CURATED-COFs ID'].values)
    cifs = [ p.name for p in CIFS_DIR.glob('*.cif') ]

    messages = []
    for id in ids:
        fname = f'{id}.cif'
        if fname in cifs:
            cifs.remove(fname)
        else:
            messages.append(f'CIF file for COF {id} missing.')

    for cif in cifs:
        messages.append(f'Unreferenced CIF file {cif}')

    if messages:
       print('\n'.join(messages))
       sys.exit(1)

    print('All frameworks in cof-frameworks.csv have a matching CIF.')

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
       print('\n'.join(messages))
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

@cli.command('unique-structures')
@click.argument('cifs', type=str, nargs=-1)
def unique_structures(cifs):
    """Check if structures are unique.

    Uses the mofchecker to compare the atom graph of all structures, making sure that they are unique.
    """
    hashes = {}
    errors = []
    
    for cif in cifs:

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            structure = CifParser(
                cif,
                occupancy_tolerance=1000,  # CSD overspecifies equivalent sites
            ).get_structures(primitive=True)[0]

        if len(structure) > 1000:
            print(f'Skipping structure graph for {cif} with {len(structure)} atoms')
            continue

        print(f'Computing structure graph for {cif} with {len(structure)} atoms')
        mofchecker = MOFChecker(structure)
        graph_hash = mofchecker.graph_hash

        if graph_hash in hashes:
            errors.append(f'Warning: {cif} and {hashes[graph_hash]} have the same structure graph hash')
        else:
            hashes[graph_hash] = cif

    if errors:
       print('\n'.join(errors))
       sys.exit(1)

if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
