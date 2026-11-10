import copy
import json
from pathlib import Path
import unittest

from agent import analyze


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path(__file__).with_name("example.json").read_text())

    def test_unknown_labels_are_not_counted_as_benign(self):
        row = analyze(self.data)["findings"][0]
        self.assertEqual(row["reviewed"], 20)
        self.assertEqual(row["unknown"], 1)
        self.assertEqual(row["false_positive_fraction_of_reviewed"], 0.9)

    def test_degraded_coverage_prevents_noise_recommendation(self):
        self.data["rules"][0]["coverage"] = "degraded"
        self.assertEqual(
            analyze(self.data)["findings"][0]["recommendation"],
            "validate_log_coverage_first",
        )

    def test_small_samples_require_more_labels(self):
        self.data["labels"] = self.data["labels"][:2]
        self.assertEqual(
            analyze(self.data)["findings"][0]["recommendation"], "collect_more_labels"
        )

    def test_empty_labels_have_no_fraction(self):
        self.data["labels"] = []
        self.assertIsNone(
            analyze(self.data)["findings"][0]["false_positive_fraction_of_reviewed"]
        )

    def test_unknown_rule_id_is_rejected(self):
        self.data["labels"][0]["rule_id"] = "missing"
        with self.assertRaises(ValueError):
            analyze(self.data)

    def test_duplicate_labels_do_not_inflate_sample(self):
        self.data["labels"].append(copy.deepcopy(self.data["labels"][0]))
        with self.assertRaises(ValueError):
            analyze(self.data)


if __name__ == "__main__":
    unittest.main()
