#!/usr/bin/env python3
"""Turn a ``[[TOC]]`` marker in a .docx into a live Word table of contents.

House rule: every client deliverable carries a contents page.
``md-to-docx.py`` has no notion of a TOC -- it is a format converter and stays
one -- so this script runs after it and swaps the marker for a real
``TOC \\o "1-3" \\h \\z \\u`` field.

Word builds the entries from the heading styles already in the document. The
field is written with ``w:dirty="true"``, so Word offers to update it the first
time the document is opened; ``Ctrl+A`` then ``F9`` refreshes it any time after.
Until it is updated the placeholder line shows instead of page numbers -- that
is the field behaving normally, not a broken document.

Usage:
    python insert-toc.py <target.docx> [more...] [options]

    --marker M    Marker paragraph text. Default ``[[TOC]]``.
    --heading H   Heading text placed above the field. Default ``Contents``.
                  Pass an empty string to suppress it.
    --levels L    Heading levels included. Default ``1-3``.
    --check       Report-only. Exit 0 if every target already carries a TOC
                  field, 1 otherwise. Never writes.
    --no-backup   Skip the <name>.docx.bak sidecar.

One status line per file: inserted | no-marker | already-has-toc | check-pass |
check-fail. Non-zero exit on any failure.

Deterministic: no network, no model, no judgement.
"""

import argparse
import shutil
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PLACEHOLDER = "Right-click here and choose Update Field to build the contents."


def has_toc(doc):
    """True if the document already carries a TOC field instruction."""
    for instr in doc.element.body.iter(qn("w:instrText")):
        if instr.text and instr.text.strip().upper().startswith("TOC"):
            return True
    return False


def build_field(paragraph, levels):
    """Replace a paragraph's runs with a TOC field code and its placeholder."""
    p = paragraph._p
    for child in list(p):
        if child.tag in (qn("w:r"), qn("w:hyperlink")):
            p.remove(child)

    def run(*children):
        r = OxmlElement("w:r")
        for child in children:
            r.append(child)
        p.append(r)
        return r

    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    begin.set(qn("w:dirty"), "true")
    run(begin)

    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = ' TOC \\o "%s" \\h \\z \\u ' % levels
    run(instr)

    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    run(separate)

    text = OxmlElement("w:t")
    text.text = PLACEHOLDER
    run(text)

    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run(end)


def process(path, marker, heading, levels, check, backup):
    doc = Document(path)

    if check:
        ok = has_toc(doc)
        print("%s: %s" % (Path(path).name, "check-pass" if ok else "check-fail"))
        return 0 if ok else 1

    if has_toc(doc):
        print("%s: already-has-toc" % Path(path).name)
        return 0

    target = next((p for p in doc.paragraphs if p.text.strip() == marker), None)
    if target is None:
        print("%s: no-marker" % Path(path).name)
        return 1

    if backup:
        shutil.copyfile(path, "%s.bak" % path)

    if heading:
        head = target.insert_paragraph_before(heading)
        head.style = doc.styles["Heading 1"]

    target.style = doc.styles["Normal"]
    build_field(target, levels)
    doc.save(path)
    print("%s: inserted" % Path(path).name)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--marker", default="[[TOC]]")
    ap.add_argument("--heading", default="Contents")
    ap.add_argument("--levels", default="1-3")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-backup", dest="backup", action="store_false")
    args = ap.parse_args(argv)

    failures = 0
    for target in args.targets:
        if not Path(target).is_file():
            print("%s: not-found" % target)
            failures += 1
            continue
        failures += process(target, args.marker, args.heading, args.levels,
                            args.check, args.backup)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
