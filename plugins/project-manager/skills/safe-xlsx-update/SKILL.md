---
name: safe-xlsx-update
description: Safe procedure for modifying an existing Excel workbook that already contains data someone cares about — especially one with embedded images, or one the user has edited themselves. Covers verified backups, why in-place openpyxl saves destroy workbooks with pictures, rebuild-from-data, cell-level diff verification, detecting snapshots orphaned by row deletions, and recovering a workbook that has already been truncated. Use whenever updating, patching, appending rows to, or restyling an existing .xlsx that is not disposable — registers, trackers, logs, schedules — and before any script that calls wb.save() on a file loaded from disk.
compatibility: Python with openpyxl and Pillow. Windows/network drives where Excel may hold file locks.
---

# Safe XLSX Update

Updating a workbook the user has already worked in is not the same as generating one. The file
holds their edits, and on a project drive there is often no version history behind it. This is the
procedure for changing such a file without losing it.

## The failure this exists to prevent

`openpyxl` streams embedded images from the source archive. `load_workbook()` closes that archive
when it returns, so a later `wb.save()` tries to re-read image bytes from a closed file, raises
`ValueError: I/O operation on closed file` **partway through writing**, and leaves a truncated
archive where the workbook used to be. The original is gone.

The compounding mistake is what happens next: re-running the script takes a fresh "backup" — from
the file that is now already destroyed — overwriting the only good copy.

## Procedure

### 1. Back up, and prove the backup is real

A copy you have not opened is not a backup. Assert it loads before touching the original, and
**never overwrite an existing backup with a file you may already have damaged** — timestamp it.

```python
import datetime, os, shutil, zipfile, openpyxl

stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
backup = os.path.join(BACKUP_DIR, f'{name}-{stamp}.xlsx')
shutil.copyfile(LIVE, backup)

z = zipfile.ZipFile(backup)
assert '[Content_Types].xml' in z.namelist(), 'backup is truncated'
assert z.testzip() is None, 'backup archive is corrupt'
wb = openpyxl.load_workbook(backup)          # must not raise
print('BACKUP VERIFIED', backup, os.path.getsize(backup))
```

Keep backups outside the project folder so they are never mistaken for a deliverable.

### 2. Read the live file, not your own last copy

If the user has had the file open, they have probably changed it. Diff what is on disk against
what you last wrote, and list their edits explicitly before doing anything — you are about to
build on top of them.

Their deletions are decisions, not gaps. A rebuild that regenerates sections from your own
content arrays will silently reinstate every row they removed — and they will have to remove
them again. Once the user has edited the file, wholesale regeneration is off the table: make
surgical edits against the live rows, and if a rebuild is truly unavoidable, seed it from the
live file's content, never from what you generated last time.

### 3. Rebuild from data; do not edit in place

For any workbook containing images, extract the data, then regenerate the workbook with the same
builder that produced it and re-embed images from their original source files. This is more
reliable than patching, and the output is deterministic and checkable.

If you genuinely must load-and-save a workbook with pictures, materialise the image bytes first:

```python
import io
wb = openpyxl.load_workbook(LIVE)
ws = wb.active
for im in ws._images:
    im.ref = io.BytesIO(im._data())   # detach from the archive before it closes
```

Round-trips also flatten rich text. openpyxl reads in-cell formatting runs (bold spans, mixed
fonts within one cell) as plain strings and writes them back flat — including in cells you never
touched. Count `<r>` elements in `xl/sharedStrings.xml` before any load-and-save; if any exist,
skip the round-trip entirely: rewrite only the affected `<si>` entries in `sharedStrings.xml`
(assert each is referenced by exactly one cell first) and copy every other zip entry
byte-for-byte. For text-only edits this surgical path is preferable anyway — images, anchors,
styles and rich text stay untouched by construction, and the verify diff shrinks to one file.

### 4. Verify before the file goes anywhere near the project folder

Build to a scratch path, check it, and only then copy over the original.

**Assert that only what you intended changed:**

```python
changed = Counter()
for ref in set(new) & set(old):
    for col in FIELDS:
        if new[ref][col] != old[ref][col]:
            changed[col] += 1
unexpected = {k: v for k, v in changed.items() if k not in INTENDED_COLUMNS}
assert not unexpected, f'unintended changes: {unexpected}'
```

Also confirm: row count and IDs unchanged, no dangling cross-references, every row still has its
image, and the saved file is byte-identical to the build you verified.

Two things about the saved file itself: openpyxl 3.1 writes strings inline and may omit
`xl/sharedStrings.xml` altogether, so a post-save rich-text check must treat a missing part as
"nothing to lose", not as a failure. And when Excel is on the machine, get its own verdict on the
scratch build before copying: open it hidden and read-only through COM (PowerShell
`New-Object -ComObject Excel.Application` needs no pywin32), read every `Shape.Placement` (1 =
move and size) and confirm `TopLeftCell` equals `BottomRightCell`, then `ExportAsFixedFormat` to
PDF and render a few pages to look at.

## Image integrity — two silent corruptions

### Orphans left by row deletions

Deleting a row in Excel does **not** delete a floating picture anchored to it; the image collapses
onto the row below. A workbook can end up with more images than rows, and the affected rows
display someone else's picture stacked on their own.

```python
by_row = defaultdict(list)
for im in ws._images:
    by_row[im.anchor._from.row + 1].append(im)

print('rows with >1 image:', {r: len(v) for r, v in by_row.items() if len(v) > 1})
print('images on empty rows:', [r for r in by_row if r not in data_rows])
```

