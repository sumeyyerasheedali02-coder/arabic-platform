# Security notes

## Action required: rotate the exposed Google API keys

Nine distinct strings that look like Google (Gemini) API keys were committed to
this repository. They were embedded in:

- `files_extracted/fix_key3.py` … `files_extracted/fix_key9.py` (seven key-swapping scripts)
- `files_extracted/main_backup.py` (a backup copy of the application entry point)
- two historical revisions of `files_extracted/main.py`

Those files have been removed from the working tree, but **removing a file does
not revoke a key and does not remove it from Git history**. Every one of those
values is still readable by anyone who can read the repository history
(`origin` is hosted on GitHub).

What to do, in order:

1. In Google AI Studio / Google Cloud Console, delete (or regenerate) every API
   key that was ever used for this project. Treat all of them as compromised;
   their validity was not tested during this cleanup.
2. Create one new key and set it only as the `GOOGLE_API_KEY` environment
   variable of the backend service (Railway). Never write it into a file that
   is tracked by Git.
3. Review the provider's usage/billing page for unexpected activity.
4. Optional: purge the old values from Git history (`git filter-repo`) and
   force-push. This rewrites history for every clone, so it was deliberately
   **not** done automatically. Rotation (steps 1–2) is what actually removes
   the risk; history rewriting is only hygiene afterwards.

## Reporting a problem

If you find a vulnerability, contact the project maintainer privately rather
than opening a public issue.
