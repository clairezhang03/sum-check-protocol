"""
sum_check_animation.py
======================
Sum-Check Protocol — full explainer video in the style of 3Blue1Brown.
Built with Manim Community Edition.

Render a single scene (low quality, for preview):
    manim -pql sum_check_animation.py TitleScene

Render all scenes at high quality:
    manim -pqh sum_check_animation.py TitleScene
    manim -pqh sum_check_animation.py SudokuMotivation
    ... (see render_all.sh)

Concatenate with ffmpeg:
    ./render_all.sh   (see render_all.sh)
"""

from manim import *
import numpy as np

# ── Global background ─────────────────────────────────────────────────────────
config.background_color = "#1e1e2e"

# ── Colour palette (3B1B-inspired) ────────────────────────────────────────────
PROVER_COLOR = "#5CD0B3"   # Alice / Prover
VERIF_COLOR  = "#FC6255"   # Bob   / Verifier
POLY_COLOR   = "#F4D03F"   # polynomial highlights
FIELD_COLOR  = "#BB93D7"   # field elements / math
ACCENT_COLOR = "#FF9F40"   # section headers / accent
GOOD_COLOR   = "#83C167"   # checkmarks / correct
BAD_COLOR    = "#FF6B6B"   # errors / wrong
DIM_COLOR    = "#555566"   # background / dim text
LINK_COLOR   = "#83C167"   # chain links


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 1 — Title Card
# ══════════════════════════════════════════════════════════════════════════════

class TitleScene(Scene):
    def construct(self):
        title = Text("The Sum-Check Protocol", font_size=54, weight=BOLD)
        sub = Text(
            "An Interactive Proof for Polynomial Sums",
            font_size=30, color=POLY_COLOR
        )
        sub.next_to(title, DOWN, buff=0.5)

        tag = Text(
            "A digest for curious students",
            font_size=22, color=DIM_COLOR
        )
        tag.next_to(sub, DOWN, buff=0.9)

        self.play(Write(title), run_time=2)
        self.play(FadeIn(sub, shift=UP * 0.3), run_time=1.2)
        self.play(FadeIn(tag), run_time=1)
        self.wait(2.5)
        self.play(FadeOut(VGroup(title, sub, tag)))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 2 — Motivation: Proving Impossibility
# ══════════════════════════════════════════════════════════════════════════════

