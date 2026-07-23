# Certificate audit

## Exact partition semantics

The first eight inner colors are immutable in the original open-strip state. Splitting
the computation into one fiber for each of their \(3^8=6561\) values therefore neither
drops states nor changes dominance. It only prevents unrelated fibers from occupying one
monolithic hash table.

Within a fiber, the local key contains a nonzero marker, the latest outer color, the
latest eight inner colors, and the exact \(Y\)-count. The minimum \(B\)-count is stored as
the value. Every transition checks the new spoke, outer edge, and step-eight inner edge.
Closure checks all nine wrap edges and \(|Y|=n\).

At length \(\ell\), the pruning

\[
Y\ge\max(0,2\ell-72)
\]

removes only states that cannot reach any requested endpoint through 72, since each
future column contributes at most two \(Y\)'s. The upper pruning \(Y\le72\) is immediate.

## Canonical fingerprints

The local memory key packs the marker at bit 0, latest outer color at bit 1, inner queue
at bit 3, and \(Y\)-count at bit 16; its minimum cost starts at bit 32.

For transcript metrics, every state is reconstructed in the canonical monolithic layout

```text
u0=1 | first<<2 | last<<15 | queue<<17 | Y<<30 | cost<<40
```

before applying SplitMix64. Counts and 64-bit XOR/sum fingerprints are combined across
thread-local transcripts using their associative operations, so scheduling cannot affect
the result.

With compile-time \(k=7\) control parameters, the same reconstruction becomes

```text
u0=1 | first<<2 | last<<14 | queue<<16 | Y<<28 | cost<<40
```

which exactly matches the frozen monolithic \(k=7\) encoding. The partitioned run
reproduced every one of its 50 layer counts and fingerprints, plus closure counts

```text
59,0,0,0,0,92,0,0,0,0,0,0,0
```

and the two positive closure XOR/sum pairs.

## Outer-\(B\) anchoring

If no outer vertex were \(B\), the outer cycle would be monochromatic. All outer \(A\)
forbids all inner \(Y\). All outer \(Y\) already supplies the required 64--72 \(Y\)'s;
the inner layer can then contain neither \(A\) nor \(Y\), so it contains more than 17
\(B\)'s. Thus some outer \(B\) exists and rotation can place it at \(u_0\).

## Frozen evidence

- Native source SHA-256:
  `b010841c02bd630f87d9500076e2de0b36e79043e58461df20da280d0556a7a0`.
- First \(k=8\) binary SHA-256:
  `ab3c4cff63b95e4faf81f283aa7f53ee85dc9ac1ca62bf0410b8a30305ea552b`.
- Full transcript SHA-256:
  `9f53f1601eac5cd136a949829955d361caa9240a63e8f7e64dbd3b210237701d`.
- Transcript-file SHA-256:
  `3740e0e706f87abf4546e6a9aeffe81b6d2906cd6a08c2ec2336814b809e7171`.
- \(k=7\) control binary SHA-256:
  `e78cd07ccb17bdf416fc755fb3387da8c886d9071a533c048aaf9e82056fdc14`.
- Pre-promotion certificate-artifact SHA-256:
  `214b0981d5e5e48b1d34001ddd88edb71c47b6e237976cc27f3170fb0ba5fe64`.
- Pre-promotion full-replay canonical certificate SHA-256:
  `836e2a4ac79e5f632468b2f780fbfc8917039b13044fe1bb212f72720b3063c2`.
- Promoted certificate-artifact SHA-256:
  `d4b9ecfd9d4edb72507131ab14b05920bd1fdb3c6a1581812406cae7cd2c6a3a`.
- Promoted canonical certificate SHA-256:
  `051add3c927d70153125c5ec595dd0671792b7aa8c897d95c904bf7071be61ca`.

The maximum aggregate layer count is 2,638,499,949. This is not simultaneous memory:
the first-boundary fibers are processed separately, and the observed first-run RSS stayed
below 0.5 GiB.

## Replay record

The first exact native run took about 46 minutes, stayed below 0.5 GiB RSS, and produced
the frozen transcript above with closure counts

```text
97,0,0,0,0,0,0,0,0
```

A second full package replay exited zero, wrote nothing to standard error, and emitted

```text
certificate=PASS sha256=836e2a4ac79e5f632468b2f780fbfc8917039b13044fe1bb212f72720b3063c2
```

The independent root replay then exited zero with the same exact output. Both full
replays preceded the promotion edit. That edit changes only the Python/JSON status
metadata to PASS; it does not change the native source or frozen transcript. The promoted
JSON was regenerated cheaply from that transcript and compared exactly with the
checked-in artifact.

## Positive control scope

The independently replayed \(P(64,8)\) block has exact internal boundary 16 and word
SHA-256
`ef38f30dde297887f7276d3fe9971b3694b0b975697f97cf9456ecc93aa5665b`.
It is only a separator control and makes no claim about \(Z(P(64,8))\).
