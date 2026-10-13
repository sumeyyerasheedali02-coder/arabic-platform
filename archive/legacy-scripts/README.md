# Legacy scripts (reference only — do not run)

These files are kept so that the history of the production content can be
understood. **They are not runnable any more** (they import modules that no
longer exist) and must not be repaired and run: most of them delete exercises,
which on PostgreSQL also deletes the answers students recorded for them.

Everything they contained that is still needed now lives in
`files_extracted/content/` and is loaded by `python -m tools.seed`.

## content-operations/

Scripts that were run by hand against the production database to add
exercises to the grammar lesson of each unit.

| Script | What it did | Replaced by |
|---|---|---|
| `add_grammar_exercises.py` | Deleted every exercise of the grammar lesson (units 1–16) and inserted grammar questions + a unit test | `content/exercises/grammar_units_1_16.py` |
| `fill_1_8.py`, `fill_9_16.py`, `fill_17_32.py`, `fill_33_48.py` | Antonym / plural / synonym / comprehension questions, numbers 801+ | `content/exercises/enrichment_units_1_48.py` |
| `fill_trans_9_28.py`, `fill_trans_29_48.py` | Fill-in-the-blank (numbers 701+) and generated translation questions | `content/exercises/fill_blank_units_9_48.py` + generation in `tools/seed.py` |
| `fill_match.py` | Generated matching questions, numbers 601+ | generation in `tools/seed.py` |
| `fill_order.py` → `order_all.py` → `fix_order_all.py`, `final_fix.py` | Word-order questions, numbers 501+. Three rewrites of the same data: the first ones wrote «رَتِّب» with its diacritics in a different order than the frontend filter expected, so the questions did not show up under "ترتيب كلمات" | `content/exercises/word_order_units_9_48.py` (last revision of the data: unit 9 from `final_fix.py`, units 10–48 from `fix_order_all.py`) |
| `extra_exercises.py`, `manual_extra.py`, `auto_extra.py` | Earlier antonym/plural sets, numbers 901+. The `fill_*` scripts delete those exercise types before inserting, so these were superseded | not carried over |
| `build_data.py` | Generated the base exercises of units 1–8 | `content/exercises/base_units_1_8.py` is now edited directly |
| `audit_empty.py`, `full_audit.py` | Counted exercises per filter category | `python -m tools.content_report` |

The order in which these were run in production was never recorded.
`python -m tools.content_report` (read-only) shows what a database actually
contains, including leftovers from the superseded sets.

## old-content-format/

`unit_1.py` and `unit_2.py` describe the first two units in an earlier, richer
format (example sentences, word types, per-lesson structure). The seed has not
used them since the book files were introduced.

## What was deleted instead of archived

About 115 one-off helpers were removed from the tree; they remain in Git
history (last present in commit `7643f25`). They were:

- scripts that edited source files by search-and-replace (`fix_*.py`,
  `add_*.py`, `apply_login.py`, `setup_design.py`, …), often with an absolute
  path from another computer;
- scripts that printed parts of files or queried the database for one value
  (`show_*.py`, `check_*.py`, `verify_*.py`, `debug_dial.py`, …);
- scripts that called the production API (`health.py`, `test_api.py`, …) or
  ran `git commit` / `git push` (`do_push.py`, `force_deploy.py`);
- `test_one.py`, which inserted a question starting with `[تجربة]` into unit 1
  (`tools.content_report` flags it if it is still in a database);
- backups, empty placeholder modules and exact duplicates
  (`schemas_backup.py`, `auth_router.py`, `gemini_router.py`, `unit_1.py`,
  the root copy of `book1_part1_data.py`).

The scripts that embedded API keys were removed earlier; see `SECURITY.md`.
