from pandas_ods_reader import read_ods
#from pandas.DataFrame import to_dict
import glob
import csv

files = glob.glob('*.ods')

# The basic structure. 
#D = {0:['RID', 'GLOSS', 'DOCULECT', 'CONCEPTICON_GLOSS', 'CONCEPTICON_ID', 'No.', 'VALUE', 'FORM', 'SOURCE', 'NOTES']}

D = {}
i = 1
for f in files:
    df = read_ods(f,1)
    column_names = df.columns
    data_column = [x for x in column_names if x not in ['No.', 'Gloss', 'CONCEPTICON_GLOSS','CONCEPTICON_ID','Source','Notes']]
    fm = [form for form in data_column if 'Form' in form] 
    vl = [v for v in data_column if 'Form' not in v]
    vl_beautified = vl[0].replace('(','').replace(')','').replace(' ','')
    for idx, row in df.iterrows():
        D[i] = {
            'RID':vl_beautified+'_'+str(row['No.']).replace('.0',''),
            'GLOSS':row['Gloss'],
            'DOCULECT':vl_beautified,
            'Language_Name': vl[0], 
            'CONCEPTICON_GLOSS': row['CONCEPTICON_GLOSS'],
            'CONCEPTICON_ID': str(int(row['CONCEPTICON_ID'])),
            'VALUE' : row[vl[0]],
            'FORM' : row[fm[0]], 
            'SOURCE' : row['Source'],
            'NOTES' : row['Notes'],
        }
        i += 1

with open('Hrusish250.tsv', 'w') as of:
    fieldnames = ['RID','GLOSS','DOCULECT', 'Language_Name', 'CONCEPTICON_GLOSS','CONCEPTICON_ID', 'VALUE','FORM', 'SOURCE',"NOTES"]
    writer = csv.DictWriter(of, delimiter='\t', fieldnames=fieldnames)
    writer.writeheader()
    for k, v in D.items():
        writer.writerow(v)

of.close()

# {'BangruForm', 'NafraMijiForm', 'Namrei (Bisai)', 'RurangDammaiForm', 'BisaiNamreiForm', 'Hruso Aka (Jamiri)', 'No.', 'CONCEPTICON_GLOSS', 'DibbinDammaiForm', 'Dammai (Rurang)', 'HrusoAkaForm', 'Gloss', 'Source', 'CONCEPTICON_ID', 'Notes', 'Miji (Nafra)', 'Bangru', 'Namrei (Nabolang)', 'Dammai (Dibin)', 'NabolangNamreiForm'}