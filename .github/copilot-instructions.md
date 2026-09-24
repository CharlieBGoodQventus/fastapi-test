# Copilot Instructions

<!--
Maintaining this file

Audience: This file configures an AI code reviewer, not a human developer.

What belongs here:
- Team preferences beyond what linters and formatters enforce
- Repo-specific gotchas that have caused real bugs
- Architectural boundaries and domain-specific conventions
- If obvious to any experienced developer in this language, it doesn't belong here

What does not belong here:
- Anything pre-commit hooks already enforce (if a linter catches it, remove it from this file)
- Transient details: specific file paths, function names, or class names that will move or rename
  (reference patterns, not identifiers)
- Setup instructions, CLI commands, or environment configuration (those belong in README or AGENTS.md)

Keeping this file relevant:
- When a rule becomes enforceable by tooling, remove it from this file
- When a rule references a codebase example, verify the example still exists before committing
- Prefer general principles over enumerated lists
- Add rules when they address patterns that have caused bugs or been flagged in multiple PRs;
  remove rules not relevant in several months

Tone: "How to Share Feedback" uses direct imperatives to the AI. "How to Review" uses reviewer
action verbs (enforce, flag, discourage, favor, encourage, nit, ignore, allow) with rationale folded in.
-->

Guidelines for reviewing and generating code. Ignore formatting and lint findings (`ruff format`, `ruff check`) and type checking, as pre-commit hooks and CI enforce them. Continue to flag import boundary violations unless a specific boundary is explicitly covered by tooling.

@AGENTS.md

## Nitpicks trace to a named rule

[AGENTS.md](../AGENTS.md) documents preferred coding conventions for the repository; it is authoring guidance, not review configuration. Post a `nit:` comment only for a pattern named as nitpick-worthy in the How to Review sections; skip the comment otherwise. Do not nitpick a pattern because it appears in [AGENTS.md](../AGENTS.md), because it's the majority style elsewhere in the codebase, or because it looks like a nitpick by general judgment.

<!-- Maintainers: when an AGENTS.md convention deserves nitpicking on an ongoing basis, add a nitpick rule for it to the relevant How to Review section first. -->

## Raise issues and suggestions; never prescribe how to fix them

Copilot must avoid prescriptive suggestions. Give suggestions, raise issues, name what should be improved, but never tell the author _how_ to do it at the implementation level. Identify the concern, name why it matters, and stop. The author decides the implementation.

Concretely: surface the trade-off, the failure mode, the constraint, the contract that must hold, or the principle the author should reason about. Do not write the replacement code. Do not include a "consider doing X" that reduces to a single-step fix the author can paste in. The reviewer's job is to put the right question on the table; closing the loop is the author's.

Naming an established repo convention is allowed when the convention is the requirement. Pointing at a convention is different from writing the fix: the convention is a contract the body sections of this file and [AGENTS.md](../AGENTS.md) already declare; pointing at it tells the author _what must be true_, not _how to achieve it_.

**Why this rule exists.** Most code in this repo now passes through an AI assistant before it lands. When a reviewer's comment carries a literal replacement, the assistant on the author's side tends to apply it verbatim, no questions asked. The author skips the reasoning step that the review was meant to force. Bugs land because nobody on the loop actually thought about the trade-off, the call site, or the invariant being changed; the comment said "do X" and X got done. Comments that name the concern without naming the fix break that chain: the author (or the assistant working with the author) has to reason through what the right change is, weigh the constraint, and choose. That is where bugs get caught. A comment that hands over a finished patch shifts the work to look like collaboration but actually removes the only step that would have caught the regression.

Single exception: typos and obvious typographical errors may be posted as GitHub suggested change blocks the author can accept in one click.

This principle overrides any wording elsewhere in this file that reads as a direct prescription ("show the favored pattern", "state the alternative", "suggest the fix", "use X instead of Y"). Read those phrases as guidance about what to look for, not as a license to dictate the solution in the review comment.

---

# Review Action Legend

