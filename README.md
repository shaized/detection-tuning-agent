# Detection Tuning Agent

**Review noisy rules while preserving detection coverage.**

A model-agnostic AI agent skill paired with a working Python evidence tool. The skill guides an assistant's analysis; the deterministic tool validates and organizes a local evidence snapshot. The included demo runs offline with no API key or dependencies.

[Agent instructions](SKILL.md) · [Example report](example-report.md) · [Input contract](INPUT.md) · [Portfolio](https://shaized.github.io/)

## Try it in one minute

Requires Python 3.11 or newer.

```sh
git clone https://github.com/shaized/detection-tuning-agent.git
cd detection-tuning-agent
python3 agent.py example.json
python3 agent.py example.json --format json
python3 -m unittest discover -v
```

**Expected result:** The first rule has 18 false positives among 20 reviewed alerts, plus one unresolved label. The second needs coverage validation before tuning.

## Use it as an AI agent

Open the repository in an assistant that can read local files and run Python, then give it this request:

> Read SKILL.md and follow its workflow. Review the fictional rule sample in example.json. Explain the sample metrics, missing labels, coverage concerns and the validation needed before changing a rule.

SKILL.md is the agent entry point. INPUT.md defines the evidence contract. agent.py performs the domain-specific analysis; runtime.py handles bounded JSON input, validation and report rendering. The assistant can explain the results, investigate alternatives and identify missing evidence using the tools you authorize.

The Python command itself is **not an LLM runtime**. It makes no network calls and performs no operational actions. There is no bundled model, production connector, autonomous service or implied access to your environment.

## What the agent does

1. Read the complete rule definition and establish intent, field semantics, schedule, aggregation, threshold and lookback. Do not infer intent only from its title.
2. Check whether the necessary logs and fields are present. Use agent.py to summarize a scoped, labeled alert sample; distinguish reviewed outcomes from unknowns.
3. Inspect representative true positives and false positives. Identify the narrow predicate responsible for noise and the malicious behavior that a proposed change could hide.
4. Produce a reviewable proposal with evidence, expected benefit, detection-loss risk, replay cases and rollback. Do not modify, disable or suppress the live rule.

## Design

```text
Selected evidence → validated local tool → traceable report
                                             ↓
                         AI-assisted reasoning → analyst decision
```

The examples are original, vendor-neutral implementations. All bundled data is fictional. Results retain unknowns and evidence gaps rather than presenting missing data as reassurance. Read the input contract for exact matching, thresholds and limitations.

## Validate and extend

The test suite covers the example, meaningful boundary cases, invalid evidence references where applicable, timestamp handling, bounded input and safe Markdown output. GitHub Actions runs the same offline tests. To add a real integration, produce the documented input shape in a separately reviewed adapter; keep credentials and operational evidence outside this repository.

A replay should include malicious and benign cases. The fraction of reviewed alerts is not a population false-positive rate and does not measure recall.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Use synthetic fixtures in issues and pull requests. This is a focused reference implementation; validate it against your data and review workflow before operational use.

## License

[MIT](LICENSE) · Built by [Shai Zaidenberg](https://github.com/shaized)
