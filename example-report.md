# Detection Tuning Agent

## Summary

- **scope:** Fictional one-day labeled sample
- **rules:** 2
- **labeled samples:** 21
- **minimum reviewed:** 20

## Findings

### Finding 1

- **rule id:** rule-1
- **name:** Unusual administrative sign-in
- **coverage:** healthy
- **sample size:** 21
- **reviewed:** 20
- **unknown:** 1
- **true positives:** 2
- **false positives:** 18
- **false positive fraction of reviewed:** 0\.9
- **recommendation:** review\_noisy\_predicates
- **evidence ids:** \["sample-1", "sample-2", "sample-3", "sample-4", "sample-5", "sample-6", "sample-7", "sample-8", "sample-9", "sample-10", "sample-11", "sample-12", "sample-13", "sample-14", "sample-15", "sample-16", "sample-17", "sample-18", "sample-19", "sample-20", "sample-21"\]

### Finding 2

- **rule id:** rule-2
- **name:** Endpoint event gap
- **coverage:** unknown
- **sample size:** 0
- **reviewed:** 0
- **unknown:** 0
- **true positives:** 0
- **false positives:** 0
- **false positive fraction of reviewed:** null
- **recommendation:** validate\_log\_coverage\_first
- **evidence ids:** \[\]


## Limitations

- The supplied labels may be biased or incorrect\. This sample fraction is not a population false-positive rate\.
- Missed detections and true negatives are absent; recall and overall detection effectiveness cannot be calculated\.
- Coverage health is supplied by the caller\. Thresholds of 20 reviewed samples and 80% false positives are example triage settings\.
- No rule changes, exclusions, suppression or disabling are performed\.

## Next Steps

- Inspect representative true positives, false positives and unresolved alerts\.
- Propose the narrowest predicate change and replay it against both malicious and benign examples\.
- Document detection loss, owner approval, rollback and monitoring before applying a change\.
