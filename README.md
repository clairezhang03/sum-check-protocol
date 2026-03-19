# Sum-Check Protocol — Manim Explainer Video

A 3Blue1Brown-style educational animation explaining the **Sum-Check Protocol** —
an interactive proof system that lets a Prover convince a Verifier that the sum
of a multivariate polynomial over all Boolean inputs equals a claimed value T,
using only O(vd) communication instead of 2ᵛ evaluations.

---

## Video Structure

| Scene | Topic |
|---|---|
| `TitleScene` | Title card |
| `SudokuMotivation` | Motivation: proving impossibility without enumeration |
| `SumCheckProblem` | The Sum-Check problem statement & running example |
| `InteractiveProof` | Interactive Proof Systems: Alice (Prover) & Bob (Verifier) |
| `PrimeFields` | Prerequisite: finite fields of prime order |
| `SchwartzZippel` | The Schwartz-Zippel Lemma |
| `Round1` | Protocol Round 1: sending s₁(X₁), verifier check, random challenge |
| `Round2` | Protocol Round 2: fixing r₁, sending s₂(X₂) |
| `GeneralRounds` | Rounds 3 to v−1: the chain metaphor & communication cost |
| `FinalRound` | Final round: oracle query to g, ACCEPT condition |
| `SoundnessAnalysis` | Completeness, Schwartz-Zippel per round, Union Bound |
| `Conclusion` | Summary & applications (GKR, IP=PSPACE) |

**Running example polynomial:**
```
g(X₁, X₂, X₃) = 2X₁³ + X₁X₃ + X₂X₃     H = 12
```

---

## Prerequisites

- Python 3.8+
- [Manim Community Edition](https://docs.manim.community/en/stable/installation.html) ≥ 0.18
- ffmpeg (for concatenation)
- LaTeX distribution (for MathTex rendering — TeX Live or MiKTeX)

Install Manim:
```bash
pip install manim
```

---

## Rendering

### Preview a single scene (fast, low quality)
```bash
manim -pql sum_check_animation.py TitleScene
```

### Render a single scene at high quality
```bash
manim -pqh sum_check_animation.py Round1
```

### Render & concatenate the full video
```bash
chmod +x render_all.sh
./render_all.sh          # medium quality (default)
./render_all.sh -qh      # high quality (for final export)
```

The final output is written to `sum_check_protocol_full.mp4`.

### Quality flags

| Flag | Resolution | Notes |
|---|---|---|
| `-ql` | 480p15 | Fast preview |
| `-qm` | 720p30 | Good for drafts |
| `-qh` | 1080p60 | Final export |
| `-qk` | 2160p60 | 4K (slow!) |

---

## Project Structure

```
sum_check/
├── sum_check_animation.py   # All 12 Manim scenes
├── render_all.sh            # Batch render + ffmpeg concat
├── requirements.txt
└── README.md
```

---

## Key Concepts Covered

- **Sum-Check problem**: is Σ_{x∈{0,1}ᵛ} g(x) = H?
- **Interactive Proof Systems**: Prover/Verifier model
- **Finite fields 𝔽_p**: arithmetic modulo a prime
- **Schwartz-Zippel Lemma**: two distinct polynomials agree on ≤ d points
- **Protocol mechanics**: round-by-round variable pinning
- **Soundness**: Union Bound gives δₛ ≤ vd/|𝔽|
- **Completeness**: honest prover always accepted

---

## References

- Lund, Fortnow, Karloff, Nisan (1992) — original Sum-Check paper
- Shamir (1992) — IP = PSPACE
- Thaler, *Proofs, Arguments, and Zero-Knowledge* (2022) — free textbook
- Goldwasser, Micali, Rackoff (1989) — Interactive Proof Systems

---

## License

MIT
