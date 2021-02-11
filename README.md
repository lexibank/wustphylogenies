# Investigating the internal and external phylogenetics of three Trans-Himalayan subgroups: Kho-Bwa, Hrusish and Bodish


Conceptlists in Concepticon:
- [Sagart-2019-250](https://concepticon.clld.org/contributions/Sagart-2019-250)
## Notes

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


## Statistics


[![Build Status](https://travis-ci.org/seagal-project/bodtphylogeny_data.svg?branch=master)](https://travis-ci.org/seagal-project/bodtphylogeny_data)
![Glottolog: 100%](https://img.shields.io/badge/Glottolog-100%25-brightgreen.svg "Glottolog: 100%")
![Concepticon: 100%](https://img.shields.io/badge/Concepticon-100%25-brightgreen.svg "Concepticon: 100%")
![Source: 100%](https://img.shields.io/badge/Source-100%25-brightgreen.svg "Source: 100%")

- **Varieties:** 86
- **Concepts:** 250
- **Lexemes:** 19,869
- **Sources:** 44
- **Synonymy:** 1.04
- **Cognacy:** 14,630 cognates in 4,905 cognate sets (2,722 singletons)
- **Cognate Diversity:** 0.24

## Possible Improvements:



- Entries missing sources: 1/19869 (0.01%)