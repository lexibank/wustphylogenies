from lingpy import Wordlist
from lexibank_sagartst import Dataset as sagartst
from pyconcepticon import Concepticon 
import csv

concepticon = Concepticon()

concepts = {
    c.english: {'english':c.english, 'id':c.id, 'concepticon_id':c.concepticon_id, 'concepticon_gloss': c.concepticon_gloss}
    for c in concepticon.conceptlists['Sagart-2019-250'].concepts.values()
}

wl = Wordlist.from_cldf(sagartst().cldf_dir.joinpath("cldf-metadata.json").as_posix())
for x in wl.concept:
    if x not in concepts.keys():
        print(x)

total_lang = len(wl.doculect)
concept_annotation ={}
for concept in wl.concept:
    tmp_dict = wl.get_dict(row=concept, entry ='cognacy')
    annotated_lang = []
    for k, v in tmp_dict.items():
        if v !=[]:
            if '0' not in v:
                annotated_lang.append(k)
    concept_annotation[concept] = {'percentage': len(annotated_lang)/total_lang, 'doculect':annotated_lang}

with open('sagart_list.tsv', 'w') as csvf:
    csvf.write('\t'.join(['sagart_id', 'concept', 'concepticon_id', 'concepticon_gloss', 'partcentage', 'doculects'+'\n']))
    for k, v in concept_annotation.items():
        sagart_id = concepts[k]['id']
        conc = k
        cid = concepts[k]['concepticon_id']
        cgloss = concepts[k]['concepticon_gloss']
        doc = ' '.join([x for x in v['doculect']])
        par = v['percentage']
        csvf.write('\t'.join([sagart_id, conc, cid, cgloss, str(par), doc+'\n']))

# sagartset =[]
# for concept in wl.concept:
#     tmp_dict = wl.get_dict(row=concept, entry='cognacy')
#     print(tmp_dict)
#     keyin=input('yes or no: ')
#     if keyin =='y':
#         sagartset.append(concept)