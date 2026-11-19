#!/usr/bin/env python3
"""Contract test ensuring SCHEMA.md Section 6 root document documentation agrees with validate.py.

This test asserts that SCHEMA.md Section 6 thoroughly documents the root document
contract, including exact error messages, network passphrases, and structural rules
enforced by check_root in validate.py.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import validate

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "SCHEMA.md"


class ValidateSchemaRootContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(SCHEMA_PATH.is_file(), f"{SCHEMA_PATH} does not exist")
        self.schema_text = SCHEMA_PATH.read_text(encoding="utf-8")

    def test_schema_has_section_six(self) -> None:
        self.assertIn("## 6. Root documents", self.schema_text)

    def test_schema_documents_missing_root_error(self) -> None:
        self.assertIn(validate.MISSING_ROOT, self.schema_text)

    def test_schema_documents_not_json_error(self) -> None:
        self.assertIn("not JSON:", self.schema_text)

    def test_schema_documents_not_json_object_error(self) -> None:
        self.assertIn("not a JSON object", self.schema_text)

    def test_schema_documents_passphrase_mismatch_error(self) -> None:
        self.assertIn("is not the", self.schema_text)

    def test_schema_documents_all_network_passphrases(self) -> None:
        for network, (_, passphrase) in validate.NETWORKS.items():
            self.assertIn(network, self.schema_text)
            self.assertIn(passphrase, self.schema_text)

    def test_schema_section_six_contains_zero_em_dashes(self) -> None:
        section_start = self.schema_text.find("## 6. Root documents")
        self.assertNotEqual(section_start, -1)
        section_end = self.schema_text.find("## 7. Versioning", section_start)
        section_text = (
            self.schema_text[section_start:section_end]
            if section_end != -1
            else self.schema_text[section_start:]
        )
        self.assertNotIn("\u2014", section_text)


if __name__ == "__main__":
    unittest.main()