Identify which image belongs by hashing against the source crops and drop the rest — do not guess
by position.

Prevent it at the source: openpyxl's default `oneCellAnchor` is Excel's "Move but don't size with
cells", which is exactly the setting that leaves orphans and lets pictures pile up when rows are
filtered. Anchor each picture as a `TwoCellAnchor(editAs='twoCell')` with `_from` and `to` both
inside its own cell (`to` = `_from` plus the picture's EMU extents) — Excel then treats it as "Move
and size with cells": deleted with its row, hidden with a filter. Keep rows tall enough that the
picture fits, or Excel will squash it.

### Wrong pairing from filename collisions

Do not key intermediate/staged image files by row ID when more than one numbering scheme is in
play (an original build, a renumbered file, an appended item). Writing `staged/CL-056.png` for a
new item silently overwrote the staged crop for a different `CL-056` and put a shopfront elevation
against a back-of-house item.

Resolve images through an explicit `row -> original source filename` map, never through a shared
folder keyed by current ID. Then audit by content, re-deriving each expected image and comparing
bytes:

```python
want = hashlib.md5(render(expected_source[ref])).hexdigest()
have = [hashlib.md5(im._data()).hexdigest() for im in by_row[row_of[ref]]]
assert want in have, f'{ref} shows the wrong snapshot'
```

Check no source is used by two rows — that reuse is the signature of this bug.

## Recovery, if a workbook is already truncated

Do not despair at `KeyError: "There is no item named '[Content_Types].xml'"`. A failed save
usually wrote the worksheet before dying on the images, and `openpyxl` writes strings inline
(`t="inlineStr"`), so the cell data is self-contained and needs no `sharedStrings.xml` or
`styles.xml`.

```python
import xml.etree.ElementTree as ET
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
root = ET.fromstring(zipfile.ZipFile(BROKEN).read('xl/worksheets/sheet1.xml'))
for row in root.iter(f'{NS}row'):
    for c in row.iter(f'{NS}c'):
        t = c.find(f'{NS}is/{NS}t') if c.get('t') == 'inlineStr' else c.find(f'{NS}v')
        ...
```

Parse the values out, rebuild with the normal builder, re-embed images from source, then prove the
recovery by asserting **every** salvaged cell reappears in the rebuilt file. Report the count —
"636 of 636 cells reproduced" is verification; "looks right" is not. Formatting applied by hand in
Excel will not survive; say so plainly rather than implying a lossless restore.

## Locked files

`PermissionError` on read means Excel has it open exclusively. Do not retry in a loop and do not
work around it by writing elsewhere and hoping. Copy-then-read fails too. Say the file is open and
ask for it to be closed. Never assume a lock has cleared — re-test it.

Excel COM is worse than python here: it does not throw on a locked workbook — it opens your
instance **read-only**, and with `DisplayAlerts = $false` the later `Save()` silently discards
everything while your script prints success. Check for the `~$` lock file before opening, assert
`$wb.ReadOnly -eq $false` immediately after `Open`, and abort if either says otherwise. Then
verify the write landed by re-reading the file — a save you have not read back is a claim, not a
fact.

## Error signatures

| Symptom | Cause | Action |
|---|---|---|
| `ValueError: I/O operation on closed file` during `save()` | images streaming from a closed archive | file is now truncated — recover, do not re-run |
| `KeyError: '[Content_Types].xml'` | truncated/partial archive | salvage `sheet1.xml`, rebuild |
| `PermissionError` on read or copy | Excel holds an exclusive lock | ask the user to close it |
| More images than data rows | rows deleted in Excel | drop orphans by content hash |
| `IndexError` in `_cell_styles` on load | stub `styles.xml` lacking a default | parse the sheet XML directly instead |
| In-cell bold/mixed formatting gone after save | openpyxl round-trip flattens rich text | restore from backup; redo via surgical `sharedStrings.xml` edit |
| Item number "1.10" displays as "1.1" | Excel COM `Value2` coerces dotted strings to floats | set `NumberFormat = "@"` on the column before writing, then read back and verify the strings |
| Rows the user deleted are back after an update | rebuild regenerated sections from your previous content arrays | restore their state from backup; redo as surgical edits on the live rows |
| COM `Save()` reports success but the file is unchanged | workbook open elsewhere — COM opened read-only and `DisplayAlerts=$false` discarded the save | check for the `~$` lock and `$wb.ReadOnly` after Open; re-read the file to prove any write landed |

## Reporting

State what changed, what was verified and how, and where the backup is. If you damaged the file,
say so plainly and first — before describing the recovery.

## Keeping this skill current

When the user corrects, refines, or adds to what this skill produced — a changed judgement, a house
convention, a trap you fell into — record the lesson before you finish the turn, then say in one line
what you recorded and where. The point is that the next run starts from the corrected behaviour
instead of repeating the mistake.

This skill ships inside the `project-manager` plugin, and the installed copy is replaced on every
update — never edit it in place. If the user maintains the plugin (their instructions name its
source folder), edit the source copy of this file. Otherwise record the lesson in the PM project's
`lessons.md` when working under the PM, or tell the user it is worth proposing upstream.

Record only what generalises: a rule, a convention, a recurring trap, a standing preference. Do **not**
record one-off project facts, file paths, or anything already obvious from the inputs. Keep each addition
terse and in the existing voice, and edit or replace the relevant line rather than appending a
near-duplicate — a skill that grows on every correction stops being read.

If the correction is genuinely specific to that one project rather than general, say so and leave the
skill unchanged.
