from lexibank_sagartst import Dataset as sagartst
from lingpy import Wordlist

columns=(
    'parameter_id',
    'concept_name',
    'language_id',
    'language_name',
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
    'source'
    )

namespace=[
    ('concept_name', 'concept'),
    ('language_id', 'doculect'),
    ('segments', 'tokens'),
    ('language_glottocode', 'glottolog'),
    ('concept_concepticon_id', 'concepticon'),
    ('language_latitude', 'latitude'),
    ('language_longitude', 'longitude'),
    ('cognacy', 'cognacy'),
    ('cogid_cognateset_id', 'cogid'),
    ('loan', 'loan'),
    ('source', 'source')
    ]

sagart_st = Wordlist.from_cldf(
sagartst().cldf_dir.joinpath("cldf-metadata.json").as_posix(),
columns = columns,
namespace = dict(namespace)
)
    
# cogid book    
tim_cogid = Wordlist('tim_cogid.tsv')
cogid_book = {}
for idx, doc, cid ,tok, cogid, loan, note in tim_cogid.iter_rows('doculect', 'concepticon', 'tokens', 'cogid', 'loan', 'note'):
    tok_str = ' '.join(tok)
    cogid_book[(doc,cid,tok_str)] = [cogid, loan.lower().capitalize(), note, tim_cogid[idx,'rid']]

# check sagart 
sagart_st.add_entries('notes', 'doculect', lambda x:'')
sagart_st.add_entries('rid', 'doculect', lambda x:'')
for idx, doc, cid, tok, cogid, loan in sagart_st.iter_rows('doculect','concepticon', 'tokens','cogid', 'loan'):
    st_tok_str = ' '.join(tok)
    if (doc, cid, st_tok_str) in cogid_book.keys():
        if cogid != cogid_book.get((doc, cid, st_tok_str))[0]:
            sagart_st[idx, 'cogid'] = cogid_book.get((doc, cid, st_tok_str))[0]
        if str(loan) !=  cogid_book.get((doc, cid, st_tok_str))[1]:
            sagart_st[idx, 'loan'] = cogid_book.get((doc, cid, st_tok_str))[1]
        sagart_st[idx, 'notes'] = cogid_book.get((doc, cid, st_tok_str))[2]
        sagart_st[idx, 'rid'] = cogid_book.get((doc, cid, st_tok_str))[3]

sagart_st.output('tsv', filename='sagartst', prettify=False)

