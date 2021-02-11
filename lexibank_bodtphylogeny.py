import pathlib

import attr
import re
from clldutils.misc import slug
from pylexibank import Language, Lexeme, Dataset as BaseDataset
from pylexibank.util import progressbar
from pylexibank.forms import FormSpec
from lingpy import Wordlist


@attr.s
class CustomLanguage(Language):
    Doculect = attr.ib(default=None)
    Subgroup = attr.ib(default=None)
    Source = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    NOTES = attr.ib(default=None)
    LOAN = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    language_class = CustomLanguage
    lexeme_class = CustomLexeme
    id = "bodtphylogeny"
    form_spect = FormSpec(
        separators="~;/",
        brackets={"(": ")"},
        strip_inside_brackets=True,
        first_form_only=True,
    )

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return super().cldf_specs()

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        >>> args.writer.objects['LanguageTable'].append(...)
        """

        def cbook(wl, col):
            cset = set()
            for idx, cid in wl.iter_rows(col):
                cset.add(cid)
            return cset

        # data area
        Tshangla_wl = Wordlist("raw/DirangTshangla.tsv")
        Galo_wl = Wordlist("raw/Galo.tsv")
        Tangam_wl = Wordlist("raw/Tangam.tsv")
        Dzalakha_wl = Wordlist("raw/Dzalakha.tsv")
        Hrusish_wl = Wordlist("raw/Hrusish250.tsv")
        WKB_wl = Wordlist("raw/wkb.tsv")
        Khengkha_wl = Wordlist("raw/Khengkha.tsv")
        Cuona_wl = Wordlist("raw/Cuona.tsv")
        Bumthang_wl = Wordlist("raw/Bumthang.tsv")
        Sagartst_wl = Wordlist("raw/sagartst.tsv")
        Kusunda_wl = Wordlist("raw/Kusunda.tsv")
        Bugun_wl = Wordlist("raw/Bugun.tsv")
        Kaman_wl = Wordlist("raw/Kaman250.tsv")
        Puroik_Soja_wl = Wordlist("raw/Puroik_Soja.tsv")
        Puroik_Remsangpuia_wl = Wordlist("raw/Puroik_Remsangpuia.tsv")
        Puroik_Sun_wl = Wordlist("raw/Puroik_Sun250.tsv")
        # lookup
        Tshangla_concepticon = cbook(Tshangla_wl, "concepticon_id")
        Galo_concepticon = cbook(Galo_wl, "concepticon_id")
        Tangam_concepticon = cbook(Tangam_wl, "concepticon_id")
        Dzalakha_concepticon = cbook(Dzalakha_wl, "concepticon_id")
        Hrusish_concepticon = cbook(Hrusish_wl, "concepticon_id")
        Khengkha_concepticon = cbook(Khengkha_wl, "concepticon_id")
        Cuona_concepticon = cbook(Cuona_wl, "concepticon_id")
        Bumthang_concepticon = cbook(Bumthang_wl, "concepticon_id")
        Bugun_concepticon = cbook(Bugun_wl, "concepticon_id")
        WKB_concepticon = cbook(WKB_wl, "concepticon")
        Sagartst_concepticon = cbook(Sagartst_wl, "concepticon")
        Kusunda_concepticon = cbook(Kusunda_wl, "concepticon")
        Kaman_concepticon = cbook(Kaman_wl, "concepticon_id")
        Puroik_Soja_concepticon = cbook(Puroik_Soja_wl, "concepticon_id")
        Puroik_Remsangpuia_concepticon = cbook(Puroik_Remsangpuia_wl, "concepticon_id")
        Puroik_Sun_concepticon = cbook(Puroik_Sun_wl, "concepticon_id")
        # source area
        # args.writer.add_sources()

        # concept area
        concepts_lookup = args.writer.add_concepts(
            id_factory=lambda c: c.number + "_" + slug(c.english),
            lookup_factory="concepticon_id",
        )
        # language area
        languages_lookup = args.writer.add_languages(
            id_factory=lambda l: l["ID"], lookup_factory="Name"
        )
        # start working on the actual data.
        for c in progressbar(concepts_lookup, desc="cldfify"):
            # Tshangla
            if c in Tshangla_concepticon:
                for idx, cid, fm in Tshangla_wl.iter_rows("concepticon_id", "form"):
                    if cid == c and fm not in ["", " ", "Ø"]:
                        row = args.writer.add_form(
                            Language_ID=languages_lookup[Tshangla_wl[idx, "doculect"]],
                            Local_ID=Tshangla_wl[idx, "doculect"]
                            + "_"
                            + str(Tshangla_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup[c],
                            Value=Tshangla_wl[idx, "value"],
                            Form=Tshangla_wl[idx, "form"],
                            Source=["TB"],
                            NOTES="",
                        )
            # Galo
            if c in Galo_concepticon:
                for idx, doc, cid, vl, fm in Galo_wl.iter_rows(
                    "doculect", "concepticon_id", "value", "form"
                ):
                    if cid == c and fm not in ["", " ", "Ø"]:
                        if vl in ["", " ", "Ø"]:
                            vl = fm
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(doc),
                            Local_ID=doc + "_" + str(Galo_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=fm,
                            Source=["Post07"],
                            NOTES=Galo_wl[idx, "notes"],
                        )
            # Tangam
            if c in Tangam_concepticon:
                for idx, doc, cid, vl, fm in Tangam_wl.iter_rows(
                    "doculect", "concepticon_id", "value", "form"
                ):
                    if cid == c and fm not in ["", " ", "Ø"]:
                        if vl in ["", " ", "Ø"]:
                            vl = fm
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(doc),
                            Local_ID=doc + "_" + str(Tangam_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=fm,
                            Source=Tangam_wl[idx, "source"],
                            NOTES=Tangam_wl[idx, "notes"],
                        )
            # Dzalakha
            if c in Dzalakha_concepticon:
                for idx, cid, vl, fm in Dzalakha_wl.iter_rows(
                    "concepticon_id", "value", "form"
                ):
                    if cid == c and vl != "" and fm != "":
                        row = args.writer.add_form(
                            Language_ID=languages_lookup[Dzalakha_wl[idx, "doculect"]],
                            Local_ID=Dzalakha_wl[idx, "doculect"]
                            + "_"
                            + str(Dzalakha_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup[c],
                            Value=Dzalakha_wl[idx, "value"],
                            Form=Dzalakha_wl[idx, "form"],
                            Source=Dzalakha_wl[idx, "source"],
                            NOTES=Dzalakha_wl[idx, "notes"],
                        )
            # Khengkha
            if c in Khengkha_concepticon:
                for idx, cid, doc, fm in Khengkha_wl.iter_rows(
                    "concepticon_id", "doculect", "form"
                ):
                    if cid == c and fm not in ["", " ", "Ø"]:
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(doc),
                            Local_ID=doc + "_" + str(Khengkha_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup[c],
                            Value=Khengkha_wl[idx, "value"],
                            Form=fm,
                            Source=Khengkha_wl[idx, "source"],
                            NOTES=Khengkha_wl[idx, "notes"],
                        )
            # Bugun
            if c in Bugun_concepticon:
                for idx, cid, doc, fm in Bugun_wl.iter_rows(
                    "concepticon_id", "doculect", "form"
                ):
                    if cid == c and fm not in ["", " ", "Ø", "–"]:
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(doc),
                            Local_ID=doc + "_" + str(Bugun_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup[c],
                            Value=Bugun_wl[idx, "value"],
                            Form=fm,
                            Source=Bugun_wl[idx, "source"],
                            NOTES=" ",
                        )
            # Couna
            if c in Cuona_concepticon:
                for idx, cid, doc, vl, fm in Cuona_wl.iter_rows(
                    "concepticon_id", "doculect", "value", "form"
                ):
                    if cid == c and vl not in ["", " ", "Ø"]:
                        doc = doc.replace(" ", "")
                        if fm in ["", " ", "Ø"]:
                            fm = vl
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(doc),
                            Local_ID=doc + "_" + str(Cuona_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=fm,
                            Source=Cuona_wl[idx, "source"],
                            NOTES=Cuona_wl[idx, "notes"],
                        )

            # wkb
            if c in WKB_concepticon:
                for idx, cid, vl, fm in WKB_wl.iter_rows(
                    "concepticon", "value", "form"
                ):
                    if cid == c and vl != "" and fm != "":
                        if WKB_wl[idx, "rid"] == "0" or WKB_wl[idx, "rid"] == 0:
                            new_rid = "v2" + str(idx)
                        else:
                            new_rid = WKB_wl[idx, "rid"]
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(WKB_wl[idx, "doculect"]),
                            Local_ID=WKB_wl[idx, "doculect"] + "_" + str(new_rid),
                            Parameter_ID=concepts_lookup[c],
                            Value=WKB_wl[idx, "value"],
                            Form=WKB_wl[idx, "form"],
                            Source=["TB"],
                            NOTES="",
                            LOAN=WKB_wl[idx, "loan"],
                            Cognacy=WKB_wl[idx, "cognacy"],
                        )
                        if WKB_wl[idx, "cognacy"]:
                            args.writer.add_cognate(
                                lexeme=row,
                                Cognateset_ID=WKB_wl[idx, "cognacy"],
                                Source=["TB"],
                                Alignment="",
                                Alignment_Source="",
                            )
            # Kusunda
            if c in Kusunda_concepticon:
                for idx, cid, vl, fm in Kusunda_wl.iter_rows(
                    "concepticon", "value", "form"
                ):
                    if cid == c and vl != "" and fm != "":
                        if Kusunda_wl[idx, "rid"] in ["0", 0]:
                            new_rid = "v2" + "_" + str(idx)
                        else:
                            new_rid = Kusunda_wl[idx, "rid"]
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(
                                Kusunda_wl[idx, "doculect"]
                            ),
                            Local_ID=Kusunda_wl[idx, "doculect"] + "_" + str(new_rid),
                            Parameter_ID=concepts_lookup[c],
                            Value=vl,
                            Form=fm,
                            Source=["Bodt2019b"],
                            NOTES=Kusunda_wl[idx, "notes"],
                            LOAN=Kusunda_wl[idx, "loan"],
                            Cognacy=Kusunda_wl[idx, "cogid"],
                        )
                        if Kusunda_wl[idx, "cogid"]:
                            args.writer.add_cognate(
                                lexeme=row,
                                Cognateset_ID=Kusunda_wl[idx, "cogid"],
                                Source="TB",
                                Alignment="",
                                Alignment_Source="",
                            )
            # Hrusish
            if c in Hrusish_concepticon:
                for idx, doc, cid, vl, fm in Hrusish_wl.iter_rows(
                    "doculect", "concepticon_id", "value", "form"
                ):
                    if cid == c and vl not in ["", " ", "Ø"]:
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(doc),
                            Local_ID=Hrusish_wl[idx, "rid"],
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=fm,
                            Source=Hrusish_wl[idx, "source"],
                            NOTES=Hrusish_wl[idx, "notes"],
                        )
            # Bumthang
            if c in Bumthang_concepticon:
                for idx, doc, cid, vl, fm in Bumthang_wl.iter_rows(
                    "doculect", "concepticon_id", "value", "form"
                ):
                    if cid == c and fm not in ["", " ", "Ø"]:
                        if vl in ["", " ", "Ø"]:
                            vl = fm
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(doc),
                            Local_ID=Bumthang_wl[idx, "doculect"]
                            + "_"
                            + str(Bumthang_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=fm,
                            Source=Bumthang_wl[idx, "source"],
                            NOTES="",
                        )
            # Sagart
            if c in Sagartst_concepticon:
                for idx, doc, cid, vl, fm in Sagartst_wl.iter_rows(
                    "doculect", "concepticon", "value", "form"
                ):
                    if (
                        cid == c
                        and doc in languages_lookup.keys()
                        and vl not in ["", " ", "Ø"]
                    ):
                        if Sagartst_wl[idx, "rid"] in ["0", 0, ""]:
                            new_rid = "v2" + "_" + str(idx)
                        else:
                            new_rid = Sagartst_wl[idx, "rid"]
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(
                                Sagartst_wl[idx, "doculect"]
                            ),
                            Local_ID=Sagartst_wl[idx, "doculect"] + "_" + str(new_rid),
                            Parameter_ID=concepts_lookup[c],
                            Value=vl,
                            Form=fm,
                            Source=Sagartst_wl[idx, "source"],
                            NOTES=Sagartst_wl[idx, "notes"],
                            LOAN=Sagartst_wl[idx, "loan"],
                            Cognacy=Sagartst_wl[idx, "cogid"],
                        )
                        if Sagartst_wl[idx, "cogid"]:
                            args.writer.add_cognate(
                                lexeme=row,
                                Cognateset_ID=Sagartst_wl[idx, "cogid"],
                                Source="Sagart2018",
                                Alignment="",
                                Alignment_Source="",
                            )
            # Kaman
            if c in Kaman_concepticon:
                for idx, cid, vl, fm in Kaman_wl.iter_rows(
                    "concepticon_id", "value", "form"
                ):
                    if cid == c and vl not in ["", " "]:
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get("Kaman"),
                            Local_ID=Kaman_wl[idx, "doculect"]
                            + "_"
                            + str(Kaman_wl[idx, "entryid"]),
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=fm.rstrip().replace(" ", "+"),
                            Source=["Sun1991"],
                            NOTES="",
                        )
            # Eastern Puroik (from author Soja)
            if c in Puroik_Soja_concepticon:
                for idx, cid, vl, sg in Puroik_Soja_wl.iter_rows(
                    "concepticon_id", "form", "segment"
                ):
                    if cid == c and vl not in ["", " "]:
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get("EasternPuroikSoja"),
                            Local_ID=slug(Puroik_Soja_wl[idx, "doculect"])
                            + "_"
                            + str(Puroik_Soja_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=sg,
                            Source=Puroik_Soja_wl[idx, "source"],
                            NOTES="",
                        )
            # Eastern Puroik (from author Remsangpuia)
            if c in Puroik_Remsangpuia_concepticon:
                for idx, cid, vl, fm in Puroik_Remsangpuia_wl.iter_rows(
                    "concepticon_id", "value", "form"
                ):
                    if cid == c and vl not in ["", " "]:
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get(
                                "EasternPuroikRemsangpuia"
                            ),
                            Local_ID=slug(Puroik_Remsangpuia_wl[idx, "doculect"])
                            + "_"
                            + str(Puroik_Remsangpuia_wl[idx, "rid"]),
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=fm,
                            Source=["Remsangpuia2008"],
                            NOTES="",
                        )
            # Eastern Puroik (from author Sun)
            if c in Puroik_Sun_concepticon:
                for idx, cid, vl, fm in Puroik_Sun_wl.iter_rows(
                    "concepticon_id", "form", "segment"
                ):
                    if cid == c and vl not in ["", " "]:
                        row = args.writer.add_form(
                            Language_ID=languages_lookup.get("EasternPuroikSun"),
                            Local_ID=slug(Puroik_Sun_wl[idx, "doculect"])
                            + "_"
                            + str(Puroik_Sun_wl[idx, "entryid"]),
                            Parameter_ID=concepts_lookup.get(c),
                            Value=vl,
                            Form=fm,
                            Source=["Sun1991"],
                            NOTES="",
                        )
