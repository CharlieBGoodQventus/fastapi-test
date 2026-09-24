# PR Skill — Agent Instructions

## Creating a pull request

1. **Open as a draft** — always create PRs with the `--draft` flag.
2. **Title** — follow `CONTRIBUTING.md`: Jira key then imperative summary
   (e.g. `PROJ-1234: Add user export endpoint`). Use the latest commit subject
   as a reference. Omit the key if there is no ticket; note that in the body.
3. **Body** — populate the body from `.github/pull_request_template.md`.
   Fill in the `Problem`, `Solution`, and `Resources` sections based on the
   work done. Leave the `Demo` section as-is if there is nothing visual to
   show.
4. **Acceptance Criteria** — copy the checkbox list from the template exactly
   as written. Do **not** check, uncheck, or remove any of the checkboxes.

## Modifying a pull request

- **Title** — do not change the PR title unless the user explicitly requests it.
- The `Acceptance Criteria` checkboxes must never be altered — do not tick,
  untick, or delete them.
