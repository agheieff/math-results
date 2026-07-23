# Prior-art and frontier audit

**Audit timestamp:** 2026-07-23 (UTC)  
**Question:** Is every finite simple \(K_7\)-minor-free graph 7-colourable?

## Primary sources

1. Martin Rolek, Zi-Xia Song, and Robin Thomas, “Properties of 8-contraction-critical graphs
   with no \(K_7\) minor,” *European Journal of Combinatorics* 110 (2023), 103711,
   [arXiv:2208.07335](https://arxiv.org/abs/2208.07335),
   [DOI:10.1016/j.ejc.2023.103711](https://doi.org/10.1016/j.ejc.2023.103711).
   Theorem 1.2 gives \(8\le\delta\le9\), \(n_8\le1\), \(n_9\ge30-2n_8\), and the exact
   degree-9 neighborhood dichotomy used in `RECONNAISSANCE.md`. Its abstract states that the
   7-colour target remains open.

2. Martin Rolek and Zi-Xia Song, “Coloring graphs with forbidden minors,” *Journal of
   Combinatorial Theory, Series B* 127 (2017), 14--31,
   [arXiv:1606.05507](https://arxiv.org/abs/1606.05507),
   [DOI:10.1016/j.jctb.2017.05.001](https://doi.org/10.1016/j.jctb.2017.05.001).
   Theorem 1.3 proves that graphs with no \(K_t\) minor are
   \((2t-6)\)-colourable for \(t\in\{7,8,9\}\), hence 8-colourable at \(t=7\).
   Lemma 1.7 is the generalized Kempe-chain result used to motivate the frozen local lemma.

3. Sergey Norin and Agnes Totschnig, “Every graph with no \(K_7^\vee\)-minor is
   6-colorable,” [arXiv:2507.03244](https://arxiv.org/abs/2507.03244) (2025 preprint).
   Here \(K_7^\vee\) is \(K_7\) with two adjacent edges deleted. This treats a stricter
   minor-closed class, so it does not close the frozen target; it does imply that any target
   counterexample contains a \(K_7^\vee\) minor.

4. Michael Lafferty, Runrun Liu, Martin Rolek, and Gexin Yu, “Connectivity of
   contraction-critical graphs,” [arXiv:2509.07144](https://arxiv.org/abs/2509.07144)
   (2025 preprint). Its improvements start at contraction-criticality 17; it does not improve the
   7-connectivity input at \(k=8\) or close the target.

5. Ahmad Albar and Daniel Gonçalves, “On triangles in \(K_r\)-minor free graphs,”
   *Journal of Graph Theory* 88 (2018), 154--160,
   [arXiv:1304.5468](https://arxiv.org/abs/1304.5468),
   [DOI:10.1002/jgt.22203](https://doi.org/10.1002/jgt.22203).
   This is the earlier computer-assisted 8-colour result generalized and reproved
   computer-free by Rolek--Song.

6. Paul Seymour, “Hadwiger's conjecture,”
   [survey manuscript](https://web.math.princeton.edu/~pds/papers/hadwiger/paper.pdf).
   This supplies background; frontier claims above use the research papers.

## Search log

The audit searched arXiv/web indexes, Crossref, journal pages, author publication pages, and
forward-looking 2024--2026 queries using:

- `"K7-minor-free" "7-colorable"` and spelling variants;
- `"every graph with no K_7 minor is 7-colorable"`;
- `"8-contraction-critical" "K7"`;
- the exact RST title, DOI, author trio, and citing-title searches;
- `"Hadwiger" "K7" coloring 2024`, `2025`, and `2026`;
- `"K_7^vee" minor`, `"K7" "two edges with a common end"`, and equivalent notation;
- negation/equivalent language: `chromatic number 8 no K7 minor`.

Crossref confirms the 2023 RST journal metadata. The arXiv records and
[current Zi-Xia Song publication list](https://sciences.ucf.edu/math/zxsong/publications/) yielded
no later paper claiming the target. The search did locate the 2025 Norin--Totschnig restricted-class
theorem above. zbMATH Open's API rejected the submitted query, while MathSciNet and automated
Google Scholar/Semantic Scholar citation views were unavailable in this environment; these are
recorded limitations, not evidence of absence. No primary-source closure was located.

## Near matches that do not settle the target

- [Boris Albar, arXiv:1402.2806](https://arxiv.org/abs/1402.2806) proves 7-colourability
  under exclusion of \(K_7^-\), a stricter graph class.
- [Lafferty and Song, arXiv:2208.07338](https://arxiv.org/abs/2208.07338) prove that
  excluding every member of \(\mathcal K_8^{-4}\) implies 7-colourability, not that every
  \(K_7\)-minor-free graph is 7-colourable.
- [Norin and Totschnig, arXiv:2507.03244](https://arxiv.org/abs/2507.03244) prove
  6-colourability after additionally excluding the proper subgraph \(K_7^\vee\); a general
  \(K_7\)-minor-free graph may still contain that minor.
- [arXiv:2510.12564](https://arxiv.org/abs/2510.12564) and
  [arXiv:2510.12567](https://arxiv.org/abs/2510.12567) concern dominating variants or restricted
  graph classes; neither proves the frozen universal statement.

## Audit conclusion

As of the audit date, the authoritative exact frontier located consists of the published universal
8-colour bound, RST's 2023 structure theorem, and Norin--Totschnig's 2025 theorem for the stricter
\(K_7^\vee\)-minor-free class. The frozen 7-colour target remains an open parent problem in this
lane. The finite object checked here addresses only a newly proposed auxiliary lemma, so it has no
novelty or significance claim relative to the parent problem.
