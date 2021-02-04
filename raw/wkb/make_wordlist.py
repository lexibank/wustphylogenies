import lingpy
import csv
import re
import argparse
from lingpy import * 
from lingpy import Wordlist
from pyconcepticon import Concepticon
from cldfcatalog import Config
from lexibank_bodtst import Dataset as bodtst
from lexibank_bodtnepal import Dataset as kusunda
from lexibank_sagartst import Dataset as sagart
from pycldf.dataset import Dataset as borrowing_info

concepticon = Concepticon(Config.from_file().get_clone("concepticon"))

tim_st = Wordlist.from_cldf(
    bodtst().cldf_dir.joinpath("cldf-metadata.json").as_posix()
    )
wkb_language = [x for x in tim_st.doculect]

tim_st.add_entries('loan', 'doculect', lambda x:'False')
tim_st.add_entries('rid', 'doculect', lambda x:'0')

tim_cogid_book ={}
with open('tim_cogid.tsv', 'r') as csvf:
    tmp = csv.DictReader(csvf, delimiter='\t')
    for each in tmp:
        if each['DOCULECT'] in wkb_language:
            concepticon_id = each['CONCEPTICON']
            doculect = each['DOCULECT']
            tokens = each['TOKENS']
            tim_cogid_book[(concepticon_id, doculect, tokens)] = [each['ID'],each['COGID'], each['LOAN']]

for idx, doc, concept_id, tok in tim_st.iter_rows('doculect', 'concepticon', 'tokens'):
    if (concept_id, doc, ' '.join(tok)) in tim_cogid_book.keys():
        tim_st[idx, 'loan'] = tim_cogid_book[(concept_id, doc, ' '.join(tok))][2]
        tim_st[idx, 'cognacy'] = tim_cogid_book[(concept_id, doc,' '.join(tok))][1]
        tim_st[idx, 'rid'] = tim_cogid_book[(concept_id, doc,' '.join(tok))][0]

for idx, tok in tim_st.iter_rows('tokens'):
    if '+ +' in ' '.join(tok):
        tim_st[idx, 'tokens'] = ' '.join(tok).replace('+ +','+').split(' ')

tim_st.output('tsv', filename='WKB', prettify=False)
