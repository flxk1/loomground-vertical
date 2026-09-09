# loomground-vertical — semantics, limits, provenance

Moved verbatim from README.md (2026-09-09, README canon). Reference material; the README carries the contract.

The surface a domain vertical registers itself through: a subject vocabulary, a
jurisdiction pack, and a requirements house.

A vertical — music rights, medical devices, employment law — needs three things
to plug into a governance engine, and none of them is engine work. This package
is those three things, as pure data plus small registries. Adding a jurisdiction
is a registration call, not an engine change.

## Install

```
pip install git+https://github.com/flxk1/loomground-vertical
```

Python 3.10+. No dependencies.

## Use

```python
from loomground_vertical import (
    DomainVocabulary, FacetSpec, build_house, court_entries,
    register_court_pack, register_vocabulary,
)

register_vocabulary(DomainVocabulary(
    domain="music-rights",
    facets=(FacetSpec(name="right", values=("mechanical", "performance", "sync")),),
))
register_court_pack("us", [(r"\bSupreme Court of the United States\b", "SCOTUS",
                            "Supreme Court of the United States",
                            "court-judgment", 1, "BINDING")])

house = build_house(
    domain="music-rights", title="Licensing duties",
    obligations=[{"solution": {"operator": "SHALL", "bearer": "licensee",
                               "action": "account for royalties quarterly",
                               "source_eId": "s.15"}}],
    artifacts=[{"solution": {"artifact": "royalty-statement",
                             "artifact_name": "Royalty Statement",
                             "category": "reporting"}}],
)
for r in house.rooms:
    print(r.title, r.category, len(r.obligations))
```

```
courts registered: 13
  'Royalty Statement' [reporting] obligations=0
  'Obligations on: licensee' [obligation] obligations=1
     SHALL licensee: account for royalties quarterly (s.15)
```

Two room kinds are visible there: a **required artifact** becomes a room of its
own, and an obligation that names no artifact is grouped into a room keyed by
the party that bears it.

## API

| | |
|---|---|
| `register_vocabulary(vocab)` / `get_vocabulary(domain)` | the controlled facet vocabulary for a domain |
| `DomainVocabulary(domain, facets, subsumption=())` | facets plus a child→parent taxonomy the matcher walks |
| `FacetSpec(name, values, description="", multi=False)` | one facet and its controlled value set |
| `make_card(domain, …)` → `SubjectCard` | the structured description of the thing being assessed |
| `register_court_pack` / `court_entries` | courts and their authority tier |
| `register_judgment_markers` / `judgment_marker_patterns` | how a judgment is recognised in text |
| `register_instrument_vocab` / `role_steps` / `room_cues_extra` / `ask_synonyms` | instrument vocabulary for a jurisdiction |
| `build_house(obligations, artifacts, cross_refs=None, …)` → `RequirementsHouse` | atoms arranged into rooms |

`AI_ACT_VOCAB` and `NEUTRAL_VOCAB` ship as starting vocabularies.

## Semantics

**Registries are stateful and additive.** Registering is the point; a pack adds
to what is already there rather than replacing it. Register once at import time.

**An unregistered domain returns `None`.** Never another domain's model as a
default — a vocabulary you did not register is not evidence about your subject.

**A house is assembled from atoms it is handed.** Producing atoms from
instrument *text* needs an extraction pipeline (classification, deontic facets,
artifact and cross-reference extraction, applicability). That is the host
engine's work. Keeping it out means a vertical can supply atoms from any source,
and the engine keeps a single implementation instead of a copy living here.

**Shipped packs are a starting library, not a claim of coverage.** The
jurisdictions present are the ones that have been needed so far.

## Limitations

- The registries are process-global module state. Two verticals registering the
  same `pack_id` both land; last write wins per key.
- `build_house` links an obligation to an artifact room by keyword hints. It is
  a heuristic, and an obligation that names its artifact obliquely will land in
  a bearer room instead.
- Nothing here validates a vocabulary against a regulation. It carries what you
  register.

## Provenance

Extracted from a governance engine, where these three modules already had no
imports from the engines — the engines imported *them*. The split makes that
direction explicit and lets a vertical depend on the surface without depending
on the engine.

## Tests

```
pytest -q
```

Includes a boundary test asserting no module here imports an engine: if that
direction ever reverses, the split has failed.

## Licence

Apache-2.0.
