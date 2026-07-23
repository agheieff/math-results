# Symbolic certificates

All arithmetic is modulo `n=4k`. The affine tables assume odd `k >= 19`;
the five smaller odd values are handled in the final section. Braces below denote
multisets when values coincide. A table row says that the listed row takes
`c0(donor)` (or `c1(donor)` in the phase-one section).
`old` is its base symbol and `new` its repaired symbol. The tables are direct
substitutions into the definition of `H_n`.

For phase zero, the base symbol multiset is one copy of every symbol, plus

```text
D0={2,5,17,25,n-39,n-31,n-23,n-15,n-7}
```

and minus

```text
O0={3,11,19,27,n-37,n-29,n-21,n-13,n-5}.
```

To audit this baseline, write `r=4q+t`. The base columns are
`(4q+1,4q+7,4q,4q+6)` for `t=(0,1,2,3)`. Apart from the two special
`t=0` cells, the first three row classes give `8q+1`, `8q+8`, and
`8q+2`. The `t=3` class gives `8q+11` for `3<=q<=k-7` and `8q+9`
at the nine boundary values. Since multiplication by two permutes
`Z_k` for odd `k`, this enumeration reduces exactly to `D0` and `O0`.

In every phase-zero table below, cancelling common terms from the `old` and
`new` columns leaves exactly `D0` and `O0`, respectively. This proves that
the repaired symbols form a permutation.

The column residues of `c0(4q+t)` are `(1,3,0,2)` for `t=0,1,2,3`,
and the quotient in each class is a translate of `q`; hence `c0` is a
permutation. Every donor list below is a disjoint union of cycles. For
`k>=19`, its constant, `2k+O(1)`, and `n-O(1)` row bands are disjoint, so
the repair still uses every column once.

For omit A, B, and C, respectively, the unmodified `c0` profile fails only
at

```text
{0,4,5,6,10,11},
{0,1,4,5,10,11},
{0,1,4,5,6,10}.
```

All these rows occur in their repair tables. Every other changed row has
the displayed target delta. On unchanged tail rows, the positive row class
uses an even column and has delta `2`, while the negative row class uses an
odd column and has delta `0`; all other unchanged rows have delta `0`.

## Phase zero: omit A

The following rows are common to both classes of odd `k`.

| row | donor | column | delta | old | new |
|---:|---:|---:|---:|---:|---:|
| 0 | `n-4` | `n-3` | 4 | 2 | 1 |
| `n-4` | `n-15` | `n-9` | 0 | `n-7` | `n-13` |
| `n-15` | `n-17` | `n-14` | 0 | `n-24` | `n-29` |
| `n-17` | `n-8` | `n-7` | 0 | `n-31` | `n-24` |
| `n-8` | `n-19` | `n-13` | 0 | `n-15` | `n-21` |
| `n-19` | `n-21` | `n-18` | 0 | `n-32` | `n-37` |
| `n-21` | `n-12` | `n-11` | 0 | `n-39` | `n-32` |
| `n-12` | 6 | 4 | 0 | `n-23` | `n-8` |
| 6 | 4 | 5 | 3 | 10 | 14 |
| 4 | `n-7` | `n-1` | 0 | 5 | 3 |
| `n-7` | `n-1` | 2 | 0 | `n-8` | `n-5` |
| `n-1` | 14 | 12 | 0 | 1 | 11 |
| 14 | 5 | 11 | 0 | 26 | 25 |
| 5 | 0 | 1 | 4 | 16 | 10 |
| 8 | 10 | 8 | 0 | 17 | 16 |
| 10 | 12 | 13 | 4 | 18 | 27 |
| 12 | 11 | 14 | 0 | 25 | 26 |
| 11 | 8 | 9 | 3 | 25 | 23 |

For `k=1 (mod 4)`, add:

| row | donor | column | delta | old | new |
|---:|---:|---:|---:|---:|---:|
| `2k+5` | `2k+8` | `2k+6` | 2 | 15 | 13 |
| `2k+8` | `2k+6` | `2k+7` | 0 | 14 | 15 |
| `2k+6` | `2k+9` | `2k+12` | 0 | 13 | 18 |
| `2k+9` | `2k+5` | `2k+8` | 2 | 23 | 19 |

For `k=3 (mod 4)`, add:

| row | donor | column | delta | old | new |
|---:|---:|---:|---:|---:|---:|
| `2k+8` | `2k+10` | `2k+11` | 0 | 14 | 19 |
| `2k+10` | `2k+9` | `2k+12` | 0 | 21 | 22 |
| `2k+9` | `2k+12` | `2k+10` | 2 | 23 | 21 |
| `2k+12` | `2k+8` | `2k+6` | 0 | 22 | 18 |

