# Thesis Patterns

`thesis` is an internal execution hint for later writing, not reader-facing copy.

Requirements:

- one sentence
- subsection-specific nouns
- ties the subsection to 1-2 leading axes
- avoids narration stems like “This subsection …”
- stays conservative when evidence is abstract-only
- subsection-local title/axes cues outrank global goal cues; a survey-wide goal must not cause adjacent H3s to inherit the wrong thesis family

The machine-readable source of truth is `assets/phrase_packs/thesis_patterns.json`.

Pattern families:

- fulltext-rich mode: emphasize decision-relevant trade-offs under shared protocols
- abstract-only mode: emphasize interpretability, reporting conventions, and protocol-aware synthesis

Good shape:

- “Design choices in X create decision-relevant trade-offs—especially in Y—and meaningful comparisons depend on consistent evaluation protocols.”

Bad shape:

- “This subsection introduces the main approaches to X.”
- “There are many methods for X and they have strengths and weaknesses.”
