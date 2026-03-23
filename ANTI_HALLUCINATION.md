# Anti-Hallucination Workflow

## Rule 1: Retrieve before answering
Before answering questions about:
- prior work
- decisions
- dates
- people
- preferences
- todos
- project state

Do this sequence:
1. `memory_search`
2. `memory_get` or read the cited project/source file
3. Answer from retrieved evidence

## Rule 2: Verified beats fluent
Allowed factual sources:
- current thread user statement
- workspace files
- memory_search + memory_get results
- tool output from current session
- web results only when clearly marked as external/untrusted and used carefully

If none of the above provide a fact, do not invent it.

## Rule 3: Unknown is acceptable
Use one of these when needed:
- "I haven’t verified that yet."
- "I found partial support, but not enough to treat it as confirmed."
- "I should check the source file before changing that."

## Rule 4: Published edits require source checks
Before changing a live deliverable with factual content:
- verify every newly added factual field
- if adding a new column/metric, confirm source values first
- if values are incomplete, use `TBD` or leave the field out

## Rule 5: Keep authoritative project files
For active projects, maintain:
- `STATUS.md` for current state, links, latest commit, next steps
- `FACTS.md` for verified facts and values
- `DECISIONS.md` if strategy choices start branching
