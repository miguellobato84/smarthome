# Planning Mode and Execution Plans

## When to use planning mode
Use an execution plan when:
- The work is a complex new feature or a complex refactor.
- The change is architectural or touches multiple automation/template/dashboard areas.
- The change affects security, privacy, external integrations, or critical reliability.
- The scope is unclear or risk is high.

## Where plans live
- Store plans under `.agent/plans/`.
- Reference the plan filename in the Codex prompt when executing.

## Commit policy
- Commit plans when they affect architecture, operating workflows, or shared team process.
- Do not commit one-off exploratory plans unless they will be reused.

## Naming convention
- `.agent/plans/YYYY-MM-DD-HHMM-short-feature.md`

## Execution plan template

### 1) Goal and context
- **Goal:**
- **User impact:**
- **Non-goals:**
- **Constraints:** (availability windows, downtime risk, compatibility)
- **Dependencies:** (integrations, services, external APIs)

### 2) Current state
- **Relevant modules/files:**
- **Known pain points:**
- **Links to docs/issues:**

### 3) Risks and safety checks
- **Prompt-injection risk:** (untrusted dashboard/template inputs)
- **Excessive agency risk:** (commands with side effects)
- **Output validation plan:** (config checks + manual automation tests)
- **Rollback plan:**

### 4) Proposed approach
- **Design overview:**
- **Data flows:**
- **Compatibility notes:**

### 5) Work breakdown
- [ ] Step 1:
- [ ] Step 2:
- [ ] Step 3:

### 6) Test plan
- **Configuration checks:**
- **Manual checks:**
- **Regression checks:**

### 7) Release and rollout
- **Rollout strategy:**
- **Monitoring/observability:**
- **Owner:**

### 8) Open questions
-