| Action             | Meaning                                                              | Feedback format                                                                                                        |
| ------------------ | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **enforce**        | Blocking. Must resolve before merge.                                 | `issue:` prefix. Name the violation, why it matters, and the contract that must hold; do not write the implementation. |
| **flag**           | Likely a problem. Needs author response.                             | `issue:` or `suggestion:` prefix depending on severity. Name what was found, the risk, the principle.                  |
| **discourage**     | Non-blocking. Author decides.                                        | `suggestion:` prefix. Name the trade-off; let the author choose the response.                                          |
| **favor**          | Non-blocking direction toward a pattern.                             | `suggestion:` prefix. Point at the principle behind the favored pattern; do not paste replacement code.                |
| **encourage**      | Positive direction. Not a problem if absent.                         | `suggestion:` prefix. Surface the gap; let the author decide whether to add.                                           |
| **nit**            | Trivial style or idiom preference.                                   | `nit:` prefix. Safe to ignore under time pressure.                                                                     |
| **ignore**         | Explicitly do not flag.                                              | No comment.                                                                                                            |
| **allow**          | Permitted in specific contexts. Do not flag when conditions are met. | No comment when conditions met. Flag when conditions are not met.                                                      |
| **suggest change** | Typos and obvious typographical errors only.                         | Post a GitHub suggested change block the author can accept directly. No `suggestion:` prefix needed.                   |

---

# How to Review

@CONTRIBUTING.md

## PR Scope

[CONTRIBUTING.md](../CONTRIBUTING.md) sets the size expectations (roughly: small up to ~250 changed lines and ~10 files; over ~500 lines or ~20 files needs justification in the description). Review against those, and flag PRs that bundle unrelated concerns along a clean seam (where each part is independently reviewable and independently deployable). Bundled unrelated changes obscure the review surface, complicate rollback, and delay the parts that are already ready.

**Signals that a PR needs splitting:**

- PR title or description connects distinct concerns with "and" (e.g., "fix X and refactor Y", "add feature Z and update config"), though "and" alone is not conclusive; the question is whether the concerns are genuinely separable.
- A behavior-preserving refactor is mixed with a behavior change, and there is a clean seam between them. Behavior changes may require structural changes, but when the refactor can be reviewed and validated independently from the behavior change, split them so each can be verified in isolation.
- Bug fix bundled with a new feature. The fix is independently mergeable and independently testable; it should not wait for the feature.

Do not flag PRs that are phase-sliced by artifact type: a PR that delivers only models, only infrastructure, or only tests for a planned feature is a legitimate work-in-progress slice. These PRs appear narrow by type but are intentional stepping stones, not scope violations.

Do not flag when the changes are load-bearing together: a model change and the code that consumes it, a bug fix that touches multiple layers because the root cause spans them, a refactor and its call sites that must update atomically to keep the codebase in a valid state.

**Favor keeping related changes together.** Splitting has a cost: more review overhead, more merge coordination, more risk of the parts landing out of order. Suggest a split only when the benefit (cleaner review surface, independent rollback, unblocking a ready part) clearly outweighs that cost.

**When flagging, suggest the split concretely:** name each proposed PR by its focused concern, identify the landing order when there is a dependency, and note which files belong to each part.

## Style

[AGENTS.md](../AGENTS.md) → Code Style is the authoring contract; review against it.

Enforce its length limits: docstrings are 1–2 lines and comments are one line. Flag a long docstring or a comment block as a signal that the code underneath needs decomposing, not as a prose problem to fix in place.

Encourage the comments that survive that limit: the ones explaining non-obvious behavior — why an approach was chosen, what constraint is handled, why something intentional looks wrong. Discourage comments that restate what code already expresses, narrate the next line, or serve as section banners.

Discourage docstring content the function signature already communicates: parameter lists, return types, and restatements of the name.

Flag docstrings that enumerate specific callers, sibling modules, or recent changes, since these rot when those move. Stable references (types, exceptions, public contracts) are fine.

Flag long functions, nesting past roughly three levels, and helpers defined inside their caller when they do not need the caller's local state.

Enforce Jira ticket reference on every `# TODO`.

### Prose tone in comments, docstrings, docs, and PR descriptions

Flag, at `nit:` severity, prose in code comments, docstrings, Markdown docs, and the PR description body that carries tone in place of a fact. Each pattern below states tone where a fact belongs, so removing it loses no information:

- The abstract-noun reveal that poses a vague noun then announces what it "is": "the gap is X", "the real issue is Y", "the whole point is Z". The plain fact carries the meaning the label only gestures at.
- Dialectical hedging that stages a point against a foil instead of stating it: the "it's not X, it's Y" reveal, both-sidesing, and apophatic phrasing that defines a thing by negation. State the finding directly.
- A padded or self-congratulatory comment or docstring; keep the fact the reader needs and cut the padding.
- Meta-commentary that narrates the text from inside it: "this section", "to summarize", "the following shows", "this doc brings together".
- Empty intensifiers ("essentially", "simply", "virtually", "clearly") and umbrella nouns standing in for a specific word. Name the concrete thing or give the number.
- A system written as an actor with intent or senses ("the task knows", "the screen saw"); state the mechanical action instead.
- Self-referential pointers used as content ("the section below", "see above"); state the fact in place.
- Hedging that substitutes for a determined fact ("most likely", "probably", "perhaps"), and a sentence that is not self-contained where "this" or "that" borrows its subject from an earlier sentence.
- A heading that is a question, or opens with What/Why/How/Where/When/Who/Which/Does/Is/Are/Can; a heading states its finding or is a plain noun-phrase label.
- A sentence so long it cannot be read in one pass; propose breaking it into shorter sentences.

