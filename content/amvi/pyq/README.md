# AMVI — PSC previous-question cards

One card per Kerala PSC previous question that fits the current AMVI syllabus
(see `../PLAN.md`). Each card is tagged with the exam, category number, question
paper code, date and question number, and comes with the real four-option MCQ.

Build: `python pyq/build_pyq.py` (from `content/amvi/`) →
`dist/amvi-pyq-pack.json` (Recallio pack, schema 1.0) and `dist/pyq-review.csv`.

## Papers used (all from keralapsc.gov.in)

| File | Exam | Cat. No. | Q.P. code | Date | Cards |
|---|---|---|---|---|---|
| 2023_amvi_045.yaml | MVI / AMVI, Motor Vehicles Dept | 517/2022, 610/2022, 613/2022 | 045/2023 | 26-05-2023 | 91 |
| 2023_lecturer_auto_105.yaml | Lecturer in Automobile Engg | 250/2022 | 105/2023/OL | 05-07-2023 | 69 |
| 2022_mti_077.yaml | Motor Transport Inspector (Technical), Police | 482/2019 | 77/2022/OL | 15-09-2022 | 65 |
| 2020_mtsi_010.yaml | Motor Transport Sub Inspector (Trainee), Police | 013/2016 | 10/2020/OL | 04-09-2020 | 56 |
| 2019_mvact_paper1_feb.yaml | Motor Vehicles Act (Paper I) test | — | — | 22-02-2019 | 36 |
| 2019_mvact_paper1_oct.yaml | Motor Vehicles Act (Paper I) test | — | — | 31-10-2019 | 36 |
| 2024_mvact_017_may.yaml | Paper 017 Motor Vehicles Act | — | 017 | 14-05-2024 | 24 |
| 2024_mvact_017_oct.yaml | Paper 017 Motor Vehicles Act | — | 017 | 29-10-2024 | 37 |
| 2025_mvact_017_may.yaml | Paper 017 Motor Vehicles Act | — | 017 | 22-05-2025 | 20 |
| 2025_mvact_017_oct.yaml | Paper 017 Motor Vehicles Act | — | 017 | 22-10-2025 | 24 |

## What was left out, and why

Every left-out question is listed under `skipped:` in its paper file with the reason:

- deleted or cancelled by PSC;
- outside the AMVI syllabus (computers, constitution/GK, industrial management,
  machining, refrigeration, lamps; CMVR/KMVR form numbers, fees, colours and
  Kerala-only rules that the AMVI syllabus does not list);
- fines from before the MV (Amendment) Act, 2019 that are no longer correct.

## Not yet found

- Older AMVI papers (Cat. 551/2014 etc.): PSC's site lists only shortlists and
  rank lists for them, not question papers.
- Departmental tests "Laws relating to Motor Vehicles" (033017, 033035): PSC
  published only answer tables, no question text.

## Review

All cards are `needs_review`. 13 cards carry a `review_note` where the PSC key or
the extracted text looked doubtful. Question text is condensed from the PSC PDFs;
check against the PDF (link in each file) before publishing.
