from pyconcepticon import Concepticon
from cldfcatalog import Config
import csv
#wl = Wordlist('LS2002_Cuona.tsv')

concepticon = Concepticon(Config.from_file().get_clone("concepticon"))
concepts = {
    c.concepticon_id: c.concepticon_gloss
    for c in concepticon.conceptlists["Sagart-2019-250"].concepts.values()
    if c.concepticon_id
}

concept_data ={}
with open('LS2002_Cuona.tsv', 'r') as csvf:
    tmp = csv.DictReader(csvf, delimiter='\t')
    for each in tmp:
        if each['CONCEPTICON_ID'] not in concept_data.keys():
            concept_data[each['CONCEPTICON_ID']] = [each['DOCULECT']]
        else:
            concept_data[each['CONCEPTICON_ID']].append(each['DOCULECT'])

with open('missing_concept_Cuona.tsv', 'w') as csvof:
    csvof.write('\t'.join(['concepticon_id', 'concepticon_gloss'+'\n']))
    for k, v in concepts.items():
        if k not in concept_data.keys():
            csvof.write('\t'.join([k,v+'\n']))
        