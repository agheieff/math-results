# Proof dependency graph

```mermaid
flowchart TD
    O36["Sibling proof: all orders <= 36"] --> M37
    PST["Plummer--Stiebitz--Toft: odd order and connectivity"] --> M37
    M37["Minimum counterexample would have n=37, chi=19, kappa>=19"]
    R39["Grinstead--Roberts: R(3,9)=36"] --> W9
    SS["Scully--Song clique threshold"] --> W9
    M37 --> W9["Only omega=9 remains"]
    W9 --> EMPTY["Empty support: K10 + 9 seagulls"]
    W9 --> J["Nonempty supports: good-pair graph J"]
    J --> MATCH["Two disjoint touching good edges"]
    MATCH --> CORE["K11 core on 13 vertices"]
    CORE --> REM["24-vertex remainder meets k=8 packing conditions"]
    CS["Chudnovsky--Seymour seagull criterion"] --> EMPTY
    CS --> REM
    EMPTY --> K19["K19 minor"]
    REM --> K19
    K19 --> O38["Hadwiger holds through order 38"]
```

The new argument consists of the support counts and component/Hall
argument at `J` and `MATCH`, plus the elementary verification of the
packing hypotheses at `EMPTY` and `REM`. External or sibling trust
boundaries are:

- the minimum-counterexample reduction of Plummer--Stiebitz--Toft;
- the exact Ramsey value \(R(3,9)=36\);
- Scully--Song's dominating-minor clique threshold;
- Chudnovsky--Seymour's seagull-packing theorem;
- the sibling proof through order 36.
