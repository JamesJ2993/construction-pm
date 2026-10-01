#!/usr/bin/env python3
"""Apply the firm's letterhead to a .docx (or .dotx) package.

The letterhead is any .docx the firm supplies - set it once as ``report.letterhead`` in the
project's config.json and pass it here as ``--source``. Its first-page and default headers and
footers, the images they use, and its page margins are injected into each target, replacing the
headers and footers the target already carries. Injected parts use reserved ``inv*`` names so they
can never collide with a target's own parts, and their presence doubles as the idempotency marker.

No letterhead configured is a valid state, not an error: ``--check`` reports ``n/a`` and passes,
and an apply run reports ``skipped``. A deliverable built without a letterhead is plain, not broken.

Usage:
    python apply-letterhead.py <target.docx> [more...] --source <letterhead.docx> [options]
    python apply-letterhead.py <target.docx> --config <state>/config.json [options]

    --source P    The letterhead package.
    --config P    A project config.json; its report.letterhead is used as --source.
    --check       Report-only. Exit 0 if every target carries the letterhead (or none is
                  configured), 1 otherwise. Never writes.
    --force       Re-apply even when the inv* marker parts already exist.
    --no-backup   Skip the <name>.docx.bak sidecar.

One status line per file: applied | already-letterheaded | skipped | check-pass | check-fail |
n/a. Non-zero exit on any failure.
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

W = "{%s}" % W_NS
R = "{%s}" % R_NS
REL = "{%s}" % REL_NS
CT = "{%s}" % CT_NS

REL_HEADER = R_NS + "/header"
REL_FOOTER = R_NS + "/footer"
REL_IMAGE = R_NS + "/image"
CT_HEADER = "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"
CT_FOOTER = "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"
IMAGE_TYPES = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "gif": "image/gif",
               "emf": "image/x-emf", "wmf": "image/x-wmf", "bmp": "image/bmp"}

# Injected part names - reserved, collision-proof, and the idempotency marker.
INV_PARTS = {
    "header_first": "word/invHeader1.xml",
    "header_default": "word/invHeader2.xml",
    "footer_first": "word/invFooter1.xml",
    "footer_default": "word/invFooter2.xml",
}
INV_RIDS = {
    "header_first": "rIdInvH1",
    "header_default": "rIdInvH2",
    "footer_first": "rIdInvF1",
    "footer_default": "rIdInvF2",
}

# CT_SectPr child order per the WordprocessingML schema - needed for ordered inserts.
SECTPR_ORDER = [
    "headerReference", "footerReference", "footnotePr", "endnotePr", "type",
    "pgSz", "pgMar", "paperSrc", "pgBorders", "lnNumType", "pgNumType", "cols",
    "formProt", "vAlign", "noEndnote", "titlePg", "textDirection", "bidi",
    "rtlGutter", "docGrid", "printerSettings", "sectPrChange",
]
MARGIN_ATTRS = ("top", "bottom", "left", "right", "header", "footer")


def _xml(root) -> bytes:
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def _rels_name(part: str) -> str:
    folder, name = part.rsplit("/", 1)
    return f"{folder}/_rels/{name}.rels"


def load_source(source: Path) -> dict:
    """Pull headers, footers, their images and the page margins out of the letterhead."""
    with zipfile.ZipFile(source) as z:
        names = set(z.namelist())
        doc = etree.fromstring(z.read("word/document.xml"))
        rels = etree.fromstring(z.read("word/_rels/document.xml.rels"))
        targets = {r.get("Id"): "word/" + r.get("Target").lstrip("/").removeprefix("word/")
                   for r in rels.iter(REL + "Relationship")}
        sectprs = list(doc.iter(W + "sectPr"))
        if not sectprs:
            raise ValueError(f"{source.name}: no section properties - not a usable letterhead")
        sect = sectprs[-1]

        refs = {}
        for tag, kind in (("headerReference", "header"), ("footerReference", "footer")):
            for ref in sect.findall(W + tag):
                refs[f"{kind}_{ref.get(W + 'type', 'default')}"] = targets.get(ref.get(R + "id"))
        for kind in ("header", "footer"):
            refs.setdefault(f"{kind}_default", refs.get(f"{kind}_first"))
            refs.setdefault(f"{kind}_first", refs.get(f"{kind}_default"))
        if not refs.get("header_default") and not refs.get("footer_default"):
            raise ValueError(f"{source.name}: carries no header or footer to apply")

        parts, media, n = {}, {}, 0
        for key in INV_PARTS:
            part = refs.get(key)
            if not part or part not in names:
                continue
            parts[key] = z.read(part)
            rels_name = _rels_name(part)
            if rels_name in names:
                prel = etree.fromstring(z.read(rels_name))
                for rel in prel.iter(REL + "Relationship"):
                    if rel.get("Type") == REL_IMAGE and rel.get("TargetMode") != "External":
                        src_media = "word/" + rel.get("Target").lstrip("/").removeprefix("word/")
                        if src_media not in media:
                            n += 1
                            ext = src_media.rsplit(".", 1)[-1].lower()
                            media[src_media] = (f"word/media/invMedia{n}.{ext}", z.read(src_media))
                        rel.set("Target", media[src_media][0].removeprefix("word/"))
                parts[key + "_rels"] = _xml(prel)

        pgmar = sect.find(W + "pgMar")
        margins = {a: pgmar.get(W + a) for a in MARGIN_ATTRS if pgmar is not None and pgmar.get(W + a)}

    return {"parts": parts, "media": list(media.values()), "margins": margins,
            "fingerprints": {data for _name, data in media.values()}}


def is_letterheaded(z: zipfile.ZipFile, src: dict) -> bool:
    names = set(z.namelist())
    if any(p in names for p in INV_PARTS.values()):
        return True
    # A document built on the letterhead itself carries the same images under its own names.
    for name in names:
        if name.startswith("word/media/"):
            info = z.getinfo(name)
            for fp in src["fingerprints"]:
                if info.file_size == len(fp) and z.read(name) == fp:
                    return True
    return False


def ordered_insert(sectpr, element):
    tag = etree.QName(element).localname
    rank = SECTPR_ORDER.index(tag)
    for i, child in enumerate(sectpr):
        child_tag = etree.QName(child).localname
        if child_tag in SECTPR_ORDER and SECTPR_ORDER.index(child_tag) > rank:
            sectpr.insert(i, element)
            return
    sectpr.append(element)


def rewrite_document_xml(doc_bytes: bytes, src: dict) -> tuple[bytes, set]:
    """Repoint every sectPr at the injected headers/footers; apply the letterhead margins."""
    root = etree.fromstring(doc_bytes)
    old_rids = set()
    sectprs = list(root.iter(W + "sectPr"))
    if not sectprs:
        raise ValueError("document.xml has no sectPr")
    present = src["parts"]

    for idx, sectpr in enumerate(sectprs):
        for tag in ("headerReference", "footerReference"):
            for ref in sectpr.findall(W + tag):
                old_rids.add(ref.get(R + "id"))
                sectpr.remove(ref)
        for tag, kind in (("headerReference", "header"), ("footerReference", "footer")):
            for hf_type in ("first", "default"):
                key = f"{kind}_{hf_type}"
                if key not in present:
                    continue
                ref = etree.Element(W + tag)
                ref.set(W + "type", hf_type)
                ref.set(R + "id", INV_RIDS[key])
                ordered_insert(sectpr, ref)
        if idx == 0 and sectpr.find(W + "titlePg") is None:
            ordered_insert(sectpr, etree.Element(W + "titlePg"))
        if src["margins"]:
            pgmar = sectpr.find(W + "pgMar")
            if pgmar is None:
                pgmar = etree.Element(W + "pgMar")
                ordered_insert(sectpr, pgmar)
            for attr, val in src["margins"].items():
                pgmar.set(W + attr, val)

    old_rids.discard(None)
    return _xml(root), old_rids


def rewrite_document_rels(rels_bytes: bytes, old_rids: set, src: dict) -> tuple[bytes, set]:
    root = etree.fromstring(rels_bytes)
    orphaned = set()
    for rel in list(root.iter(REL + "Relationship")):
        if rel.get("Id") in old_rids and rel.get("Type") in (REL_HEADER, REL_FOOTER):
            target = rel.get("Target").lstrip("/")
            orphaned.add(target if target.startswith("word/") else "word/" + target)
            root.remove(rel)
    for rel in list(root.iter(REL + "Relationship")):
        if rel.get("Id") in INV_RIDS.values():
            root.remove(rel)
    for key, rid in INV_RIDS.items():
        if key not in src["parts"]:
            continue
        rel = etree.SubElement(root, REL + "Relationship")
        rel.set("Id", rid)
        rel.set("Type", REL_HEADER if "header" in key else REL_FOOTER)
        rel.set("Target", INV_PARTS[key].removeprefix("word/"))
    return _xml(root), orphaned


def rewrite_content_types(ct_bytes: bytes, removed_parts: set, src: dict) -> bytes:
    root = etree.fromstring(ct_bytes)
    have = {d.get("Extension", "").lower() for d in root.findall(CT + "Default")}
    for name, _data in src["media"]:
        ext = name.rsplit(".", 1)[-1].lower()
        if ext not in have and ext in IMAGE_TYPES:
            d = etree.Element(CT + "Default")
            d.set("Extension", ext)
            d.set("ContentType", IMAGE_TYPES[ext])
            root.insert(0, d)
            have.add(ext)
    removed_partnames = {"/" + p for p in removed_parts}
    for o in list(root.findall(CT + "Override")):
        if o.get("PartName") in removed_partnames:
            root.remove(o)
    existing = {o.get("PartName") for o in root.findall(CT + "Override")}
    for key in INV_PARTS:
        if key not in src["parts"]:
            continue
        partname = "/" + INV_PARTS[key]
        if partname not in existing:
            o = etree.SubElement(root, CT + "Override")
            o.set("PartName", partname)
            o.set("ContentType", CT_HEADER if "header" in key else CT_FOOTER)
    return _xml(root)


def strip_even_and_odd(settings_bytes: bytes) -> bytes:
    root = etree.fromstring(settings_bytes)
    found = root.findall(W + "evenAndOddHeaders")
    for el in found:
        root.remove(el)
    return _xml(root) if found else settings_bytes


def apply(target: Path, src: dict, force: bool, backup: bool) -> str:
    with zipfile.ZipFile(target) as z:
        if not force and is_letterheaded(z, src):
            return "already-letterheaded"
        names = z.namelist()
        contents = {n: z.read(n) for n in names}
        infos = {n: z.getinfo(n) for n in names}

    doc_xml, old_rids = rewrite_document_xml(contents["word/document.xml"], src)
    rels_xml, orphaned = rewrite_document_rels(contents["word/_rels/document.xml.rels"], old_rids, src)

    orphaned -= set(INV_PARTS.values())
    removed = set()
    for part in orphaned:
        for victim in (part, _rels_name(part)):
            if victim in contents:
                del contents[victim]
                removed.add(victim)

    contents["[Content_Types].xml"] = rewrite_content_types(
        contents["[Content_Types].xml"], {p for p in removed if p.endswith(".xml")}, src)
    contents["word/document.xml"] = doc_xml
    contents["word/_rels/document.xml.rels"] = rels_xml
    if "word/settings.xml" in contents:
        contents["word/settings.xml"] = strip_even_and_odd(contents["word/settings.xml"])

    for key, part in INV_PARTS.items():
        if key in src["parts"]:
            contents[part] = src["parts"][key]
            if key + "_rels" in src["parts"]:
                contents[_rels_name(part)] = src["parts"][key + "_rels"]
    for name, data in src["media"]:
        contents[name] = data

    if backup:
        shutil.copy2(target, target.with_name(target.name + ".bak"))

    fd, tmp_name = tempfile.mkstemp(suffix=".docx", dir=str(target.parent))
    os.close(fd)
    tmp = Path(tmp_name)
    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            ordering = ["[Content_Types].xml"] + \
                [n for n in infos if n in contents and n != "[Content_Types].xml"] + \
                [n for n in contents if n not in infos]
            for name in ordering:
                z.writestr(name, contents[name])
        with zipfile.ZipFile(tmp) as z:
            if z.testzip() is not None:
                raise RuntimeError("zip integrity check failed")
        import docx  # deferred - only needed on the write path
        docx.Document(str(tmp))
        os.replace(tmp, target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return "applied"


def resolve_source(args) -> Path | None:
    if args.source:
        return args.source
    if args.config:
        cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
        lh = (cfg.get("report") or {}).get("letterhead")
        return Path(lh) if lh else None
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("targets", nargs="+", type=Path)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--source", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args(argv)

    source = resolve_source(args)
    if source is None:
        for target in args.targets:
            print(f"{target.name}: {'n/a' if args.check else 'skipped'} (no letterhead configured)")
        return 0
    if not source.is_file():
        print(f"error: letterhead not found: {source}", file=sys.stderr)
        return 2
    src = load_source(source)

    failed = False
    for target in args.targets:
        if not target.is_file():
            print(f"{target.name}: check-fail (file not found)")
            failed = True
            continue
        try:
            if args.check:
                with zipfile.ZipFile(target) as z:
                    ok = is_letterheaded(z, src)
                print(f"{target.name}: {'check-pass' if ok else 'check-fail'}")
                failed = failed or not ok
            else:
                print(f"{target.name}: {apply(target, src, args.force, backup=not args.no_backup)}")
        except Exception as exc:
            print(f"{target.name}: check-fail ({exc})")
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
