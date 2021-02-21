Notes:
1. The "RID" in WKB lists the entriy id of the first version cognate judgements.
2. The "cognacy" in WKB lists the the first version cognate ids
3. The "cognacy" in languages in Sagart's study lists the cognate decisions from Sagart's study 
4. In Khengkha folder the latest version is the one with "v2" filename (and it's also the one I am using for the CLDF)

How to use the commands
```Python

pip3 install -e .
cldfbench lexibank.makecldf lexibank_bodtphylogeny.py
cldfbench bodtphylogeny.check_concepts --wordlist='raw/[data name].tsv'
cldfbench bodtphylogeny.get_wordlist --output='[data name]' --cognate_set='raw/wordlist.20201216.tsv'
```
For the visualising purpose, the `get_wordlist` function removed the peculiarous markers in Sagart's segmentation. Therefore, it is only used during the data merging and curation process. The final