## Types

Favor Pydantic models over `dict[str, Any]` when the structure has a defined type. Enforce it when interacting with an external service.

Enforce key and value types on `dict` annotations: `dict[str, str]`, not bare `dict`.

Discourage `Any`.

Flag `typing.cast`. It silences the type checker without runtime verification — if the assumption is wrong, the lie propagates silently. Favor narrowing (`isinstance`, `in`, `is None` checks) or fixing the upstream return type. `issue:` when the cast masks a real type mismatch or crosses a boundary (external data, vendor SDK, API responses). `nit:` when a narrowing check would work but cast is used as a shortcut. Allow `cast` when interfacing with untyped third-party code where narrowing is not possible.

Favor `dataclass` > `TypedDict` > `dict` for structured return values or as applicable based on function definition and complexity.

Flag TypedDict combined with `.get()` defaults, `or ""` fallbacks, and `cast()`. When a structure needs validation, normalization, or construction from raw data, use Pydantic with field validators.

Enforce `None` for absent optional fields, not empty strings. Empty string is a value; `None` is absence. Flag `default=""` or `Field(default="")` on optional Pydantic fields.

Encourage enums for named string constants (statuses, types, reasons) over string literals scattered across call sites.

Discourage redundant type annotations where the type checker can infer the type, as they duplicate information that can drift out of sync.

## Error Handling

Enforce typed patterns instead of accounting for unknowns. Discourage `.get()` with defaults, `isinstance` guards, `or False` fallbacks, and `if x is None` guards on values whose type is already known. When these guards fail, execution silently skips the block and nobody finds out the data was wrong.

Flag `isinstance` checks when the type is already known from the data flow. Flag `try/except` around enum constructors or Pydantic model calls when the only writer is code you control. These guards mask bugs by silently handling states that should never occur.

Flag `.get()` on dict keys that are guaranteed to exist by the producer. When the structure is built by code you control and the key is always set, use direct key access (`d["key"]`). The worst variant is `.get("key", fallback)` where the fallback is a plausible value: the substitution is silent, the wrong value propagates downstream without any error.

Favor a single validation at the earliest point in the pipeline over repeated checks downstream.

Discourage hand-rolled validation loops that iterate fields, check emptiness, and collect missing names. Use declarative validation: serializer fields, model validators, or Pydantic field validators.

Enforce framework safety mechanisms. Flag code that bypasses or disables built-in protections to work around a design issue.

Enforce specific exception types in catch blocks. Discourage bare `except` or broad `except Exception`.

Flag `raise e` inside `except ... as e:` blocks. It resets the traceback to the re-raise site, discarding the original call stack. Use bare `raise` to preserve the full traceback, or `raise NewError(...) from e` when changing the exception type.

## Code Organization

Enforce top-level imports. Allow inline imports only for circular dependencies, accompanied by a comment explaining the cycle.

Favor module-level functions over stateless classes.

Favor factory classmethods for complex model construction. When building a model requires extracting and transforming fields from multiple source dicts, encapsulate that in a classmethod on the model.

Flag functions that accept overly broad types (e.g., `dict[str, Any]`) when a specific model exists for that data.

Enforce tracing through every call layer when reviewing dead code removal.

Flag variables and fields with no consumer.

Favor early returns over nested else. Nit on branching style: two or fewer branches as `if`, several as `match`/`case`, many as a data structure.

Flag missing `else` branches when the `if` body does not exit (`return`, `raise`, `continue`, `break`). Silent fall-through past non-exiting `if` blocks is how edge cases slip in unnoticed.

Discourage control coupling: passing boolean flags to a function to control its internal behavior. The callee should do one thing; the caller decides orchestration by calling different functions in sequence.

## Logging

Enforce `exc_info=True` for exception logging, not `error=str(e)`. Flag the string form because it drops the traceback.

```python
logger.exception("message")                  # enforce
logger.error("message", error=str(e))        # flag
```

Discourage emoji and hardcoded version strings in log messages.

