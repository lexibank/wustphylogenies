from pyconcepticon import Concepticon
from cldfcatalog import Config
import csv

concepticon = Concepticon(Config.from_file().get_clone("concepticon"))
concepts = {
    c.concepticon_id: c.concepticon_gloss
    for c in concepticon.conceptlists["Sagart-2019-250"].concepts.values()
    if c.concepticon_id
}

concept_data =[]
with open('Bumthang_wordlist.tsv', 'r') as csvf:
    tmp = csv.DictReader(csvf, delimiter='\t')
    for each in tmp:
        concept_data.append(each['CONCEPTICON_ID'])

with open('Bumthang_missing_concepts.tsv', 'w') as of:
    of.write('\t'.join(['CONCEPTICON_ID', 'CONCEPTICON_GLOSS'+'\n']))
    for a, b in concepts.items():
        if a not in concept_data:
            of.write('\t'.join([str(a),b+'\n']))
of.close()
            