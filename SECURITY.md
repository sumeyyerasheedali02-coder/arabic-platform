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

## Teacher accounts

Teacher rights belong to the accounts whose e-mail is listed in `TEACHER_EMAILS`.
The platform does not verify e-mail ownership, so:

- An allowlisted address can no longer be registered through the public
  sign-up form (the API answers 403). Before this change, whoever registered
  that address first — or any upper/lower-case variant of it — received
  teacher rights and could read every student's name, e-mail and progress.
- The teacher account is created by the server operator:
  `python -m tools.teacher_accounts create --email <address> --name "<name>"`.
- E-mail addresses are now compared without regard to letter case everywhere.

**Review needed once:** accounts that already existed were not verified. Run
`python -m tools.teacher_accounts list` against the production database. If an
address shows more than one account, or you are not sure who registered it,
delete the extra rows and reset the password with
`python -m tools.teacher_accounts set-password --email <address>`.

## Reporting a problem

If you find a vulnerability, contact the project maintainer privately rather
than opening a public issue.
