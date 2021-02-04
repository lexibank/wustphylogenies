import csv
from pyconcepticon import Concepticon
from cldfcatalog import Config
import re

concepticon = Concepticon(Config.from_file().get_clone("concepticon"))
concepts = {
    c.id: {
        "concepticon_id": c.concepticon_id,
        "concepticon_gloss": c.concepticon_gloss,
        "number": c.number,
        "english": c.english,
    }
    for c in concepticon.conceptlists["Sagart-2019-250"].concepts.values()
    if c.id
}

Hrusish_concept = {}
with open("Hrusish_mapped.tsv", "r") as csvf:
    tmp = csv.DictReader(csvf, delimiter="\t")
    for each in tmp:
        if each["CONCEPTICON_ID"] in concepts.keys():
            real_concepticon_id = concepts[each["CONCEPTICON_ID"]]["concepticon_id"]
            real_concepticon_gloss = concepts[each["CONCEPTICON_ID"]][
                "concepticon_gloss"
            ]
            Hrusish_concept[each["GLOSS"]] = [
                real_concepticon_id,
                real_concepticon_gloss,
            ]

Hrusish_data = {}
with open("Hrusish_raw.tsv", "r") as df:
    tmp = csv.DictReader(df, delimiter="\t")
    for e in tmp:
        if e["concept"] in Hrusish_concept.keys():
            if e["form"] != "" or e["form"] != "Ø":
                Hrusish_data[e["RID"]] = {
                        "RID": e["RID"],
                        "DOCULECT": e["doculect"],
                        "CONCEPT": e["concept"],
                        "CONCEPTICON_GLOSS": Hrusish_concept[e["concept"]][1],
                        "PARAMETER_ID": "",
                        "CONCEPTICON_ID": Hrusish_concept[e["concept"]][0],
                        "VALUE": e["value"],
                        "FORM": e['form'],
                        "SOURCE": '',
                        "NOTES": '',
                        "SEGMENTS": "",
                        }
with open("../Hrusish.tsv", "w") as of:
    fd = [
        "RID",
        "DOCULECT",
        "CONCEPT",
        "CONCEPTICON_GLOSS",
        "PARAMETER_ID",
        "CONCEPTICON_ID",
        "VALUE",
        "FORM",
        "SOURCE",
        "NOTES",
        "SEGMENTS",
    ]
    writer = csv.DictWriter(of, delimiter="\t", fieldnames=fd)
    writer.writeheader()
    for k, v in Hrusish_data.items():
        writer.writerow(v)

# with open('Hrusish_missing.tsv', 'w') as of:
#     fn = ['concepticon_id', 'concepticon_gloss']
#     writer = csv.DictWriter(of,delimiter='\t' , fieldnames=fn)
#     writer.writeheader()
#     for k, v in concepts.items():
#         if k not in Hrusish_concept:
#             writer.writerow(v)
# of.close()
