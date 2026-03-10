# Evidence Quality Policy

## Evidence levels

- `fulltext`
  - strongest basis for comparison, limitation, and protocol context
- `abstract`
  - useful, but comparative claims must stay conservative when protocol details are missing
- `title`
  - not sufficient for stable claim writing; usually block and route upstream

## Numeric claims

If a snippet includes numbers, keep them only when at least some protocol context is available in the same evidence trail:
- task or setting
- metric definition
- constraint/budget/tool access/threat model

If that context is missing, prefer a qualitative summary plus `verify_fields`.

## Sparse evidence rule

Do not use generic caution bullets to make a pack look complete.
Instead:
- block when core evidence substrate is missing
- downgrade when evidence exists but is too thin for strong claims
- add `verify_fields` for missing protocol details
