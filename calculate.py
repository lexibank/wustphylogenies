from lexibank_bodtstnew import Dataset as bodtstnew
from lingpy import Wordlist
from pyconcepticon import Concepticon
from cldfcatalog import Config
import csv
import re


concepticon = Concepticon(Config.from_file().get_clone("concepticon"))

concepts_dict = {
    c.concepticon_id: c.concepticon_gloss
    for c in concepticon.conceptlists["Sagart-2019-250"].concepts.values()
    if c.concepticon_id
}


columns=(
    'parameter_id',
    'concept_name',
    'language_id',
    'language_doculect',
    'language_subgroup',
    'value',
    'form',
    'segments',
    'language_glottocode',
    'concept_concepticon_id',
    'language_latitude',
    'language_longitude',
    'cognacy',
    'cogid_cognateset_id',
    'loan',
    'source',
    'notes'
    )

namespace=[
    ('concept_name', 'concept'),
    ('language_id', 'doculect'),
    ('language_subgroup', 'subgroup'),
    ('segments', 'tokens'),
    ('language_doculect', 'language_name'),
    ('language_glottocode', 'glottolog'),
    ('concept_concepticon_id', 'concepticon'),
    ('language_latitude', 'latitude'),
    ('language_longitude', 'longitude'),
    ('cognacy', 'cognacy'),
    ('cogid_cognateset_id', 'cogid'),
    ('loan', 'loan'),
    ('source', 'source'),
    ('notes', 'notes')
    ]


wl = Wordlist.from_cldf(
    bodtstnew().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    columns = columns,
    namespace = dict(namespace)
    )

# correct errors
for idx, tok in wl.iter_rows('tokens'):
    if '+ +' in ' '.join(tok):
        tok_string = ' '.join(tok).replace('+ +', '+')
        wl[idx, 'tokens'] = tok_string.split(' ')

# print the number of doculects and concepts 
print('The number of doculects: %s' % len(wl.doculect))
print('The number of concepts: %s'% len(wl.concepts))
wl.add_entries('morphemes', 'tokens', lambda x:' ')
# calculate coverages and output 
Doculect_coverage = {}
Concept_coverage = {}
for idx, doc, ln, con, tok in wl.iter_rows('doculect', 'language_name', 'concepticon', 'tokens'):
    ln_new = re.sub('\(|\)| ', '',ln)
    if doc not in Doculect_coverage.keys():
        Doculect_coverage[doc]=set([con])
    else:
        Doculect_coverage[doc].add(con)
    if con not in Concept_coverage.keys():
        Concept_coverage[con] = set([doc])
    else:
        Concept_coverage[con].add(doc)
    wl[idx, 'language_name'] =ln_new
    if '+' in tok:
        tok_array = '_'.join(tok).split('+')
        morph = wl[idx, 'parameter_id'].split('_')[1]
        wl[idx, 'morphemes']=['_'+morph for i in range(len(tok_array))]
    else:
        wl[idx, 'morphemes']=wl[idx, 'parameter_id'].split('_')[1]

#doculect coverage
print('saving language coverages')
total_concepts = len(wl.concepts)
with open('language_coverage.tsv', 'w') as of:
    fieldname = ['LANGUAGE', 'COVERAGE']
    writer=csv.DictWriter(of, delimiter='\t', fieldnames = fieldname)
    writer.writeheader()
    for k, v in Doculect_coverage.items():
        writer.writerow({'LANGUAGE':k, 'COVERAGE':len(v)/total_concepts})

#concept coverage
print('saving concept coverages')
total_doculates = len(wl.doculect)
with open('concept_coverage.tsv','w') as wf:
    fieldname = ['CONCEPTICON', 'COVERAGE']
    writer=csv.DictWriter(wf, delimiter='\t', fieldnames = fieldname)
    writer.writeheader()
    for k, v in Concept_coverage.items():
        writer.writerow({'CONCEPTICON':concepts_dict[k], 'COVERAGE':len(v)/total_doculates})


# WKB concept checking 
# WKB = ['BuluPuroik','DikhyangBugun','Duhumbi','Khispi','Khoina','Khoitam','Rahung','Rupa','Shergaon','Jerigaon']
# for k, v in Concept_coverage.items():
#     tmp = [x for x in v if x in WKB]
#     if tmp == []:
#         print('Western Kho-Bwa missing concept (100%): {}'.format(concepts_dict[k]))
#     elif len(tmp) < 5:
#         print('Western Kho-Bwa missing concept (50%): {}'.format(concepts_dict[k]))

wl.output('tsv', filename='Phylogeny_wordlist', prettify=False)