## Phase zero: omit B

For `k=1 (mod 4)`:

| row | donor | column | delta | old | new |
|---:|---:|---:|---:|---:|---:|
| 0 | 4 | 5 | 4 | 2 | 9 |
| 4 | 3 | 6 | 0 | 5 | 10 |
| 3 | 10 | 8 | 0 | 9 | 11 |
| 10 | 16 | 17 | 4 | 18 | 31 |
| 16 | 11 | 14 | 0 | 33 | 30 |
| 11 | 8 | 9 | 3 | 25 | 23 |
| 8 | 5 | 11 | 0 | 17 | 19 |
| 5 | 12 | 13 | 4 | 16 | 22 |
| 12 | 6 | 4 | 0 | 25 | 16 |
| 6 | `n-4` | `n-3` | 0 | 10 | 3 |
| `n-4` | `n-15` | `n-9` | 0 | `n-7` | `n-13` |
| `n-15` | `n-9` | `n-6` | 0 | `n-24` | `n-21` |
| `n-9` | `n-16` | `n-15` | 0 | `n-15` | `n-24` |
| `n-16` | `n-19` | `n-13` | 0 | `n-31` | `n-29` |
| `n-19` | `n-21` | `n-18` | 0 | `n-32` | `n-37` |
| `n-21` | `n-12` | `n-11` | 0 | `n-39` | `n-32` |
| `n-12` | 1 | 7 | 0 | `n-23` | `n-5` |
| 1 | 0 | 1 | 3 | 8 | 5 |
| `2k+2` | `2k+8` | `2k+6` | 0 | 5 | 8 |
| `2k+8` | `2k+12` | `2k+10` | 0 | 14 | 18 |
| `2k+12` | `2k+13` | `2k+16` | 0 | 22 | 28 |
| `2k+13` | `2k+9` | `2k+12` | 2 | 31 | 27 |
| `2k+9` | `2k+16` | `2k+14` | 2 | 23 | 25 |
| `2k+16` | `2k+11` | `2k+17` | 0 | 30 | 33 |
| `2k+11` | `2k+2` | `2k+3` | 0 | 28 | 14 |

For `k=3 (mod 4)`:

| row | donor | column | delta | old | new |
|---:|---:|---:|---:|---:|---:|
| 0 | 4 | 5 | 4 | 2 | 9 |
| 4 | 7 | 10 | 0 | 5 | 14 |
| 7 | 14 | 12 | 0 | 17 | 19 |
| 14 | 5 | 11 | 0 | 26 | 25 |
| 5 | `n-4` | `n-3` | 4 | 16 | 6 |
| `n-4` | `n-15` | `n-9` | 0 | `n-7` | `n-13` |
| `n-15` | `n-9` | `n-6` | 0 | `n-24` | `n-21` |
| `n-9` | `n-16` | `n-15` | 0 | `n-15` | `n-24` |
| `n-16` | `n-19` | `n-13` | 0 | `n-31` | `n-29` |
| `n-19` | `n-21` | `n-18` | 0 | `n-32` | `n-37` |
| `n-21` | `n-12` | `n-11` | 0 | `n-39` | `n-32` |
| `n-12` | 1 | 7 | 0 | `n-23` | `n-5` |
| 1 | 0 | 1 | 3 | 8 | 5 |
| 2 | 3 | 6 | 0 | 2 | 8 |
| 3 | 2 | 0 | 0 | 9 | 3 |
| 8 | 10 | 8 | 0 | 17 | 16 |
| 10 | 12 | 13 | 4 | 18 | 27 |
| 12 | 11 | 14 | 0 | 25 | 26 |
| 11 | 8 | 9 | 3 | 25 | 23 |
| `2k-1` | `2k+2` | `2k+3` | 0 | 4 | 2 |
| `2k+2` | `2k+4` | `2k+2` | 0 | 5 | 4 |
| `2k+4` | `2k+6` | `2k+7` | 0 | 6 | 11 |
| `2k+6` | `2k+9` | `2k+12` | 0 | 13 | 18 |
| `2k+9` | `2k+8` | `2k+6` | 2 | 23 | 17 |
| `2k+8` | `2k-1` | `2k+5` | 0 | 14 | 13 |

## Phase zero: omit C

This table is valid in both odd residue classes.

