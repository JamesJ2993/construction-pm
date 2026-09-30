---
name: highlight-sow-clarifications
description: Cross-reference clarification/RFI references (CL-001, RFI-12, etc.) cited in a Scope of Works or tender Word document against a Clarifications Register Excel workbook, then visibly highlight each reference in the live open documents using COM automation — scrolling to every hit so the user can watch the work happen. Use this whenever the user asks to check, highlight, mark up, or cross-reference clarifications, RFIs, or register items against a scope of works, tender document, or specification — even phrased loosely, like "which clarifications are in the SOW", "highlight the clarifications in section 7", or "mark the register items used in the tender".
compatibility: Windows with desktop Word and Excel installed (COM automation); Python with python-docx and openpyxl for fast extraction.
---

# Highlight SOW Clarifications

Cross-references clarification citations in a construction tender Scope of Works (Word) against a Clarifications Register (Excel), highlighting them **visibly in the live open applications** so the user can watch each step. This is a demonstrative workflow, not a batch job — the user wants to see the documents scroll and light up.

## Why COM, not file editing

The user watches the work happen. Editing the .docx/.xlsx on disk (python-docx/openpyxl) is invisible and fails on files locked by open Office windows. Instead, attach to the **running** Word/Excel instances with COM, scroll each hit into view, pause briefly, then apply the highlight. Reserve python-docx/openpyxl for *reading* (fast text extraction) — never for writing while the file is open.

## Workflow

### 1. Locate and open the documents

Glob for candidates (`**/*[Ss]cope*`, `**/*larification*`). Revisions matter: there are usually several register revisions in different folders. Note the revision letter in each filename. Open both documents on screen so the user can see them:

```powershell
Invoke-Item "<full path to Scope of Works .docx>"
Invoke-Item "<full path to Clarifications Register .xlsx>"
```

If the user named a specific revision ("scope of works rev A"), open that one. For the register, open the latest revision by default but hold off marking anything until step 3's alignment check.

### 2. Extract the citations from the Word document

Read the docx with python-docx (fast, read-only, works while Word has it open). Walk body elements in order so tables interleave correctly, capture the target section (heading style boundaries), and collect references matching the citation pattern — typically `CL-\d{3}`, but adapt to what the document actually uses (RFI-##, C##, etc.). Also note any "Clarification required" prose that carries **no** reference number — these are unregistered clarifications worth reporting.

```python
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
d = Document(path)
insec = False
lines = []
for child in d.element.body.iterchildren():
    if child.tag.endswith('}p'):
        p = Paragraph(child, d)
        style = p.style.name if p.style else ''
        if 'Heading 1' in style:
            if p.text.strip().startswith(SECTION_NUMBER): insec = True
            elif insec: break
        if insec and p.text.strip(): lines.append(p.text.strip())
    elif child.tag.endswith('}tbl') and insec:
        lines += [' | '.join(c.text.strip() for c in r.cells) for r in Table(child, d).rows]
```

### 3. Verify revision alignment — before highlighting anything

**Register numbering shifts between revisions.** New items get inserted and everything renumbers, so "CL-001" in the SOW may be "CL-004" in the latest register. Spot-check 2–3 citations: does the subject matter next to the citation in the SOW (e.g. "two centre lines 66mm apart") match the register row with that number? Read the register via COM if it's open, or openpyxl (`read_only=True`) if not.

If the numbers don't line up, **stop and tell the user** which register revision the SOW was written against, and ask which file they want marked (the matching old revision, the current one via a description-based mapping, or both). Highlighting the wrong rows silently is the worst outcome of this workflow.

### 4. Highlight visibly, scrolling to each hit

Pause ~800ms between hits so the user can follow. Track what you highlight for the summary.

**Word** — attach, find each citation with wildcards, scroll, highlight yellow:

```powershell
$word = [Runtime.InteropServices.Marshal]::GetActiveObject("Word.Application")
$doc = $word.Documents | Where-Object { $_.Name -like "*<doc name fragment>*" }
$word.Activate()
$rng = $doc.Content; $find = $rng.Find
$find.ClearFormatting(); $find.MatchWildcards = $true
$find.Text = "CL-[0-9]{3}"
$found = @()
while($find.Execute()){
  $rng.Select()
  $word.ActiveWindow.ScrollIntoView($rng, $true)
  $rng.HighlightColorIndex = 7   # wdYellow
  $found += $rng.Text
  Start-Sleep -Milliseconds 800
  $rng.Collapse(0)               # wdCollapseEnd - continue past this hit
}
```

**Excel** — attach, jump to each matching row, fill the row range:

```powershell
$xl = [Runtime.InteropServices.Marshal]::GetActiveObject("Excel.Application")
$wb = $xl.Workbooks | Where-Object { $_.Name -like "*Clarifications*" }
$ws = $wb.Worksheets.Item(1)
$lastRow = $ws.Cells.Item($ws.Rows.Count, 1).End(-4162).Row   # xlUp
foreach($ref in $refs){
  for($r = $headerRow + 1; $r -le $lastRow; $r++){
    if($ws.Cells.Item($r,1).Text -eq $ref){
      $xl.Goto($ws.Cells.Item($r,1), $true)                    # scrolls window to the row
      $ws.Range($ws.Cells.Item($r,1), $ws.Cells.Item($r,$lastCol)).Interior.Color = 65535  # yellow
      Start-Sleep -Milliseconds 800
    }
  }
}
```

PowerShell 5.1 notes: no `&&` chaining; `GetActiveObject` needs the exact ProgID; scoped `Find.Execute` loops need `$rng.Collapse(0)` or the loop re-finds the same hit.

### 5. Leave unsaved and report

Do **not** save either document — the user reviews the highlights live and decides. Close with a summary that covers:

- Total occurrences highlighted and the unique reference list
- Register items **not** cited in the section (and whether any are already Closed — that often explains the omission)
- References cited more than once, and where
- Un-numbered "clarification required" notes that exist in the SOW but not in the register
- Any revision-numbering mismatch found in step 3 and its consequence (e.g. "if this SOW issues with the Rev L register, every cross-reference points at the wrong item")

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
