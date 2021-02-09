Notes:
1. The "RID" in WKB lists the entriy id of the first version cognate judgements.
2. The "cognacy" in WKB lists the the previous version cognate ids
3. In Khengkha folder the latest version is the one with "v2" filename (and it's also the one I am using for the CLDF)

How to use the commands
```Python

pip3 install -e .
cldfbench lexibank.makecldf lexibank_bodtphylogeny.py
cldfbench bodtphylogeny.check_concepts --wordlist='raw/[data name].tsv'
cldfbench bodtphylogeny.get_wordlist --output='[data name]' --cognate_set='raw/wordlist.20201216.tsv'
```