# Prior art checked on 23 July 2026

1. J. S. Alameda, E. Curl, A. Grez, L. Hogben, O. Kingston, A. Schulte, D. Young, and
   M. Young, “Families of graphs with maximum nullity equal to zero forcing number,”
   *Special Matrices* 6 (2018), 56–67,
   [doi:10.1515/spma-2018-0006](https://doi.org/10.1515/spma-2018-0006).
   Theorem 2.2 gives \(Z(P(n,k))\le2k+2\). This package supplies an explicit descending
   full-column schedule and verifier for that bound.
2. S. Rashidi, N. Shajareh Poursalavati, and M. Tavakkoli, “Computing the zero forcing
   number for generalized Petersen graphs,” *J. Algebra Comb. Discrete Struct. Appl.* 7
   (2020), 183–193,
   [doi:10.13069/jacodesmath.729465](https://doi.org/10.13069/jacodesmath.729465).
   It gives several claimed exact subfamilies; its \(P(n,3)\) lower proof was corrected in
   2026 and is not used here.
3. Y. Wang, M. Cao, Z. Lv, and M. Lu, “Treewidth of Generalized Hamming Graph, Bipartite
   Kneser Graph and Generalized Petersen Graph,” *Electronic Journal of Combinatorics* 33
   (2026), #P1.7, [doi:10.37236/12892](https://doi.org/10.37236/12892).
   It studies treewidth bounds for generalized Petersen graphs but does not state the
   \(k\)-column reduction proved here.

A targeted search found no prior statement of
\(P(n-k,k)\preccurlyeq P(n,k)\) in this form. The finite-basis corollary is an immediate use
of that reduction with standard pathwidth facts.
