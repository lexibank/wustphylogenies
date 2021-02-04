from lexibank_bodtnepal import Dataset as kusunda
from lingpy import Wordlist


kusunda_wordlist = Wordlist.from_cldf(
    kusunda().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
    filter=lambda row: row["language_id"] in ['KusundaK']
    )
kusunda_wordlist.add_entries('cogid','doculect', lambda x:'')
kusunda_wordlist.add_entries('loan','doculect', lambda x:False)
kusunda_wordlist.add_entries('notes', 'doculect', lambda x:'')
kusunda_wordlist.add_entries('rid', 'doculect', lambda x:'')

# tim cogid
tim_cogid = Wordlist('tim_cogid.tsv')
cogid_book = {}
for idx, doc, cid ,tok, cogid, loan, note in tim_cogid.iter_rows('doculect', 'concepticon', 'tokens', 'cogid', 'loan', 'note'):
    tok_str = ' '.join(tok)
    cogid_book[(doc,cid,tok_str)] = [cogid, loan.lower().capitalize(), note, tim_cogid[idx, 'rid']] 


for idx, doc, cid, tok in kusunda_wordlist.iter_rows('doculect','concepticon', 'tokens'):
    st_tok_str = ' '.join(tok)
    if (doc, cid, st_tok_str) in cogid_book.keys():
            kusunda_wordlist[idx, 'cogid'] = cogid_book.get((doc, cid, st_tok_str))[0]
            kusunda_wordlist[idx, 'loan'] = cogid_book.get((doc, cid, st_tok_str))[1]
            kusunda_wordlist[idx, 'notes'] = cogid_book.get((doc, cid, st_tok_str))[2]
            kusunda_wordlist[idx, 'rid'] = cogid_book.get((doc, cid, st_tok_str))[3]


kusunda_wordlist.output('tsv', filename='kusunda', prettify=False)