# Educational content

Everything the platform teaches is defined in this folder as plain Python data.
Nothing here touches the database; `tools/seed.py` reads these modules and
writes the rows.

## Authoritative sources

| What | File | Notes |
|---|---|---|
| Units, dialogues, vocabulary, grammar points | `books/book1_part1.py` … `books/book3_part2.py` | 6 parts × 8 units = units 1–48. `books/__init__.py` puts them in course order (`all_units()`). |
| Base exercises, units 1–8 | `exercises/base_units_1_8.py` | Fill-in, translation, matching, synonyms, antonyms, word order, comprehension, plurals. |
| Grammar questions + unit test, units 1–16 | `exercises/grammar_units_1_16.py` | Supplementary. |
| Word-order questions, units 9–48 | `exercises/word_order_units_9_48.py` | Supplementary. |
| Fill-in-the-blank questions, units 9–48 | `exercises/fill_blank_units_9_48.py` | Supplementary. |
| Antonyms / plurals / synonyms / comprehension, units 1–48 | `exercises/enrichment_units_1_48.py` | Supplementary. |

Edit these files to change content. Do not edit content in the database by
hand and do not write one-off scripts for it: the next rebuild would lose the
change.

### Dialogue audio

Recordings are served directly from Vercel Blob. `dialogue_audio.py` maps
`(unit_number, dialogue_number)` to a published HTTPS URL; these are course
numbers, not database row IDs. Upload compressed, reviewed clips with a content
hash in the filename, then add their URLs to this catalog. Check the recording
against the deployed dialogue text before publishing. No database migration,
student-data update, or storage token in the frontend is needed. The player
does not preload recordings and pauses another dialogue when playback starts.
Recordings that cover only the beginning of a dialogue must also be listed in
`PARTIAL_DIALOGUE_AUDIO`, so both dialogue views label them as partial while
keeping the complete lesson text available. The unit 2, dialogue 2 recording is
partial and was published in that form at the owner's request.

## What a seed produces

**Base content** (`python -m tools.seed`, and the automatic first-run bootstrap):

- 48 units, each with three lessons: dialogues (`hiwar`), vocabulary
  (`mufradat`), grammar (`nahw`).
- 147 dialogues and texts (1343 lines), 998 words, all transcribed from the student
  book. Units 1–32: the book's dialogues; units 17–32 also hold Book 2's two
  listening texts per unit (appendix, titled "فَهْمُ المَسْمُوعِ"). Book 3 (units 33–48) has no dialogues;
  its first lesson holds the book's two listening texts per unit instead
  ("نصوص فهم المسموع"). A line with an empty speaker is narration: a stage
  direction or a paragraph.
- 2129 exercises: two generated per word (multiple choice + true/false, with
  randomly chosen wrong answers) plus the base exercises of units 1–8.

**Supplementary sets** (`--with-supplements`, or `--supplements-only` on an
existing database): 1960 more exercises, all in the grammar lesson of each unit,
for a total of 4056.

| Set | Units | Exercise numbers | Count |
|---|---|---|---|
| Grammar questions and unit test | 1–16 | 1… (replaces the lesson's base exercises) | 200 |
| Word order | 9–48 | 501+ | 200 |
| Matching, generated from the first 5 words | 9–48 | 601+ | 200 |
| Fill-in-the-blank, then "translate" for the first 5 words | 9–48 | 701+ | 400 |
| Antonyms, plurals, synonyms, comprehension | 1–48 | 801+ | 960 |

### Why the supplements are separate

These sets were originally added to the production database by hand, with
separate scripts run one after another (kept for reference in
`archive/legacy-scripts/content-operations/`). The order in which they were
run, and whether all of them were run, is not recorded anywhere. The
`--with-supplements` build reproduces the result of running each of them once
in the only order that keeps all of them; it matches the "+4000 exercises"
figure shown on the landing page, but it has **not** been compared with the
production database.

To compare, run the read-only report against each database:

```bash
python -m tools.content_report          # uses DATABASE_URL
```

## Changing content safely

1. Edit the data file.
2. Try it on a scratch database:
   `DATABASE_URL=sqlite+aiosqlite:///./scratch.db python -m tools.seed --with-supplements`
   then `python -m tools.content_report --units`.
3. Decide how to apply it to a database that students already use:
   - **Supplementary exercises only** → `python -m tools.seed --supplements-only`.
     It stops if students have answers on the exercises it would rebuild; add
     `--yes-delete-affected-answers` only if losing those answers is acceptable.
   - **Dialogues only** → `python -m tools.update_dialogues` (a dry run that
     reports the changes), then the same with `--apply`. It replaces the dialogues
     and the first lesson's title of every unit; no student data refers to them,
     so answers, progress, review cards and active time are kept.
   - **Units, vocabulary or base exercises** → there is no in-place
     update. `--replace --yes-delete-student-activity` rebuilds everything and
     deletes all answers, progress and review cards. Plan this for a term break,
     or write a targeted migration instead.

## Rules the code depends on

- Published dialogue audio is mapped by unit number and dialogue number in
  `dialogue_audio.py`, independent of database IDs. Media stays in object storage.
  `PARTIAL_DIALOGUE_AUDIO` labels incomplete recordings;
  `TEXT_VARIANT_DIALOGUE_AUDIO` labels approved wording differences. Neither flag
  changes the written lesson. Do not attach a substantially different recording
  merely because its topic matches the lesson.

- A true/false answer is stored exactly as `صَحِيح` or `خَطَأ`
  (`ANSWER_TRUE` / `ANSWER_FALSE` in `exercises/__init__.py`); the buttons in
  the app send these strings.
- Category texts (hints, the word-order prefix) are constants in
  `exercises/__init__.py`. Use the constants; do not retype Arabic text with
  diacritics. Two strings can look identical and still differ in the order of
  their combining marks, which is how the word-order filter broke for units
  9–48 in the past.
- Answers are compared after removing diacritics, so `عليكم` matches `عَلَيْكُم`.
