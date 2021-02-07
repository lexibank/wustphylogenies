"""
This script is designed to check concepts in the individual raw data
print out missing concepticon IDs 
"""

from lingpy import Wordlist
from pyconcepticon import Concepticon
from cldfcatalog import Config
from tabulate import tabulate


def register(parser):
    parser.add_argument(
        '--wordlist',
        action='store',
        default=None,
        help = 'a wordlist in raw file'
    )


def run(args):
    """
    main entry point
    """

    raw = Wordlist(args.wordlist)
    incorrect_gloss = []
    missing_gloss = []
    concept_id_wordlist = []
    concepticon = Concepticon(Config.from_file().get_clone('concepticon'))
    concept_ref ={}
    for concept in concepticon.conceptlists['Sagart-2019-250'].concepts.values():
        if concept.concepticon_id:
            concept_ref[concept.concepticon_id] = concept.concepticon_gloss
    
    for idx, cid, cgloss in raw.iter_rows('concepticon_id', 'concepticon_gloss'):
        concept_id_wordlist.append(cid)
        if cid in concept_ref.keys():
            if cgloss != concept_ref[cid]:
                incorrect_gloss.append((cid, concept_ref[cid], cgloss))
            else:
                continue
    
    for k, v in concept_ref.items():
        if k not in concept_id_wordlist:
            missing_gloss.append((k, v))
    
    print('incorrect mapping')
    print(tabulate(incorrect_gloss, headers=['CONCEPTICON_ID', 'CONCEPTICON_GLOSS', 'CONCEPTICON_GLOSS_IN_DATA']))
    print('missing concepts')
    print(tabulate(missing_gloss, headers=['CONCEPTICON_ID', 'CONCEPTICON_GLOSS']))
        

# if __name__== "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(description = 'check the concept mappings in each raw data')
#     parser.add_argument('--wordlist', help='a wordlist in the file')
#     args = parser.parse_args()
#     run(wl = args.wordlist)