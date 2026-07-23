# Exact result

The exact computation and independent replays prove

\[
Z(P(n,8))=18\qquad(n\ge65).
\]

The boundary-\(\le17\) closure counts at orders \(64,\ldots,72\) are

```text
97,0,0,0,0,0,0,0,0
```

Thus order 64 is a positive control and orders \(65,\ldots,72\) are the eight pathwidth
bases. The full 65-layer transcript is frozen in `artifacts/native-transcript.txt`.

The known general construction gives the matching 18-vertex upper bound. The literature
search recorded in `PRIOR_ART.md` found no fixed-\(k=8\) eventual theorem, but that is not
a comprehensive novelty claim.

The initial native run, a second full package replay, and an independent root replay all
agree. Replay provenance and the later metadata-only promotion are recorded in
`AUDIT.md`.
