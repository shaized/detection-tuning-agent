"""Summarize labeled alert samples without modifying detection rules."""

from runtime import choice, cli, integer, report, rows, text, unique


def analyze(data):
    scope = text(data.get("scope"), "scope")
    minimum = integer(data.get("minimum_reviewed", 20), "minimum_reviewed", 1)
    rules = rows(data.get("rules"), "rules")
    labels = rows(data.get("labels"), "labels")
    unique(rules)
    unique(labels, "alert_id")
    known = {rule["id"] for rule in rules}
    for label in labels:
        if text(label.get("rule_id"), "label.rule_id") not in known:
            raise ValueError("label references an unknown rule")
        choice(
            label.get("disposition"),
            ["true_positive", "false_positive", "unknown"],
            "disposition",
        )
    findings = []
    for rule in rules:
        coverage = choice(
            rule.get("coverage"), ["healthy", "degraded", "unknown"], "rule.coverage"
        )
        sample = [label for label in labels if label["rule_id"] == rule["id"]]
        counts = {
            key: sum(label["disposition"] == key for label in sample)
            for key in ("true_positive", "false_positive", "unknown")
        }
        reviewed = counts["true_positive"] + counts["false_positive"]
        fraction = counts["false_positive"] / reviewed if reviewed else None
        recommendation = "collect_more_labels"
        if coverage != "healthy":
            recommendation = "validate_log_coverage_first"
        elif reviewed >= minimum:
            recommendation = (
                "review_noisy_predicates"
                if fraction >= 0.8
                else "retain_and_review_missed_cases"
            )
        findings.append(
            {
                "rule_id": rule["id"],
                "name": text(rule.get("name"), "rule.name"),
                "coverage": coverage,
                "sample_size": len(sample),
                "reviewed": reviewed,
                "unknown": counts["unknown"],
                "true_positives": counts["true_positive"],
                "false_positives": counts["false_positive"],
                "false_positive_fraction_of_reviewed": fraction,
                "recommendation": recommendation,
                "evidence_ids": [label["alert_id"] for label in sample],
            }
        )
    return report(
        "Detection Tuning Agent",
        {
            "scope": scope,
            "rules": len(rules),
            "labeled_samples": len(labels),
            "minimum_reviewed": minimum,
        },
        findings,
        [
            "The supplied labels may be biased or incorrect. This sample fraction is not a population false-positive rate.",
            "Missed detections and true negatives are absent; recall and overall detection effectiveness cannot be calculated.",
            "Coverage health is supplied by the caller. Thresholds of 20 reviewed samples and 80% false positives are example triage settings.",
            "No rule changes, exclusions, suppression or disabling are performed.",
        ],
        [
            "Inspect representative true positives, false positives and unresolved alerts.",
            "Propose the narrowest predicate change and replay it against both malicious and benign examples.",
            "Document detection loss, owner approval, rollback and monitoring before applying a change.",
        ],
    )


if __name__ == "__main__":
    cli(analyze, __doc__)
