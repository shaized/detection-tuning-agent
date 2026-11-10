# Input and output contract

## Input

The root requires scope, rules and labels. minimum_reviewed is a positive integer (default 20). Rules have unique id, name and coverage (healthy/degraded/unknown). Labels have unique alert_id, rule_id and disposition (true_positive/false_positive/unknown). The false-positive fraction divides false positives by reviewed labels only. The 80% suggestion threshold is an example heuristic, not a statistically validated tuning policy.

See [example.json](example.json) for a complete fictional input. All demo identities, indicators, events, products and reputation providers are synthetic. Documentation IPs and example domains are not threat intelligence.

Input must be a UTF-8 JSON object no larger than 2 MiB. Duplicate JSON keys, malformed required fields, ambiguous timestamps and conflicting identifiers are rejected. Timestamps require an explicit UTC offset. Small local snapshots are the intended workload; there is no streaming, database or production connector in this version.

## Output

`python3 agent.py INPUT.json` emits Markdown. Add `--format json` for structured output. The JSON envelope contains schema_version, agent, summary, findings, limitations and next_steps. The tool writes to standard output and does not modify the source input. Input errors return exit code 2; a valid assessment returns 0 even when findings are present.

JSON preserves evidence text. Markdown renders evidence as literal escaped text, so input cannot inject links, headings or HTML into the report. Every result preserves substantive limitations.

## Example interpretation

The first rule has 18 false positives among 20 reviewed alerts, plus one unresolved label. The second needs coverage validation before tuning.

A replay should include malicious and benign cases. The fraction of reviewed alerts is not a population false-positive rate and does not measure recall.