| row | donor | column | delta | old | new |
|---:|---:|---:|---:|---:|---:|
| 0 | `n-4` | `n-3` | 4 | 2 | 1 |
| `n-4` | `n-15` | `n-9` | 0 | `n-7` | `n-13` |
| `n-15` | `n-17` | `n-14` | 0 | `n-24` | `n-29` |
| `n-17` | `n-8` | `n-7` | 0 | `n-31` | `n-24` |
| `n-8` | `n-19` | `n-13` | 0 | `n-15` | `n-21` |
| `n-19` | `n-21` | `n-18` | 0 | `n-32` | `n-37` |
| `n-21` | `n-12` | `n-11` | 0 | `n-39` | `n-32` |
| `n-12` | 6 | 4 | 0 | `n-23` | `n-8` |
| 6 | 4 | 5 | 3 | 10 | 14 |
| 4 | `n-7` | `n-1` | 0 | 5 | 3 |
| `n-7` | `n-1` | 2 | 0 | `n-8` | `n-5` |
| `n-1` | 5 | 11 | 0 | 1 | 10 |
| 5 | 8 | 9 | 4 | 16 | 18 |
| 8 | 10 | 8 | 0 | 17 | 16 |
| 10 | 12 | 13 | 4 | 18 | 27 |
| 12 | 1 | 7 | 0 | 25 | 19 |
| 1 | 0 | 1 | 3 | 8 | 5 |
| `2k+2` | `2k+8` | `2k+6` | 0 | 5 | 8 |
| `2k+8` | `2k+2` | `2k+3` | 0 | 14 | 11 |

The forced-entry audit is now immediate from the tables. Omit A uses rows 6
and 11 at columns 5 and 9, while row 1 is not at column 1. Omit B uses rows
1 and 11 at columns 1 and 9, while row 6 has delta zero. Omit C uses rows 1
and 6 at columns 1 and 5, while row 11 is unchanged with delta zero.

## Phase `+4`: omit A

The actual `c1=c0+4` diagonal has excess multiset

```text
D1={9,9,13,21,29,n-35,n-27,n-19,n-11,n-3}
```

and omitted set

```text
O1={7,14,15,22,31,n-33,n-25,n-17,n-9,n-1}.
```

A row-class enumeration gives the repeated-symbol rows

| symbol | rows |
|---:|:---|
| 9 | `0,4,2k+2` |
| 13 | `3,6` |
| 21 | `7,8` |
| 29 | `11,12` |
| `n-35` | `n-21,n-20` |
| `n-27` | `n-17,n-16` |
| `n-19` | `n-13,n-12` |
| `n-11` | `n-9,n-8` |
| `n-3` | `n-5,n-4` |

Thus symbol 9 contributes two excess copies and the other rows contribute
one each, giving `D1`; the ten absent values are exactly `O1`.

Since `c1=c0+4`, it is a column permutation. Its unmodified omit-A profile
fails only at `{4,5,6,10,11}`, all of which occur below. The same parity
argument as for `c0` handles every unchanged tail row.

For `k=1 (mod 4)` the changed rows are:

| row | donor | column | delta | old | new |
|---:|---:|---:|---:|---:|---:|
| 0 | `n-12` | `n-7` | 4 | 9 | `n-3` |
| `n-12` | `n-21` | `n-14` | 0 | `n-19` | `n-26` |
| `n-21` | `n-14` | `n-12` | 0 | `n-35` | `n-33` |
| `n-14` | `n-8` | `n-3` | 0 | `n-26` | `n-17` |
| `n-8` | `n-17` | `n-10` | 0 | `n-11` | `n-18` |
| `n-17` | `n-10` | `n-8` | 0 | `n-27` | `n-25` |
| `n-10` | `n-4` | 1 | 0 | `n-18` | `n-9` |
| `n-4` | 6 | 8 | 0 | `n-3` | 4 |
| 6 | 0 | 5 | 3 | 13 | 14 |
| 4 | 14 | 16 | 0 | 9 | 20 |
| 14 | 5 | 15 | 0 | 30 | 29 |
| 5 | 8 | 13 | 4 | 20 | 22 |
| 8 | `n-3` | 7 | 0 | 21 | 15 |
| `n-3` | `n-5` | 2 | 0 | 4 | `n-1` |
| `n-5` | 10 | 12 | 0 | `n-3` | 7 |
| 10 | 12 | 17 | 4 | 23 | 31 |
| 12 | 11 | 18 | 0 | 29 | 30 |
| 11 | 4 | 9 | 3 | 29 | 23 |

