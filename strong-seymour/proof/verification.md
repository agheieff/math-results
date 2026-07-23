# Certificate verification

Committed artifacts:

```text
CNF:   7,111 variables; 18,992 clauses; 263 KiB
DRAT:  130,787 lemma lines; 14 MiB
```

The CNF was solved by CaDiCaL 2.2.1 at commit
`4198d817d0dcde5b1240eefbff70b555b7df2af9`. Its 25.09 MiB ASCII DRAT trace was checked
and core-trimmed by `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. The committed trimmed trace was then checked
again against the original CNF:

```text
c parsing input formula with 7111 variables and 18992 clauses
c detected empty clause; start verification via backward checking
c 3753 of 18992 clauses in core
c 128841 of 130787 lemmas in core using 4000054 resolution steps
c 0 RAT lemmas in core; 23004 redundant literals in core lemmas
s VERIFIED
c verification time: 2.201 seconds
```

The first in-memory PySAT trace was explicitly discarded because it did not pass independent
checking. Only the standalone CaDiCaL trace above is committed.

To reproduce the semantic CNF and check the proof, build the official checker and run:

```bash
git clone https://github.com/marijnheule/drat-trim.git /tmp/drat-trim
git -C /tmp/drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
cc -std=gnu17 -O2 /tmp/drat-trim/drat-trim.c -o /tmp/drat-trim/drat-trim
uv sync
uv run strong-seymour-verify \
  --cnf certificates/order13.cnf \
  --proof certificates/order13.drat \
  --drat-trim /tmp/drat-trim/drat-trim
```

Expected hashes are in `certificates/order13.sha256`. The verifier regenerates the CNF
byte-for-byte before invoking `drat-trim`.

