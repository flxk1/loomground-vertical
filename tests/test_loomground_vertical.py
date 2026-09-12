# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""Tests for loomground_vertical. Runs under pytest and `python -m unittest`.

The registries are module-level and stateful by design — registering is the
whole point — so tests that register use distinct ids and assert additively
rather than assuming an empty registry.
"""
from __future__ import annotations

import ast
import os
import pathlib
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import loomground_vertical as v  # noqa: E402

SRC = pathlib.Path(__file__).resolve().parents[1] / "src" / "loomground_vertical"


class TestSubjectVocabulary(unittest.TestCase):
    def test_a_vertical_registers_its_own_vocabulary(self):
        vocab = v.DomainVocabulary(
            domain="test-widgets",
            facets=(v.FacetSpec(name="risk", values=("low", "high"),
                                description="how much harm it can do"),))
        v.register_vocabulary(vocab)
        self.assertIs(v.get_vocabulary("test-widgets"), vocab)

    def test_an_unregistered_domain_returns_none_rather_than_a_default(self):
        """Silence about a domain must not resolve to some other domain's model."""
        self.assertIsNone(v.get_vocabulary("no-such-domain-xyz"))

    def test_the_shipped_vocabularies_are_present(self):
        self.assertEqual(v.AI_ACT_VOCAB.domain, "ai-act")
        self.assertEqual(v.NEUTRAL_VOCAB.domain, "neutral")

    def test_a_card_can_be_made_for_a_registered_domain(self):
        card = v.make_card("neutral", description="a subject under assessment")
        self.assertIsInstance(card, v.SubjectCard)


class TestJurisdictionPacks(unittest.TestCase):
    def test_registering_a_court_pack_adds_its_entries(self):
        before = len(v.court_entries())
        v.register_court_pack("test-us", [
            (r"\bSupreme Court of the United States\b", "SCOTUS",
             "Supreme Court of the United States", "court-judgment", 1, "BINDING")])
        after = v.court_entries()
        self.assertEqual(len(after), before + 1)
        self.assertTrue(any(e[1] == "SCOTUS" for e in after))

    def test_registering_judgment_markers_adds_patterns(self):
        before = len(v.judgment_marker_patterns())
        v.register_judgment_markers("test-jm", [r"\bheld that\b"])
        self.assertGreater(len(v.judgment_marker_patterns()), before)

    def test_registering_instrument_vocab_extends_role_steps(self):
        v.register_instrument_vocab("test-iv", role_steps={"test-role": "test-step"})
        self.assertEqual(v.role_steps().get("test-role"), "test-step")

    def test_a_jurisdiction_is_added_without_an_engine_change(self):
        """The doctrine: adding a jurisdiction is registration, not code."""
        v.register_court_pack("test-fr", [
            (r"\bCour de cassation\b", "CASS", "Cour de cassation",
             "court-judgment", 1, "BINDING")])
        self.assertTrue(any(e[1] == "CASS" for e in v.court_entries()))


class TestRequirementsHouse(unittest.TestCase):
    def test_a_required_artifact_becomes_a_room(self):
        house = v.build_house(
            obligations=[],
            artifacts=[{"solution": {"artifact": "technical-documentation",
                                     "artifact_name": "Technical Documentation",
                                     "category": "conformity",
                                     "trigger_phrase": "Art. 11"}}],
            domain="test", title="Test")
        self.assertIsInstance(house, v.RequirementsHouse)
        self.assertGreaterEqual(len(house.rooms), 1)
        self.assertTrue(all(isinstance(r, v.Room) for r in house.rooms))

    def test_a_house_with_no_atoms_is_empty_not_invented(self):
        house = v.build_house(obligations=[], artifacts=[], domain="test")
        self.assertEqual(house.rooms, [])

    def test_the_house_is_deterministic(self):
        args = dict(obligations=[], domain="test",
                    artifacts=[{"solution": {"artifact": "risk-management-system",
                                             "artifact_name": "Risk Management System",
                                             "category": "conformity"}}])
        first, second = v.build_house(**args), v.build_house(**args)
        self.assertEqual([r.room_id for r in first.rooms],
                         [r.room_id for r in second.rooms])


class TestExtractionBoundary(unittest.TestCase):
    """What makes this a package rather than a copy of part of the engine."""

    def test_no_module_imports_an_engine(self):
        """The engines import THIS. If that reverses, the split has failed."""
        forbidden = ("workspaces", "loomground_solver", "loomground_governance")
        offenders = []
        for path in SRC.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                mod = (node.module if isinstance(node, ast.ImportFrom) else None) or ""
                names = [a.name for a in getattr(node, "names", [])] if isinstance(node, ast.Import) else []
                for candidate in [mod, *names]:
                    if candidate.split(".")[0] in forbidden:
                        offenders.append(f"{path.name}: {candidate}")
        self.assertEqual(offenders, [])

    def test_the_text_pipeline_did_not_come_along(self):
        """`build_house_from_text` needs the engine's extractors. A copy out here
        would be the parallel structure this split exists to avoid."""
        self.assertFalse(hasattr(v.requirements_house, "build_house_from_text"))
        self.assertTrue(hasattr(v.requirements_house, "build_house"))

    def test_the_package_is_stdlib_only(self):
        import tomllib
        toml = tomllib.loads((SRC.parents[1] / "pyproject.toml").read_text())
        self.assertEqual(toml["project"]["dependencies"], [])

    def test_version_matches_packaging(self):
        import re
        toml = (SRC.parents[1] / "pyproject.toml").read_text()
        declared = re.search(r'^version = "([^"]+)"', toml, re.M).group(1)
        self.assertEqual(v.__version__, declared)


if __name__ == "__main__":
    unittest.main()
