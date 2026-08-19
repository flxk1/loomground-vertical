# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 flxk1
"""loomground-vertical — the surface a domain vertical registers itself through.

A vertical (music rights, medical devices, employment law) needs three things to
plug into the stack, and none of them is engine work:

  * a **vocabulary** — what the facets of its subject are, and what the values
    mean (:mod:`.subject_card`);
  * a **jurisdiction pack** — its courts, judgment markers and instrument
    vocabulary (:mod:`.jurisdiction_packs`);
  * a **requirements house** — its obligations and required artifacts arranged
    into rooms (:mod:`.requirements_house`).

Extracted from the engine because it was never engine code: these are pure data
plus small registries, with no imports from the engines — the engines import
*this*. Registering a jurisdiction takes no engine change.

**What deliberately did not come along.** Turning instrument *text* into
obligation and artifact atoms needs an extraction pipeline (classification,
deontic facets, artifact and cross-reference extraction, applicability). That is
engine work, and a copy of it living out here would be the parallel structure
this split exists to avoid. :func:`build_house` therefore assembles a house from
atoms it is *handed*, which also frees a vertical to supply atoms from any
source without adopting the pipeline.

Stdlib only. No engine dependency, in either direction.
"""

from __future__ import annotations

from . import jurisdiction_packs, requirements_house, subject_card
from .jurisdiction_packs import (
    ask_synonyms, court_entries, judgment_marker_patterns, register_court_pack,
    register_instrument_vocab, register_judgment_markers, role_steps,
    room_cues_extra,
)
from .requirements_house import RequirementsHouse, Room, build_house
from .subject_card import (
    AI_ACT_VOCAB, NEUTRAL_VOCAB, UNKNOWN, DomainVocabulary, FacetSpec,
    SubjectCard, get_vocabulary, make_card, register_vocabulary,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # submodules — the registries are stateful, so callers often want the module
    "subject_card", "jurisdiction_packs", "requirements_house",
    # subject vocabulary
    "FacetSpec", "DomainVocabulary", "SubjectCard", "UNKNOWN",
    "AI_ACT_VOCAB", "NEUTRAL_VOCAB",
    "register_vocabulary", "get_vocabulary", "make_card",
    # jurisdiction packs
    "register_court_pack", "court_entries",
    "register_judgment_markers", "judgment_marker_patterns",
    "register_instrument_vocab", "role_steps", "room_cues_extra", "ask_synonyms",
    # requirements house
    "Room", "RequirementsHouse", "build_house",
]