class SudokuMotivation(Scene):
    def construct(self):
        # ── Section header ──────────────────────────────────────────────────
        header = Text("Part 1 — Motivation", font_size=38, color=ACCENT_COLOR, weight=BOLD)
        self.play(Write(header))
        self.wait(0.5)
        self.play(header.animate.to_edge(UP))

        # ── Opening question ───────────────────────────────────────────────
        q = Text(
            "When is checking harder than solving?",
            font_size=34, color=WHITE
        )
        self.play(Write(q), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(q))

        # ── Sudoku setup ───────────────────────────────────────────────────
        sudoku_label = Text("Consider: An Unsolvable Sudoku Puzzle", font_size=30, color=POLY_COLOR)
        sudoku_label.next_to(header, DOWN, buff=0.6)
        self.play(Write(sudoku_label))

        grid = self._make_grid()
        grid.shift(LEFT * 3 + DOWN * 0.5)
        self.play(Create(grid), run_time=1.5)

        # ── Enumeration explanation ────────────────────────────────────────
        lines = VGroup(
            Text("To prove it's unsolvable:", font_size=26, color=VERIF_COLOR),
            Text("  → Try every possible assignment", font_size=24),
            Text("  → Show none of them work", font_size=24),
            MathTex(r"\text{  → Potentially } 9^{81} \text{ checks!}", font_size=28, color=BAD_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        lines.next_to(grid, RIGHT, buff=1.2)

        for line in lines:
            self.play(FadeIn(line, shift=RIGHT * 0.15), run_time=0.55)
            self.wait(0.2)
        self.wait(1)

        # ── Insight ────────────────────────────────────────────────────────
        insight = Text(
            "What if a clever Prover could convince us\n"
            "without enumerating everything?",
            font_size=27, color=GOOD_COLOR
        )
        insight.to_edge(DOWN, buff=0.8)
        self.play(Write(insight), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(VGroup(header, sudoku_label, grid, lines, insight)))

    def _make_grid(self):
        group = VGroup()
        s = 0.58
        # Grid lines (4×4 with thick borders at box boundaries)
        for i in range(5):
            lw = 5 if i % 2 == 0 else 2
            h = Line(LEFT * s * 2, RIGHT * s * 2, stroke_width=lw, color=WHITE)
            h.shift(UP * (i - 2) * s)
            v = Line(UP * s * 2, DOWN * s * 2, stroke_width=lw, color=WHITE)
            v.shift(RIGHT * (i - 2) * s)
            group.add(h, v)

        # Partial assignment
        given = {
            (0, 0): "3", (0, 3): "2",
            (1, 1): "1",
            (2, 2): "4",
            (3, 0): "4", (3, 3): "3",
        }
        for (r, c), val in given.items():
            num = Text(val, font_size=22, color=POLY_COLOR)
            num.move_to(RIGHT * (c - 1.5) * s + UP * (1.5 - r) * s)
            group.add(num)
        return group


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 3 — Introduce the Sum-Check Problem
# ══════════════════════════════════════════════════════════════════════════════

class SumCheckProblem(Scene):
    def construct(self):
        header = Text("The Sum-Check Problem", font_size=42, color=POLY_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        # ── Main formula ───────────────────────────────────────────────────
        formula = MathTex(
            r"H = \!\!\sum_{x_1,\,\ldots,\,x_v\,\in\,\{0,1\}}\!\! g(x_1,\,x_2,\,\ldots,\,x_v)",
            font_size=36
        )
        formula.next_to(header, DOWN, buff=0.55)
        self.play(Write(formula), run_time=2)
        self.wait(0.8)

        # ── Glossary ───────────────────────────────────────────────────────
        glossary = VGroup(
            MathTex(r"g", r"\ :\ \text{multivariate polynomial}", font_size=28),
            MathTex(r"v", r"\ :\ \text{number of variables}", font_size=28),
            MathTex(r"H", r"\ :\ \text{the claimed sum (a single number)}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        glossary.next_to(formula, DOWN, buff=0.5)
        glossary[0][0].set_color(POLY_COLOR)
        glossary[1][0].set_color(ACCENT_COLOR)
        glossary[2][0].set_color(GOOD_COLOR)

        for entry in glossary:
            self.play(FadeIn(entry, shift=UP * 0.1), run_time=0.6)
            self.wait(0.2)
        self.wait(0.5)

        # ── {0,1} restriction note ─────────────────────────────────────────
        note = Text(
            "Variables range over {0,1}  (extends to any finite field!)",
            font_size=24, color=ACCENT_COLOR
        )
        note.next_to(glossary, DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.9)
        self.wait(0.8)

        # ── Running example ────────────────────────────────────────────────
        ex_label = Text("Our running example:", font_size=26)
        ex_poly  = MathTex(
            r"g(X_1,X_2,X_3) = 2X_1^3 + X_1 X_3 + X_2 X_3",
            font_size=34, color=POLY_COLOR
        )
        ex_sum = MathTex(r"H = 12", font_size=34, color=GOOD_COLOR)

        ex_group = VGroup(ex_label, ex_poly, ex_sum).arrange(DOWN, buff=0.3)
        ex_group.next_to(note, DOWN, buff=0.45)

        self.play(Write(ex_label), run_time=0.6)
        self.play(Write(ex_poly),  run_time=1.2)
        self.play(Write(ex_sum),   run_time=0.7)
        self.wait(0.8)

        # ── Verification table ─────────────────────────────────────────────
        self._show_table()

        self.play(FadeOut(VGroup(header, formula, glossary, note, ex_group)))

    def _show_table(self):
        rows = [
            ("(0,0,0)", "0"), ("(0,0,1)", "0"), ("(0,1,0)", "0"), ("(0,1,1)", "1"),
            ("(1,0,0)", "2"), ("(1,0,1)", "3"), ("(1,1,0)", "2"), ("(1,1,1)", "4"),
        ]
        title = Text("Checking H = 12 by enumeration:", font_size=22, color=DIM_COLOR)

        col1 = VGroup(Text("point", font_size=18, color=GREY), *[Text(r[0], font_size=18) for r in rows])
        col2 = VGroup(Text("g(...)", font_size=18, color=GREY), *[Text(r[1], font_size=18, color=POLY_COLOR) for r in rows])
        total_row = VGroup(
            Text("Total:", font_size=18, color=ACCENT_COLOR),
            Text("12",    font_size=18, color=GOOD_COLOR, weight=BOLD)
        )

        col1.arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        col2.arrange(DOWN, buff=0.17)
        table = VGroup(col1, col2).arrange(RIGHT, buff=0.7)
        total_row.arrange(RIGHT, buff=0.5)
        total_row.next_to(table, DOWN, buff=0.12, aligned_edge=LEFT)

        full = VGroup(title, table, total_row).arrange(DOWN, buff=0.25)
        full.scale(0.85).to_corner(DR, buff=0.5)

        self.play(FadeIn(full), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(full))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 4 — Interactive Proof System
# ══════════════════════════════════════════════════════════════════════════════

class InteractiveProof(Scene):
    def construct(self):
        header = Text("Part 2 — Setup", font_size=38, color=ACCENT_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        sub = Text("Interactive Proof Systems", font_size=32, weight=BOLD)
        sub.next_to(header, DOWN, buff=0.4)
        self.play(Write(sub))
        self.wait(0.5)
        self.play(FadeOut(sub))

        # ── Alice (Prover) ─────────────────────────────────────────────────
        alice_circle = Circle(radius=0.75, color=PROVER_COLOR, fill_opacity=0.2)
        alice_text   = Text("Alice\n(Prover)", font_size=22, color=PROVER_COLOR)
        alice_text.move_to(alice_circle)
        alice = VGroup(alice_circle, alice_text).to_edge(LEFT, buff=2).shift(DOWN * 0.4)

        alice_role = Text(
            "Knows the true sum\nGoal: convince Bob",
            font_size=20, color=PROVER_COLOR
        )
        alice_role.next_to(alice, DOWN, buff=0.35)

        # ── Bob (Verifier) ─────────────────────────────────────────────────
        bob_circle = Circle(radius=0.75, color=VERIF_COLOR, fill_opacity=0.2)
        bob_text   = Text("Bob\n(Verifier)", font_size=22, color=VERIF_COLOR)
        bob_text.move_to(bob_circle)
        bob = VGroup(bob_circle, bob_text).to_edge(RIGHT, buff=2).shift(DOWN * 0.4)

        bob_role = Text(
            "Can query g at any point\nGoal: verify H efficiently",
            font_size=20, color=VERIF_COLOR
        )
        bob_role.next_to(bob, DOWN, buff=0.35)

        self.play(FadeIn(alice), FadeIn(bob), run_time=1)
        self.play(Write(alice_role), Write(bob_role), run_time=1.1)
        self.wait(0.8)

        # ── Message arrows ─────────────────────────────────────────────────
        a_to_b = Arrow(alice.get_right(), bob.get_left(), color=POLY_COLOR, buff=0.15)
        a_to_b.shift(UP * 0.35)
        msg_a = Text("polynomial  sᵢ(Xᵢ)", font_size=20, color=POLY_COLOR)
        msg_a.next_to(a_to_b, UP, buff=0.1)

        b_to_a = Arrow(bob.get_left(), alice.get_right(), color=FIELD_COLOR, buff=0.15)
        b_to_a.shift(DOWN * 0.35)
        msg_b = Text("random challenge  rᵢ", font_size=20, color=FIELD_COLOR)
        msg_b.next_to(b_to_a, DOWN, buff=0.1)

        self.play(Create(a_to_b), Write(msg_a), run_time=1)
        self.wait(0.4)
        self.play(Create(b_to_a), Write(msg_b), run_time=1)
        self.wait(0.8)

        # ── Rounds note ────────────────────────────────────────────────────
        rounds_note = Text(
            "This exchange repeats for v rounds — one per variable",
            font_size=26, color=ACCENT_COLOR
        )
        rounds_note.to_edge(DOWN, buff=0.9)
        self.play(Write(rounds_note))
        self.wait(2.5)

        self.play(FadeOut(VGroup(
            header, alice, bob, alice_role, bob_role,
            a_to_b, b_to_a, msg_a, msg_b, rounds_note
        )))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 5 — Finite Fields of Prime Order
# ══════════════════════════════════════════════════════════════════════════════

class PrimeFields(Scene):
    def construct(self):
        header = Text("Prerequisite: Finite Fields", font_size=40, color=FIELD_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        # ── Definition ─────────────────────────────────────────────────────
        defn = MathTex(
            r"\mathbb{F}_p = \{0,\,1,\,2,\,\ldots,\,p-1\}",
            r"\quad p \text{ prime}",
            font_size=38
        )
        defn.next_to(header, DOWN, buff=0.6)
        self.play(Write(defn), run_time=1.4)
        self.wait(0.5)

        ex = MathTex(
            r"\text{Example: } \mathbb{F}_7 = \{0,1,2,3,4,5,6\}",
            font_size=32, color=FIELD_COLOR
        )
        ex.next_to(defn, DOWN, buff=0.4)
        self.play(Write(ex), run_time=1)

        # ── Arithmetic wraps around ────────────────────────────────────────
        arith = VGroup(
            MathTex(r"5 + 4 \equiv 2 \pmod{7}", font_size=28),
            MathTex(r"3 \times 6 \equiv 4 \pmod{7}", font_size=28),
        ).arrange(RIGHT, buff=1.8)
        arith.next_to(ex, DOWN, buff=0.45)
        self.play(Write(arith), run_time=1)
        self.wait(0.8)

        # ── Key randomness property ────────────────────────────────────────
        rand_text = Text(
            "Key property:\n"
            "If  r ∈ 𝔽_p  is uniformly random, then\n"
            "r + a  and  r · a  (for any fixed a ≠ 0)\n"
            "are also uniformly random.",
            font_size=24, color=WHITE
        )
        rand_rect = SurroundingRectangle(rand_text, color=FIELD_COLOR, buff=0.25, corner_radius=0.12)
        rand_group = VGroup(rand_text, rand_rect)
        rand_group.next_to(arith, DOWN, buff=0.55)

        self.play(Create(rand_rect), Write(rand_text), run_time=1.5)
        self.wait(1.2)

        # ── Why it matters ─────────────────────────────────────────────────
        why = Text(
            "→ A cheating prover cannot predict the random challenge!\n"
            "   This is the engine of our soundness argument.",
            font_size=24, color=ACCENT_COLOR
        )
        why.to_edge(DOWN, buff=0.7)
        self.play(Write(why), run_time=1.4)
        self.wait(2.5)

        self.play(FadeOut(VGroup(header, defn, ex, arith, rand_group, why)))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 6 — Schwartz-Zippel Lemma
# ══════════════════════════════════════════════════════════════════════════════

class SchwartzZippel(Scene):
    def construct(self):
        header = Text("The Schwartz-Zippel Lemma", font_size=38, color=FIELD_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        # ── Statement ──────────────────────────────────────────────────────
        stmt1 = MathTex(
            r"\text{If } f \neq g \text{ are polynomials of total degree} \leq d\text{,}",
            font_size=28
        )
        stmt2 = MathTex(
            r"\Pr_{r \,\leftarrow\, \mathbb{F}}\!\bigl[f(r) = g(r)\bigr] \;\leq\; \frac{d}{|\mathbb{F}|}",
            font_size=38, color=POLY_COLOR
        )
        VGroup(stmt1, stmt2).arrange(DOWN, buff=0.4).next_to(header, DOWN, buff=0.55)

        self.play(Write(stmt1), run_time=1.2)
        self.play(Write(stmt2), run_time=1.4)
        self.wait(0.8)

        # ── Intuition ──────────────────────────────────────────────────────
        intuition = Text(
            "Intuition:  two distinct degree-d polynomials share\n"
            "at most  d  roots.  Most random points expose the difference.",
            font_size=26
        )
        intuition.next_to(stmt2, DOWN, buff=0.5)
        self.play(Write(intuition), run_time=1.3)
        self.wait(0.8)

        # ── Visual: two curves ─────────────────────────────────────────────
        ax = Axes(
            x_range=[-0.5, 5, 1], y_range=[-2, 5, 1],
            x_length=5.5, y_length=3.8, tips=False,
            axis_config={"color": DIM_COLOR, "stroke_width": 1.5}
        )
        ax.to_corner(DR, buff=0.6)

        f_graph = ax.plot(lambda x: 0.35 * (x - 1) * (x - 3.5) + 1.5,
                          x_range=[0, 4.8], color=PROVER_COLOR, stroke_width=3)
        g_graph = ax.plot(lambda x: 0.20 * (x - 2.2) ** 2 - 0.5,
                          x_range=[0, 4.8], color=VERIF_COLOR, stroke_width=3)

        fl = MathTex("f", font_size=26, color=PROVER_COLOR).next_to(ax.c2p(4.8, 1.5), RIGHT, buff=0.1)
        gl = MathTex("g", font_size=26, color=VERIF_COLOR).next_to(ax.c2p(4.8, 2.5), RIGHT, buff=0.1)

        self.play(Create(ax), run_time=0.8)
        self.play(Create(f_graph), Create(g_graph), run_time=1.5)
        self.play(Write(fl), Write(gl))

        # Mark approximate intersections
        for xval in [0.55, 3.9]:
            yval = 0.35 * (xval - 1) * (xval - 3.5) + 1.5
            dot = Dot(ax.c2p(xval, yval), color=GOOD_COLOR, radius=0.1)
            self.play(FadeIn(dot), run_time=0.4)

        agree = Text("agree ≤ d times", font_size=18, color=GOOD_COLOR)
        agree.next_to(ax, LEFT, buff=0.2).shift(UP * 0.2)
        self.play(Write(agree))
        self.wait(0.8)

        # ── Takeaway ───────────────────────────────────────────────────────
        takeaway = MathTex(
            r"\text{Random } r \text{ catches a lie with probability} \;\geq\; 1 - \frac{d}{|\mathbb{F}|}",
            font_size=28, color=ACCENT_COLOR
        )
        takeaway.to_edge(DOWN, buff=0.7)
        self.play(Write(takeaway), run_time=1.4)
        self.wait(2.5)

        self.play(FadeOut(VGroup(
            header, stmt1, stmt2, intuition,
            ax, f_graph, g_graph, fl, gl, agree, takeaway
        )))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 7 — Round 1
# ══════════════════════════════════════════════════════════════════════════════

class Round1(Scene):
    def construct(self):
        header = Text("Part 3 — The Protocol", font_size=38, color=ACCENT_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        round_lbl = Text("Round 1", font_size=32, color=POLY_COLOR, weight=BOLD)
        round_lbl.next_to(header, DOWN, buff=0.35)
        self.play(Write(round_lbl))

        g_def = MathTex(
            r"g(X_1,X_2,X_3)=2X_1^3+X_1 X_3+X_2 X_3",
            font_size=26, color=POLY_COLOR
        )
        g_def.next_to(round_lbl, DOWN, buff=0.35)
        self.play(Write(g_def), run_time=1)

        # ── Prover's polynomial ────────────────────────────────────────────
        p_lbl = Text("Prover sends:", font_size=26, color=PROVER_COLOR)
        s1_def = MathTex(
            r"s_1(X_1) = \!\!\sum_{x_2,\,x_3\,\in\,\{0,1\}}\!\! g(X_1,\,x_2,\,x_3)",
            font_size=28
        )
        s1_exp = MathTex(
            r"= g(X_1,0,0)+g(X_1,0,1)+g(X_1,1,0)+g(X_1,1,1)",
            font_size=24, color=DIM_COLOR
        )
        s1_exp.set_color(WHITE)
        s1_res = MathTex(
            r"s_1(X_1) = 8X_1^3 + 2X_1 + 1",
            font_size=32, color=POLY_COLOR
        )

        prover_group = VGroup(p_lbl, s1_def, s1_exp, s1_res)
        prover_group.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        prover_group.next_to(g_def, DOWN, buff=0.4)

        self.play(Write(p_lbl), run_time=0.6)
        self.play(Write(s1_def), run_time=1.1)
        self.play(Write(s1_exp), run_time=1)
        self.wait(0.3)
        self.play(Write(s1_res), run_time=0.9)
        self.wait(0.5)

        # ── Verifier check ─────────────────────────────────────────────────
        v_lbl   = Text("Verifier checks:", font_size=26, color=VERIF_COLOR)
        check   = MathTex(r"s_1(0)+s_1(1)\stackrel{?}{=}T", font_size=28)
        conc    = MathTex(r"1+11=12\ \checkmark", font_size=30, color=GOOD_COLOR)

        check_group = VGroup(v_lbl, check, conc).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        check_group.to_corner(DR, buff=0.9).shift(UP * 0.5)

        self.play(Write(v_lbl), run_time=0.6)
        self.play(Write(check), run_time=0.8)
        self.play(Write(conc),  run_time=0.7)
        self.wait(0.5)

        # ── Random challenge ───────────────────────────────────────────────
        r1_lbl = Text("Verifier samples random  r₁ ∈ 𝔽:", font_size=24, color=VERIF_COLOR)
        r1_val = MathTex(r"r_1 = 2", font_size=34, color=FIELD_COLOR)
        VGroup(r1_lbl, r1_val).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=1.4)

        self.play(Write(r1_lbl), Write(r1_val), run_time=1)

        # ── Why random? box ────────────────────────────────────────────────
        why_text = Text(
            "Why random?  A wrong polynomial agrees with the truth\n"
            "at most d times.  A random point exposes the lie\n"
            "with probability  ≥ 1 − d/|𝔽|.",
            font_size=21, color=ACCENT_COLOR
        )
        why_rect = SurroundingRectangle(why_text, color=ACCENT_COLOR, buff=0.2, corner_radius=0.1)
        why_box  = VGroup(why_text, why_rect)
        why_box.to_edge(DOWN, buff=0.25)

        self.play(FadeIn(why_box), run_time=1.1)
        self.wait(3)

        self.play(FadeOut(VGroup(
            header, round_lbl, g_def, prover_group,
            check_group, r1_lbl, r1_val, why_box
        )))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 8 — Round 2
# ══════════════════════════════════════════════════════════════════════════════

class Round2(Scene):
    def construct(self):
        header = Text("Round 2", font_size=38, color=POLY_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        # ── X1 is fixed ────────────────────────────────────────────────────
        fix = MathTex(
            r"X_1 \text{ is now fixed at } r_1 = 2",
            font_size=30, color=FIELD_COLOR
        )
        fix.next_to(header, DOWN, buff=0.45)
        self.play(Write(fix), run_time=1)

        # ── Shifted claim ──────────────────────────────────────────────────
        claim = MathTex(
            r"\sum_{x_2,\,x_3\,\in\,\{0,1\}} g(2,\,x_2,\,x_3) \;=\; s_1(2) \;=\; 69",
            font_size=28
        )
        claim.next_to(fix, DOWN, buff=0.4)
        self.play(Write(claim), run_time=1.2)
        self.wait(0.5)

        # ── Prover's polynomial ────────────────────────────────────────────
        p_lbl = Text("Prover sends:", font_size=26, color=PROVER_COLOR)
        s2_def = MathTex(
            r"s_2(X_2) = \sum_{x_3\,\in\,\{0,1\}} g(2,\,X_2,\,x_3)",
            font_size=28
        )
        s2_exp1 = MathTex(
            r"= g(2,X_2,0) + g(2,X_2,1)",
            font_size=26
        )
        s2_exp2 = MathTex(
            r"= 16 + (18+X_2) = 34+X_2",
            font_size=26
        )
        s2_res = MathTex(
            r"s_2(X_2)=34+X_2",
            font_size=32, color=POLY_COLOR
        )

        prover_group = VGroup(p_lbl, s2_def, s2_exp1, s2_exp2, s2_res)
        prover_group.arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        prover_group.next_to(claim, DOWN, buff=0.4)

        self.play(Write(p_lbl), run_time=0.6)
        self.play(Write(s2_def), run_time=1)
        self.play(Write(s2_exp1), run_time=0.9)
        self.play(Write(s2_exp2), run_time=0.9)
        self.play(Write(s2_res),  run_time=0.8)
        self.wait(0.5)

        # ── Verifier check ─────────────────────────────────────────────────
        v_lbl = Text("Verifier checks:", font_size=26, color=VERIF_COLOR)
        check = MathTex(
            r"s_2(0)+s_2(1)\stackrel{?}{=}s_1(r_1)=s_1(2)",
            font_size=28
        )
        conc  = MathTex(
            r"34+35=69=s_1(2)\ \checkmark",
            font_size=28, color=GOOD_COLOR
        )
        check_group = VGroup(v_lbl, check, conc).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        check_group.to_corner(DR, buff=0.9).shift(UP * 0.3)

        self.play(Write(v_lbl), Write(check), run_time=1)
        self.play(Write(conc), run_time=0.8)
        self.wait(0.5)

        # ── New random challenge ───────────────────────────────────────────
        r2 = MathTex(
            r"r_2 = 3 \;\text{(sampled at random)}",
            font_size=28, color=FIELD_COLOR
        )
        r2.to_edge(DOWN, buff=0.9)
        self.play(Write(r2), run_time=0.9)
        self.wait(2)

        self.play(FadeOut(VGroup(header, fix, claim, prover_group, check_group, r2)))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 9 — General Rounds & Chain Metaphor
# ══════════════════════════════════════════════════════════════════════════════

class GeneralRounds(Scene):
    def construct(self):
        header = Text("Rounds 3 to v−1", font_size=38, color=ACCENT_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        # ── General formula ────────────────────────────────────────────────
        gen = MathTex(
            r"s_i(X_i)=\!\!\!\sum_{x_{i+1},\ldots,x_v\in\{0,1\}}\!\!\! g(r_1,\ldots,r_{i-1},X_i,x_{i+1},\ldots,x_v)",
            font_size=24
        )
        gen.next_to(header, DOWN, buff=0.5)
        self.play(Write(gen), run_time=1.5)

        check_i = MathTex(
            r"\text{Verifier checks: }\; s_i(0)+s_i(1) \;=\; s_{i-1}(r_{i-1})",
            font_size=28, color=VERIF_COLOR
        )
        check_i.next_to(gen, DOWN, buff=0.4)
        self.play(Write(check_i), run_time=1)
        self.wait(0.6)

        # ── Chain metaphor ─────────────────────────────────────────────────
        chain_lbl = Text("Think of every round as a link in a chain:", font_size=26)
        chain_lbl.next_to(check_i, DOWN, buff=0.5)
        self.play(Write(chain_lbl))
        self.wait(0.3)

        chain, labels = self._make_chain(7)
        chain.next_to(chain_lbl, DOWN, buff=0.45)
        labels_group = VGroup(*[
            Text(f"Round {i+1}", font_size=15, color=LINK_COLOR).next_to(chain[i], DOWN, buff=0.18)
            for i in range(7)
        ])

        self.play(LaggedStart(*[Create(c) for c in chain], lag_ratio=0.15), run_time=1.8)
        self.play(Write(labels_group), run_time=0.8)
        self.wait(0.5)

        # ── Break one link ─────────────────────────────────────────────────
        broken = Text("If any link breaks → entire chain fails", font_size=26, color=BAD_COLOR)
        broken.to_edge(DOWN, buff=1.1)
        self.play(Write(broken))

        self.play(chain[3].animate.set_color(BAD_COLOR).set_stroke(width=5), run_time=0.6)
        cross = Cross(chain[3], color=BAD_COLOR, stroke_width=3)
        self.play(Create(cross), run_time=0.5)
        self.wait(1.5)

        # ── Communication cost ─────────────────────────────────────────────
        comm = MathTex(
            r"\text{Communication per round: }\deg_i(g)+1\text{ field elements}",
            font_size=24
        )
        total = MathTex(
            r"\text{Total cost: }O(v\cdot d)\text{ — exponentially less than }2^v!",
            font_size=26, color=ACCENT_COLOR
        )
        VGroup(comm, total).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.25)

        self.play(FadeOut(broken))
        self.play(Write(comm), Write(total), run_time=1.2)
        self.wait(2.5)

        self.play(FadeOut(VGroup(
            header, gen, check_i, chain_lbl, chain, labels_group, cross, comm, total
        )))

    def _make_chain(self, n):
        links = VGroup()
        for i in range(n):
            ellipse = Ellipse(width=1.0, height=0.52, color=LINK_COLOR, stroke_width=3)
            if i > 0:
                ellipse.next_to(links[-1], RIGHT, buff=-0.16)
            links.add(ellipse)
        return links, VGroup()


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 10 — Final Round & Oracle Query
# ══════════════════════════════════════════════════════════════════════════════

class FinalRound(Scene):
    def construct(self):
        header = Text("Final Round — The Oracle Query", font_size=36, color=ACCENT_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        # ── sᵥ definition ──────────────────────────────────────────────────
        sv_def = MathTex(
            r"s_v(X_v) \;=\; g(r_1,\,r_2,\,\ldots,\,r_{v-1},\,X_v)",
            font_size=32, color=POLY_COLOR
        )
        sv_def.next_to(header, DOWN, buff=0.5)
        self.play(Write(sv_def), run_time=1)

        check_v = MathTex(
            r"s_v(0)+s_v(1)\stackrel{?}{=}s_{v-1}(r_{v-1})",
            font_size=28, color=VERIF_COLOR
        )
        check_v.next_to(sv_def, DOWN, buff=0.4)
        self.play(Write(check_v), run_time=1)
        self.wait(0.5)

        # ── Oracle query ───────────────────────────────────────────────────
        oracle_lbl = Text(
            "Now — the ONLY time the Verifier queries g directly:",
            font_size=26, color=WHITE
        )
        oracle_lbl.next_to(check_v, DOWN, buff=0.5)
        self.play(Write(oracle_lbl))

        oracle = MathTex(
            r"\text{Compute: }g(r_1,\,r_2,\,\ldots,\,r_v)",
            font_size=30, color=FIELD_COLOR
        )
        oracle.next_to(oracle_lbl, DOWN, buff=0.3)
        oracle_box = SurroundingRectangle(oracle, color=FIELD_COLOR, buff=0.22, corner_radius=0.1)
        self.play(Write(oracle), Create(oracle_box), run_time=1.1)
        self.wait(0.5)

        # ── Final check ────────────────────────────────────────────────────
        final_check = MathTex(
            r"g(r_1,\ldots,r_v)\stackrel{?}{=}s_v(r_v)",
            font_size=32, color=VERIF_COLOR
        )
        final_check.next_to(oracle, DOWN, buff=0.45)
        self.play(Write(final_check), run_time=1)

        accept = Text("✓  ACCEPT", font_size=42, color=GOOD_COLOR, weight=BOLD)
        accept.next_to(final_check, DOWN, buff=0.35)
        self.play(Write(accept), run_time=0.8)
        self.wait(0.8)

        # ── Concrete example ───────────────────────────────────────────────
        conc_lbl = Text("Concrete (our example):", font_size=24, color=DIM_COLOR)
        conc_lbl.set_color(WHITE)
        conc_r   = MathTex(r"r_1=2,\ r_2=3,\ r_3=6", font_size=26)
        # g(2,3,6) = 2*8 + 2*6 + 3*6 = 16 + 12 + 18 = 46
        conc_g   = MathTex(
            r"g(2,3,6)=2(8)+2(6)+3(6)=16+12+18=46",
            font_size=26, color=POLY_COLOR
        )
        # s3(X3) = g(2,3,X3) = 16+5X3 => s3(6)=46
        conc_s3  = MathTex(
            r"s_3(X_3)=16+5X_3 \;\Rightarrow\; s_3(6)=46\ \checkmark",
            font_size=26, color=GOOD_COLOR
        )
        conc_group = VGroup(conc_lbl, conc_r, conc_g, conc_s3)
        conc_group.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        conc_group.to_corner(DR, buff=0.6).shift(UP * 0.2)

        self.play(Write(conc_lbl), run_time=0.5)
        self.play(Write(conc_r), Write(conc_g), run_time=1)
        self.play(Write(conc_s3), run_time=0.8)
        self.wait(2.5)

        self.play(FadeOut(VGroup(
            header, sv_def, check_v, oracle_lbl, oracle, oracle_box,
            final_check, accept, conc_group
        )))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 11 — Soundness Analysis
# ══════════════════════════════════════════════════════════════════════════════

class SoundnessAnalysis(Scene):
    def construct(self):
        header = Text("Part 4 — Why It Works", font_size=38, color=ACCENT_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        # ── Completeness ───────────────────────────────────────────────────
        comp_title = Text("Completeness", font_size=28, color=GOOD_COLOR, weight=BOLD)
        comp_body  = Text(
            "Honest prover always sends the true sᵢ.\n"
            "Every check passes with probability 1.",
            font_size=22
        )
        comp_box_content = VGroup(comp_title, comp_body).arrange(DOWN, buff=0.22)
        comp_rect = SurroundingRectangle(comp_box_content, color=GOOD_COLOR, buff=0.28)
        comp = VGroup(comp_box_content, comp_rect)
        comp.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        # ── Soundness ──────────────────────────────────────────────────────
        snd_title = Text("Soundness", font_size=28, color=BAD_COLOR, weight=BOLD)
        snd_body  = Text(
            "Cheating prover must send at least\n"
            "one wrong polynomial sᵢ ≠ true gᵢ.",
            font_size=22
        )
        snd_box_content = VGroup(snd_title, snd_body).arrange(DOWN, buff=0.22)
        snd_rect = SurroundingRectangle(snd_box_content, color=BAD_COLOR, buff=0.28)
        snd = VGroup(snd_box_content, snd_rect)
        snd.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.3)

        self.play(FadeIn(comp), FadeIn(snd), run_time=1.2)
        self.wait(1.5)

        # ── Dim completeness, focus on soundness ───────────────────────────
        self.play(
            comp.animate.set_opacity(0.35),
            snd.animate.move_to(ORIGIN).shift(UP * 1.2)
        )
        self.wait(0.4)

        # ── Per-round Schwartz-Zippel ──────────────────────────────────────
        sz = MathTex(
            r"\Pr[\text{round }i\text{ catches the lie}]\;\geq\;1-\frac{d}{|\mathbb{F}|}",
            font_size=28, color=VERIF_COLOR
        )
        sz.next_to(snd, DOWN, buff=0.5)
        self.play(Write(sz), run_time=1.2)
        self.wait(0.5)

        # ── Union bound ────────────────────────────────────────────────────
        union_lbl = Text("Union Bound over all v rounds:", font_size=26)
        union_lbl.next_to(sz, DOWN, buff=0.45)
        union = MathTex(
            r"\delta_s \;\leq\; \frac{vd}{|\mathbb{F}|}",
            font_size=44, color=BAD_COLOR
        )
        union.next_to(union_lbl, DOWN, buff=0.3)
        union_rect = SurroundingRectangle(union, color=BAD_COLOR, buff=0.3, corner_radius=0.12)

        self.play(Write(union_lbl), run_time=0.8)
        self.play(Write(union), Create(union_rect), run_time=1.2)
        self.wait(0.8)

        # ── Making error small ─────────────────────────────────────────────
        small = Text(
            "Choose  |𝔽| >> vd  →  soundness error becomes negligible.",
            font_size=26, color=GOOD_COLOR
        )
        small.to_edge(DOWN, buff=0.8)
        self.play(Write(small), run_time=1.2)
        self.wait(2.5)

        self.play(FadeOut(VGroup(
            header, comp, snd, sz, union_lbl, union, union_rect, small
        )))


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 12 — Summary & Conclusion
# ══════════════════════════════════════════════════════════════════════════════

class Conclusion(Scene):
    def construct(self):
        header = Text("Summary", font_size=44, color=POLY_COLOR, weight=BOLD)
        self.play(Write(header))
        self.play(header.animate.to_edge(UP))

        bullets = [
            ("①", "Sum-Check reduces a global sum to v local polynomial checks."),
            ("②", "Each round pins one variable with a random challenge."),
            ("③", "Schwartz-Zippel + Union Bound → soundness error  δₛ ≤ vd/|𝔽|."),
            ("④", "Cost:  O(vd)  field elements — vs  2ᵛ  naïve evaluations."),
            ("⑤", "Applications: GKR protocol, IP = PSPACE, verifiable computation."),
        ]
        colors = [POLY_COLOR, FIELD_COLOR, VERIF_COLOR, GOOD_COLOR, ACCENT_COLOR]

        point_group = VGroup()
        for (num, txt), col in zip(bullets, colors):
            row = VGroup(
                Text(num, font_size=26, color=col),
                Text(txt, font_size=24),
            ).arrange(RIGHT, buff=0.3)
            point_group.add(row)
        point_group.arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        point_group.next_to(header, DOWN, buff=0.55)

        for row in point_group:
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.55)
            self.wait(0.2)
        self.wait(1.5)

        # ── Final equation ─────────────────────────────────────────────────
        final = MathTex(
            r"\underbrace{2^v\text{ eval.}}_{\text{naïve}}"
            r"\;\xrightarrow{\text{Sum-Check}}\;"
            r"\underbrace{O(vd)\text{ messages}}_{\text{interactive proof}}",
            font_size=30, color=ACCENT_COLOR
        )
        final.to_edge(DOWN, buff=0.9)
        self.play(Write(final), run_time=1.5)
        self.wait(3)

        self.play(FadeOut(VGroup(header, point_group, final)))

        end = Text("Thanks for watching!", font_size=50, weight=BOLD)
        self.play(Write(end), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(end))
