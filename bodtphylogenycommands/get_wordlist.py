"""
This script is designed to output the wordlist with cognate judgements
"""

from lexibank_bodtphylogeny import Dataset
from lingpy import Wordlist
from pyconcepticon import Concepticon
from cldfcatalog import Config
from tabulate import tabulate
import csv
import re

def register(parser):
    parser.add_argument(
        '--output',
        action='store',
        default=None,
        help = 'a label for output'
    )
    parser.add_argument(
        '--cognate_set',
        action = 'store',
        default=None,
        help = 'a wordlist with cognate judgements'
    )

def run(args):
    """
    main entry point
    """

    columns=(
    'parameter_id',
    'concept_name',
    'language_id',
    'language_doculect',
    'language_subgroup',
    'value',
    'form',
    'language_glottocode',
    'concept_concepticon_id',
    'language_latitude',
    'language_longitude',
    'cognacy',
    'loan',
    'source',
    'notes'
    )

    namespace=[
    ('concept_name', 'concept'),
    ('language_id', 'doculect'),
    ('language_subgroup', 'subgroup'),
    ('language_doculect', 'language_name'),
    ('language_glottocode', 'glottolog'),
    ('concept_concepticon_id', 'concepticon'),
    ('language_latitude', 'latitude'),
    ('language_longitude', 'longitude'),
    ('cognacy', 'cognacy'),
    ('loan', 'loan'),
    ('source', 'source'),
    ('notes', 'notes')
    ]

    ds = Dataset()
    wl = Wordlist.from_cldf(ds.dir.joinpath('cldf','cldf-metadata.json').as_posix(),
    columns = columns,
    namespace = dict(namespace)
    )

    wl.add_entries('cogid', 'cognacy', lambda x:0)
    missing_cogid_set = []
    # add cognate sets from an external version
    cgid = Wordlist(args.cognate_set)
    cgid_book = {}
    for idx, c, doc, fm, cid in cgid.iter_rows('concept','doculect', 'form', 'cogid'):
        cgid_book[(c, doc, fm)] = [cid, cgid[idx, 'cognacy']]
    
    for idx, c, doc, fm in wl.iter_rows('concept', 'doculect', 'form'):
        if doc == 'KBWestPuroikLieberherr':
            doc = 'KBBuluPuroik'
        if (c, doc, fm) in cgid_book.keys():
            wl[idx, 'cogid'] = cgid_book[(c, doc, fm)][0]
            wl[idx, 'cognacy'] = cgid_book[(c, doc, fm)][1]
        else:
            if doc not in ['MishmiKaman', 'KBEastPuroikSoja', 'KBEastPuroikRemsangpuia', 'KBEastPuroikSun']:
                missing_cogid_set.append([c, doc, fm])
    print('Cannot find the cognate sets for the following entries in our new data: ')
    print(tabulate(missing_cogid_set, headers=['concept','doculect', 'value','form']))

    print('output wordlist')
    wl.output('tsv', filename=args.output, prettify=False)