from pyconcepticon import Concepticon 
import csv

concepticon = Concepticon()

concepts = {
    c.id: {'concepticon_id':c.concepticon_id, 'concepticon_gloss': c.concepticon_gloss}
    for c in concepticon.conceptlists['Sagart-2019-250'].concepts.values()
    if c.concepticon_id
}


output_book = {}
non_missing = []
with open('Hrusish_mapping.tsv', 'r') as csvf:
    tmp = csv.DictReader(csvf, delimiter='\t')
    for each in tmp:
        if each['CONCEPTICON_GLOSS'] =='' or each['CONCEPTICON_GLOSS'] =='???':
            output_book[each['GLOSS']] = ['', '']
        else:
            concepticon_id = concepts[each['CONCEPTICON_ID']]['concepticon_id']
            concepticon_gloss = concepts[each['CONCEPTICON_ID']]['concepticon_gloss']
            output_book[each['GLOSS']] = [concepticon_id, concepticon_gloss]
            non_missing.append(concepticon_id) 

with open('missing_concept_Hrusish.tsv', 'w') as of:
    of.write('\t'.join(['CONCEPTICON_ID', 'CONCEPTCION_GLOSS'+'\n']))
for k, v in concepts.items():
    if v['concepticon_id'] not in non_missing:
        of.write('\t'.join([k,v+'\n']))

        

