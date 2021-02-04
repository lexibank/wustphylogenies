from pandas_ods_reader import read_ods
#from pandas.DataFrame import to_dict
import glob
import csv
import re
from lingpy.align import pairwise
from segments import Profile, Tokenizer

# def alignment
def align_for_seg(ref_form, test_form):
    tmp_res = pairwise.sw_align(ref_form, test_form)
    clean = [''.join(a).replace('-','') for a in tmp_res[1] if a !=[]]
    if len(clean) <=2:
        out_form = ''.join(clean)
    elif len(clean) >=3:
        out_form = '+'.join(clean)
        out_form = out_form.replace(out_form[len(out_form)-2],'')
    else:
        out_form = '+'.join(clean)
    return out_form


df = read_ods('Bugun.ods', sheet = 1)
Concept_book = {}
with open('bugun_concept_mapped.tsv', 'r') as csvf:
    tmp = csv.DictReader(csvf, delimiter='\t')
    for each in tmp:
        if each['CONCEPTICON_ID']:
            Concept_book[each['GLOSS']] = {
                'CONCEPTICON_ID': each['CONCEPTICON_ID'], 
                'CONCEPTICON_GLOSS': each['CONCEPTICON_GLOSS']
                 }

# select syn.
syn_book = {} 
with open('Bugun_expert_selected_syn.tsv', 'r') as csvfile:
    tmp = csv.DictReader(csvfile, delimiter='\t')
    for each in tmp:
        syn_book[each['VALUE']]=each['FORM']

# expert seg. 
seg_book = {}
with open('dikhyangbugun_expert_seg.tsv', 'r') as segfile:
    tmp = csv.DictReader(segfile, delimiter='\t')
    for each in tmp:
        seg_book[each['CONCEPTICON']] = each['TOKENS']

# import orthography
prf = Profile.from_file('orthography.tsv')
bugun_tokenizer = Tokenizer(profile=prf)

data_column = [x for x in df.columns if x !='unnamed.1']
D = {}
i = 1
for idx, entry in df.iterrows():
    if entry['unnamed.1'] in Concept_book.keys():
        gloss = entry['unnamed.1']
        for col in data_column:
            doc = re.search(r'\((.*?)\)', col).group(1)+'Bugun'
            ln = col.split(' ')[0]
            if entry[col] not in ['',' ','-']:
                new_form = [syn_book.get(entry[col]) if syn_book.get(entry[col]) else entry[col]][0]
                if len(new_form)>3 and Concept_book[gloss]['CONCEPTICON_ID'] in seg_book.keys():
                    new_form = bugun_tokenizer(new_form, column='IPA')
                    ref_form = seg_book.get(Concept_book[gloss]['CONCEPTICON_ID'])
                    new_form = align_for_seg(ref_form, new_form).replace(' ','')
                D[i] = {
                    'RID':idx,
                    'GLOSS':gloss,
                    'DOCULECT': doc, 
                    'LANGUAGE_NAME':ln,
                    'CONCEPTICON_GLOSS':Concept_book[gloss]['CONCEPTICON_GLOSS'],
                    'CONCEPTICON_ID':Concept_book[gloss]['CONCEPTICON_ID'],
                    'VALUE': entry[col],
                    'FORM': new_form,
                    'SOURCE': 'Abraham'
                }
                i +=1

with open('Bugun.tsv', 'w') as of:
    fieldnames = ['RID','GLOSS','DOCULECT', 'LANGUAGE_NAME', 'CONCEPTICON_GLOSS','CONCEPTICON_ID', 'VALUE','FORM', 'SOURCE']
    writer = csv.DictWriter(of, delimiter='\t', fieldnames=fieldnames)
    writer.writeheader()
    for k, v in D.items():
        writer.writerow(v)

of.close()

# {'BangruForm', 'NafraMijiForm', 'Namrei (Bisai)', 'RurangDammaiForm', 'BisaiNamreiForm', 'Hruso Aka (Jamiri)', 'No.', 'CONCEPTICON_GLOSS', 'DibbinDammaiForm', 'Dammai (Rurang)', 'HrusoAkaForm', 'Gloss', 'Source', 'CONCEPTICON_ID', 'Notes', 'Miji (Nafra)', 'Bangru', 'Namrei (Nabolang)', 'Dammai (Dibin)', 'NabolangNamreiForm'}