For `k=3 (mod 4)` only the first donor cycle changes; its table is:

| row | donor | column | delta | old | new |
|---:|---:|---:|---:|---:|---:|
| 0 | `n-12` | `n-7` | 4 | 9 | `n-3` |
| `n-12` | `n-21` | `n-14` | 0 | `n-19` | `n-26` |
| `n-21` | `n-14` | `n-12` | 0 | `n-35` | `n-33` |
| `n-14` | `n-16` | `n-11` | 0 | `n-26` | `n-25` |
| `n-16` | `n-9` | `n-2` | 0 | `n-27` | `n-18` |
| `n-9` | `n-10` | `n-8` | 0 | `n-11` | `n-17` |
| `n-10` | `n-4` | 1 | 0 | `n-18` | `n-9` |
| `n-4` | 6 | 8 | 0 | `n-3` | 4 |
| 6 | 0 | 5 | 3 | 13 | 14 |

The second donor cycle is the last nine constant/high rows of the preceding
`k=1 (mod 4)` table, beginning at row 4. In either residue class, cancelling
the old and new columns leaves exactly `D1` and `O1`. Thus the phase-one
symbols are also a permutation.

## Empty four-way intersection

Outside the finite cycle supports, the three phase-zero transversals use
`c0(r)` and the fourth uses `c1(r)=c0(r)+4`, so no entry is common there.
Inside the supports, it is enough to inspect rows where the first three
columns agree. For `k=1 (mod 4)` these are:

| row | common phase-zero column | phase-one column |
|---:|---:|---:|
| `n-21` | `n-11` | `n-12` |
| `n-19` | `n-18` | `n-9` |
| `n-14` | `n-16` | `n-3` |
| `n-10` | `n-12` | 1 |
| `n-5` | `n-2` | 12 |
| `n-4` | `n-9` | 8 |
| `n-3` | 3 | 2 |

For `k=3 (mod 4)` they are:

| row | common phase-zero column | phase-one column |
|---:|---:|---:|
| 8 | 8 | 7 |
| 10 | 13 | 17 |
| `n-21` | `n-11` | `n-12` |
| `n-19` | `n-18` | `n-9` |
| `n-14` | `n-16` | `n-11` |
| `n-10` | `n-12` | 1 |
| `n-5` | `n-2` | 12 |
| `n-4` | `n-9` | 8 |
| `n-3` | 3 | 2 |

Every pair in the last two columns is unequal for `k>=19`. Hence the four
transversals have empty intersection.

## Collision-boundary certificates

For `k in {9,11,13,15,17}`, the uniform phase-zero A/B supports collide.
The replacement donor cycles are the `_FINITE_A` and `_FINITE_B` constants
in `explicit.py`. Written out, they are:

```text
k=9:
 A: (0,16,5); (4,21,27,18,31,10,20,11,8,6); (23,26,28)
 B: (0,20,31,12,9,19,2,4,5,28,1); (8,11); (10,24,30,16)
k=11:
 A: (0,32,1,11,8,2,24,35,30,27,6,4,39,10,40,5)
 B: (0,36,23,4,9,27,24,1); (5,20,33,11,8,10,40); (32,38)
k=13:
 A: (0,32,35,6,4,5); (8,10,40,34,44,33,11); (22,48,43)
 B: (0,28,5,36,43,16,45,31,42,40,1); (4,11,8,10,48,50)
k=15:
 A: (0,40,53,51,38,52,55,26,44,5); (4,11,8,10,48,6)
 B: (0,4,47,10,56,3,26,52,5,40,1); (2,11,8); (32,43,58)
k=17:
 B: (0,36,43,59,42,55,20,66,48,1); (4,11,8,13,63,10); (5,52)
```

These cycle lists are the finite certificate data.
The phase-zero C and phase-one A formulas remain uniform.

The exact finite verification results are:

| `k` | `T_A` | `T_B` | `T_C` | `T_A+` | common entries |
|---:|:---:|:---:|:---:|:---:|---:|
| 9 | pass | pass | pass | pass | 0 |
| 11 | pass | pass | pass | pass | 0 |
| 13 | pass | pass | pass | pass | 0 |
| 15 | pass | pass | pass | pass | 0 |
| 17 | pass | pass | pass | pass | 0 |

Here `pass` means that the selected rows, columns, and symbols are all
permutations, the target delta profile holds row by row, the two required
forced entries occur, and the omitted forced entry does not. The verifier
performs these checks directly from the defining cases of `H_n`; it does not
enumerate other transversals.
