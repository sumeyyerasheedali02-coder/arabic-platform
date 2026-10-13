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

## Staff accounts and section access

Roles are stored in the database: student, teacher, admin. The reserved owner
address is `malekco721@gmail.com`. Migration 0003 promotes its existing account
and imports existing `TEACHER_EMAILS` accounts once; the allowlist never grants
runtime privileges. Public registration cannot claim reserved staff addresses.
Passwords and existing student activity are preserved during migration.

Only the admin can create teacher accounts, assign sections, reset teacher
passwords, disable teachers, and correct student sections. Teacher section
assignments support multiple teachers per section. No assignment grants no
student access. Every list, unit report and student detail request is scoped
on the server; inaccessible student ids return the same 404 as missing ids.
Staff accounts are excluded from student reports. Unassigned students are
visible only to the admin. Student corrections preserve all progress records.

JWT subjects resolve to active database accounts on every protected request.
Disabling an account or resetting its password increments token_version and
invalidates its existing tokens, including legacy tokens without a version.
Changing assignments takes effect on the next server request. Admin changes
are recorded in admin_audit without password material or access tokens.

Use the admin dashboard for normal management. The legacy teacher_accounts CLI
is a server-operator recovery tool; newly provisioned teachers still need
section assignments. On a fresh deployment, `python -m tools.admin_account`
creates only the reserved owner and privately prompts for its password; it
refuses to overwrite an existing account. There is no automated invitation
mail service or public staff signup.

Review ownership of old staff accounts before assigning their sections.
E-mail addresses are compared without regard to case. Duplicate legacy
addresses require operator review; only the lowest id can log in.

## Reporting a problem

If you find a vulnerability, contact the project maintainer privately rather
than opening a public issue.
