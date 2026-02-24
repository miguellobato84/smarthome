# Standard: Commit Structure

## Principles
- Commits should be scoped, understandable, and easy to revert.
- The message should describe behavior intent, not only file churn.
- Follow observed repository style while improving clarity for new commits.

## Repo-specific rules (detected from this repository)
- Subject format currently observed is mixed:
  - Conventional style appears (`feat: ...`, `refactor: ...`, `chore: ...`, optionally with scope like `feat(lovelace): ...`).
  - Imperative/plain subjects also appear (`Add ...`, `Remove ...`, `fix`).
- For new Codex commits, prefer conventional style:
  - `<type>(<optional-scope>): <short imperative description>`
  - Common types used here: `feat`, `fix`, `refactor`, `chore`.
- Keep the subject concise and without trailing period.
- Even though historical commits rarely include bodies, Codex commits must include a meaningful body explaining what and why.

## Codex baseline rules (always apply)
- One logical change per commit.
- Use a blank line between subject and body.
- In the body, explain rationale and notable decisions for non-trivial changes.
- For multiline commit messages, prefer:
  - `git commit -m "<subject>" -m "<full body with real line breaks, paragraphs, and trailers>"`
- Keep the full body (including trailers) in one multiline `-m` argument with actual newlines.
- Do not compose multiline bodies with escaped `\n`.
- AI-assisted commits from Codex must end with this trailer block (after an empty line):
  - `AI-assisted-by: OpenAI Codex`
  - `Co-authored-by: Codex <199175422+chatgpt-codex-connector[bot]@users.noreply.github.com>`

## Examples
- `docs: add agentic coding setup for Home Assistant repo`
- `refactor(automation): split bathroom extractor logic by trigger source`

## Validation
- `git show --stat` reflects one coherent logical change.
- `git log -1 --format=%B` contains:
  - Real line breaks (no literal `\n`)
  - A blank line between subject and body
  - A blank line before attribution trailers
