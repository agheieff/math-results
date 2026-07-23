# Certificate

The checker constructs all 46 complement isomorphism types and classifies
all 1,035 pairs:

```text
q1:       644
q2:       354
q3:        30
endpoint:   1
q4:         6
```

The six deep \(q_4\) identities and the endpoint identity are verified as
polynomial identities. After multiplication by
\((n-1)(n-2)(n-3)\), every relevant difference has degree at most 11 in
\(n\) and at most 3 in the formal hook parameter \(k\):

- \(e_4\) has degree at most 8 in \(n\);
- \(V\) has degree at most 6;
- \(S\) has degree at most 5;
- \(C_4\) has degree at most 4;
- the scaled character numerators have total degree at most 3.

Equality on the exact \(12\times4\) grid
\(20\le n\le31\), \(0\le k\le3\) therefore proves each displayed identity.
The formal value \(k=0\) is used only for polynomial interpolation.

Canonical payload SHA-256:

```text
8519991111d6428962c7ac5513e542ecd44e36b689aaf0c00a01d38cb6de2ee0
```

Replay:

```sh
uv run --locked laplacian-hook-all-check
```