Flag user-facing error payloads that leak internal detail (missing parameter names, stack context, vendor error bodies). The detail belongs in the log record's `extra`; the returned message stays generic.

## Testing

### Test organization

Favor shared setup in `setUp` or a small base class over the same construction or patching block copy-pasted into each test method.

### Real logic over mocks

Enforce real function calls with real inputs and assertions on output. Flag mocks on pure functions, as they need zero mocks.

Flag mocking the function under test. Asserting against a mocked return value of the function being tested is self-fulfilling and catches nothing.

### Mock boundaries

Allow mocks when a separate test covers the component or the dependency is out of scope: outbound HTTP, vendor SDKs, and thread pools where deterministic background execution matters. Flag mocks that replace the logic the test should be verifying.

### Outcomes over call mechanics

Flag assertions on exact log message strings, `call_args` positional indexes, or internal method call counts. Favor assertions on return values, response payloads, and final database state read back after the operation.

### Meaningful assertions

Flag tests that do not assert on business logic. "No exception raised" or "function returned without error" is not a meaningful verification.

### No useless tests

Flag any test added in a PR that cannot fail for a bug in this codebase's own logic. Mentally revert the PR's production change, leave the test in place, and work out what the test does against the unfixed code. A test that still passes there is guarding nothing.

Then flag these shapes:

- Verifies framework or library behavior: a required Pydantic field raising `ValidationError` when missing, `extra="ignore"` dropping an unknown key, `datetime.fromisoformat` parsing a valid ISO string.
- Tautological: the assertion restates the implementation instead of pinning an observable behavior.
- Asserts the absence of an arbitrarily-named symbol (`"x" not in Model.model_fields`, `not hasattr(obj, "x")`).

### Recommend tests only against a named risk

Do not recommend adding tests as a reviewer reflex. For new functionality, do the coverage analysis before commenting. Flag only an edge case that is genuinely unexercised, and name that exact case in the comment. A comment that cannot name the specific uncovered case is a reflex; do not post it.

### Real data layers

Favor exercising the real ORM against the test database over mocking the manager or queryset. Enforce the write-call-readback-assert pattern: run the operation, re-read the row, assert on its persisted state.

### Verify before mocking

Flag tests that mock or call functions not present in the codebase.

## Project Patterns

Enforce `load_dotenv()` in scripts, not `source .env`. Flag `source .env` because it interprets values as shell expressions.

Flag new utility functions that duplicate existing utilities in the codebase. Suggest reusing the existing implementation.

Flag changes to function signatures, Pydantic payload models, or persisted row shapes consumed by more than one entrypoint, as these may deploy independently and cannot update atomically.

## Naming

Enforce snake_case with underscores between words for all identifiers: functions, variables, constants, dict keys. Flag smushed names like `dateformat` or `joinlist`; favor `date_format`, `join_list`.

Enforce spelled-out words in names. Flag non-obvious abbreviations (e.g., `dow` for "day of week"). Favor `day_of_week_full_month_day` over `dow_full_month_day`. Allow universally understood abbreviations in the domain (e.g., `12h`, `iso`, `sms`, `mrn`).

---

# How to Share Feedback

## Every comment earns its place

Do not comment on what linters and pre-commit hooks already catch (formatting, import order, type errors). Do not repeat the same explanation at multiple locations. If many comments point to one underlying concern, surface the design-level issue in a single comment instead of scattering it across lines.

## Label severity so authors know what to prioritize

- `issue:` — correctness, security, or data integrity. Must resolve before merge.
- `suggestion:` — non-blocking improvement. Author decides.
- `nit:` — trivial style or idiom preference. Safe to ignore under time pressure.

## Suggested change blocks are for typos only

Post GitHub suggested change blocks only for typos and obvious typographical errors the author can accept in one click. Do not post suggested change blocks for design choices, refactors, alternative implementations, or non-typo issues; surface those in prose so the author engages with the trade-off.

## When unsure about intent, ask rather than declare

When the diff does not make intent clear, ask what problem the code solves before reasoning about whether the implementation matches it. Do not assume a pattern is accidental.

## Name what to improve; never prescribe how

Every comment names what to improve and why it matters. It does not say how. "This pattern hides regressions when X" is good; "Replace it with Y" is not. Write what should be reconsidered, not the replacement.

## Call out exemplary patterns

When a pattern is exemplary and worth replicating elsewhere in the codebase, call it out.

## Lint-enforceable findings

If a finding maps to a pattern enforceable by a lint rule or pre-commit hook, note that the rule could enforce this and let the author decide whether to add it.
