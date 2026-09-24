# Contributing

This repository expects pull requests to be easy to review, safe to merge, and explicit about their intent. These rules apply to both human contributors and AI coding agents.

## Pull request size

Prefer small, focused pull requests. A PR should normally address one issue, feature, refactor, or bug fix. If the change starts to cover multiple goals, split it into separate PRs.

As a rule of thumb:

- **Small PR:** up to ~250 changed lines and up to ~10 files.
- **Medium PR:** ~250-500 changed lines or ~10-20 files. These are acceptable when the scope is still focused and the PR description explains the structure of the change.
- **Large PR:** more than ~500 changed lines, more than ~20 files, or changes across several unrelated areas. Large PRs should be split unless there is a clear reason not to.
- **Very large PR:** around 1000+ changed lines. These require explicit justification in the PR description and should usually be discussed before review.

Generated files, lockfiles, migrations, snapshots, and mechanical formatting changes may inflate the line count. Call that out in the PR description so reviewers can focus on the meaningful changes.

Large PRs can be justified when splitting the work would create unnecessary transitional behavior or temporary compatibility code. For example, when removing or replacing a field, it may be better to make one larger consistent change than to support both the old and new behavior across several PRs.

A high file count can also be justified when the change is mechanical and low-risk, such as applying the same syntax update, import change, rename, or formatting rule across many files. In those cases, keep the PR limited to the mechanical change and avoid mixing it with behavioral changes.

## Branch, PR title, and merge method

- **Branch name:** include the Jira ticket key as a prefix, for example `PROJ-1234-add-user-export`. A personal prefix is also acceptable as long as the ticket key is still in the name, for example `eder/PROJ-1234-add-user-export`.
- **PR title:** start with the Jira ticket key followed by a concise, imperative summary, for example `PROJ-1234: Add user export endpoint`. Keep the title self-contained — it becomes the commit subject on `main` after squashing.
- **Merge method:** use **Squash and merge**. The PR title is used as the squash commit subject; GitHub appends the PR number automatically.

If a change genuinely has no Jira ticket (a small docs or tooling fix, for example), call that out in the PR description and omit the Jira prefix from the branch and title.

## Pull request description

Every PR should explain:

- Related Jira ticket (link).
- What changed, described at a high level.
- Why the change is needed.
- How the change was tested.
- Any risks, tradeoffs, migrations, rollout steps, or follow-up work.
- A **Notes** section for remaining issues, stale docs, or TODOs reviewers should know about.

### Writing "What changed"

Write this section for a reviewer who has not read the diff yet. Describe the change in terms of behavior and intent, not implementation. A few sentences or bullets is usually enough. If a reviewer can read it and correctly describe what the system does now, it is doing its job.

For example:

> Inbound SMS messages are now handled by a background worker instead of inline in the webhook request. The webhook persists the message and enqueues a job; delivery failures are retried instead of dropped. No change to the webhook's response contract.

Do:

- Describe the behavior before and after, or what is new.
- Name the concepts and components involved (endpoint, job, model, screen), not the individual functions and files that implement them.
- Call out anything that changes a contract: API shape, settings, permissions, database schema, events, or operational behavior.
- Point out mechanical or generated parts of the diff so reviewers know they can skim them.

Avoid:

- File-by-file or commit-by-commit walkthroughs.
- Restating the diff — "added `foo()`", "renamed `bar` to `baz`", "updated imports". The diff already says that.
- Line-level commentary on code the reviewer has no context for yet.

Details that only make sense with the code in front of you belong in inline comments on the diff, where the reviewer is actually looking, not in the description.

### Pointing reviewers at the code

Use the `F:` file-path style (for example, `F:src/app/authentication.py`) to point reviewers at the files that matter most: the entry point of the change, or where a decision worth discussing lives. Use it sparingly — a few signposts, not an index of the diff.

If the PR is large, explain why it was not split and point reviewers to the most important files or decisions.

A pull request template is provided at `.github/pull_request_template.md` and is pre-filled when you open a PR on GitHub.

## Testing

Test the change before requesting review. Automated tests are expected when behavior changes, but they are not enough by themselves.

At minimum, the PR description should mention:

- The automated tests that were added or updated.
- The manual verification performed in the local environment.
- Any QA deployment or additional validation used for risky or potentially breaking changes.

List the commands you ran with a pass/fail marker (✅ / ❌) so reviewers can see the result at a glance.

If a test could not be run, state why and explain what was done instead.

## UI changes

For UI changes, include screenshots or screen recordings in the PR. Show the relevant before and after states when useful.

When applicable, verify important responsive states, empty states, loading states, error states, and permission-dependent views.

## Documentation and operational changes

Update documentation when behavior, configuration, setup, APIs, commands, permissions, or operational procedures change.

For database migrations, background jobs, feature flags, settings, or deployment-sensitive changes, describe the rollout and rollback considerations in the PR.

## Keep changes reviewable

Avoid unrelated cleanup, formatting, dependency updates, or refactors in the same PR as a behavioral change. If cleanup is needed, prefer a separate PR before or after the main change.

Each commit should represent a logical unit of work when practical. Do not include fixup commits, temporary debugging code, commented-out code, or local-only configuration.

@AGENTS.md

## Agent-specific expectations

AI agents must follow the same standards as human contributors.

Agents should:

- Keep the change scoped to the user request.
- Prefer established project patterns over introducing new abstractions. Following the surrounding code does not mean copying a bad pattern that happens to be nearby.
- Avoid broad refactors unless explicitly requested or required.
- Keep comments and docstrings short — comment only what the code cannot say. Docstrings are 1–2 lines and comments are one line; if more is needed, the code should be simplified instead.
- Prefer small, single-purpose functions and shallow control flow over long functions, deeply nested conditions, and defensive checks for states that cannot happen. See [AGENTS.md](AGENTS.md) for repo-specific style guidance.
- Run the relevant checks before finishing.
- Clearly report what was changed, what was tested, and what could not be verified.
- Include screenshots for UI changes when the environment allows it.

Agents should not claim that tests, screenshots, or QA validation were performed unless they were actually completed.
