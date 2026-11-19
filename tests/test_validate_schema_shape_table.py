#!/usr/bin/env python3
"""Contract test ensuring SCHEMA.md Section 5 shape table aligns with validate.py shapes_of.

This test parses the markdown table in SCHEMA.md Section 5 and asserts exact
bidirectional parity between the documented shape labels and all tokens that
shapes_of in validate.py can emit.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "SCHEMA.md"

# The exhaustive vocabulary of 24 labels that shapes_of in validate.py can derive
# from Stellar account objects.
CANONICAL_SHAPES: frozenset[str] = frozenset(
    {
        "no_signers",
        "single_signer",
        "multi_signer",
        "master_is_signer",
        "master_absent",
        "thresholds_zero",
        "thresholds_nonzero",
        "auth_required",
        "auth_revocable",
        "auth_immutable",
        "auth_clawback_enabled",
        "no_home_domain",
        "blank_home_domain",
        "has_home_domain",
        "has_inflation",
        "no_inflation",
        "has_data",
        "no_data",
        "sponsored",
        "not_sponsored",
        "sponsoring",
        "not_sponsoring",
        "no_balances",
        "many_balances",
    }
)


def extract_schema_table_labels(schema_text: str) -> set[str]:
    """Extract all shape labels documented in Section 5 table of SCHEMA.md."""
    section_start = schema_text.find("## 5. The shape vocabulary")
    if section_start == -1:
        raise ValueError("Section 5 heading not found in SCHEMA.md")
    section_end = schema_text.find("## 6. Root documents", section_start)
    section_text = (
        schema_text[section_start:section_end] if section_end != -1 else schema_text[section_start:]
    )

    labels: set[str] = set()
    table_row_pattern = re.compile(r"^\|\s*`([a-z0-9_]+)`\s*\|", re.MULTILINE)
    for match in table_row_pattern.finditer(section_text):
        labels.add(match.group(1))
    return labels


class ValidateSchemaShapeTableTest(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(SCHEMA_PATH.is_file(), f"{SCHEMA_PATH} does not exist")
        self.schema_text = SCHEMA_PATH.read_text(encoding="utf-8")
        self.table_labels = extract_schema_table_labels(self.schema_text)

    def test_extracted_labels_non_empty(self) -> None:
        self.assertTrue(len(self.table_labels) > 0)

    def test_count_matches_expected_vocabulary_size(self) -> None:
        self.assertEqual(len(self.table_labels), len(CANONICAL_SHAPES))

    def test_bidirectional_parity(self) -> None:
        missing_from_schema = CANONICAL_SHAPES - self.table_labels
        unexpected_in_schema = self.table_labels - CANONICAL_SHAPES
        self.assertSetEqual(
            missing_from_schema,
            set(),
            f"Labels present in validate.py but missing from SCHEMA.md: "
            f"{sorted(missing_from_schema)}",
        )
        self.assertSetEqual(
            unexpected_in_schema,
            set(),
            f"Labels documented in SCHEMA.md but not emitted by validate.py: "
            f"{sorted(unexpected_in_schema)}",
        )

    def test_section_five_contains_zero_em_dashes(self) -> None:
        section_start = self.schema_text.find("## 5. The shape vocabulary")
        section_end = self.schema_text.find("## 6. Root documents", section_start)
        section_text = (
            self.schema_text[section_start:section_end]
            if section_end != -1
            else self.schema_text[section_start:]
        )
        self.assertNotIn("\u2014", section_text)


if __name__ == "__main__":
    unittest.main()
