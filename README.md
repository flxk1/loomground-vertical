# loomground-vertical

Domain-registration contract: the subject vocabulary, jurisdiction pack, and requirements house a vertical registers through.

## Install

```
pip install git+https://github.com/flxk1/loomground-vertical
```

## Usage

```python
from loomground_vertical import DomainVocabulary, FacetSpec, build_house, register_vocabulary

register_vocabulary(DomainVocabulary(
    domain="music-rights",
    facets=(FacetSpec(name="right", values=("mechanical", "performance", "sync")),),
))
house = build_house(
    domain="music-rights", title="Licensing duties",
    obligations=[{"solution": {"operator": "SHALL", "bearer": "licensee",
                               "action": "account for royalties quarterly", "source_eId": "s.15"}}],
    artifacts=[{"solution": {"artifact": "royalty-statement",
                             "artifact_name": "Royalty Statement", "category": "reporting"}}],
)
for r in house.rooms:
    print(r.title, r.category, len(r.obligations))
```

```
Royalty Statement reporting 0
Obligations on: licensee obligation 1
```

## Contracts

| Artifact | Register | Read |
|---|---|---|
| vocabulary | `register_vocabulary(DomainVocabulary(domain, facets, subsumption=()))` | `get_vocabulary(domain)` → vocabulary or `None` · `make_card(domain, …)` → `SubjectCard` |
| jurisdiction pack | `register_court_pack` · `register_judgment_markers` · `register_instrument_vocab` | `court_entries` · `judgment_marker_patterns` · `role_steps` · `room_cues_extra` · `ask_synonyms` |
| requirements house | `build_house(obligations, artifacts, cross_refs=None, …)` | `RequirementsHouse.rooms` → `Room(title, category, obligations)` |

Registries are process-global and additive. `build_house` takes atoms; text extraction stays in the host engine. Semantics and limits: `docs/semantics.md`.

## Family

Domain-registration contract. The three registered artifacts: vocabulary, jurisdiction pack, requirements house. Consumes: stdlib only · consumed by: RVND and the domain verticals registering through it · pipeline position: outside the reasoning pipeline; the engine imports this package.

## Status

Version 0.1.0 · 15 tests · 0 dependencies · Python >=3.10 · shipped: 2 vocabularies (`AI_ACT_VOCAB`, `NEUTRAL_VOCAB`) · 1 court pack (`de-eu`, 12 courts) · 3 judgment-marker packs (`de`, `eu`, `en-uk`).

## License

Apache-2.0 · `LICENSES/Apache-2.0.txt` · `NOTICE`
