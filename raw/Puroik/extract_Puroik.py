from pyconcepticon import Concepticon
from cldfcatalog import Config
from lingpy import Wordlist
from bs4 import BeautifulSoup


# read in data
with open('Puroik_Sun.html', 'r') as hf:
    html_doc = hf.read()


tmp = BeautifulSoup(html_doc, 'html.parser').find_all('tr')
with open('Puroik_html2tsv.tsv', 'w') as tf:
    tf.write('\t'.join(['ENTRYID','form','gloss','gfn','language', 'source', 'srcid', 'note\n']))
    for each in tmp:
        data_entry = each.find_all('td')
        data_array = [x.get_text() for x in data_entry ]
        actual_data = [data_array[0], data_array[2], data_array[3], data_array[5], data_array[9],data_array[11]]
        tf.write('\t'.join(actual_data)+'\n')