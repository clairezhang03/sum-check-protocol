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
config.background_color = BLACK

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



class IntroSumCheck(Scene):
    def construct(self):
        polynomial = MathTex(
        r'g(X_1,X_2,X_3) = 2X_1^3 + X_1 X_3 + X_2 X_3',
        font_size=48,
        tex_to_color_map={
            r"X_1": RED,
            r"X_2": GREEN,
            r"X_3": BLUE,
        }
        )
        self.add(polynomial)

        self.play(Write(polynomial), run_time=3)
        self.wait(1)

        free_vars = polynomial[0][1:11].copy()  # X_1, X_2, X_3
        self.play(free_vars.animate.scale(0.7).to_corner(UL, buff=0.5), run_time=1.5)

        vars_domain = MathTex(
            r'\in \{0,1\}^3',
            font_size=36,
            color=WHITE
        )

        vars_domain.next_to(free_vars, RIGHT, buff=0.2)
        self.play(Write(vars_domain), run_time=1.5)
        self.wait(1.5)

        self.play(polynomial.animate.to_edge(UP, buff=1.5), run_time=1.5)


        summation_formula = MathTex(
            r"\sum_{\scriptscriptstyle X_1, X_2, X_3} g(X_1, X_2, X_3) = ",
            r"\ T",
            font_size=36,
            color=WHITE
        )
        summation_formula[1].set_color(ORANGE)
        summation_formula[1].scale(1.4)
        # shift the whole formula so the = sign is at x=0
        eq_sign = summation_formula[0][-2]  # last character of [0] is the =
        summation_formula.shift(LEFT * eq_sign.get_center()[0])

        self.play(Write(summation_formula[0][0:-1]), run_time=2.5)
        self.wait(1.5)
        self.play(Write(summation_formula[0][-1:]), Write(summation_formula[1]), run_time=1.5)
        self.wait(2.5)

        question_mark = MathTex(r"\stackrel{?}{=}", font_size=36, color=BAD_COLOR)
        question_mark.move_to(summation_formula[0][-1])  # on top of the =
        question_mark.shift(UP * 0.1)  # nudge up a bit
        self.play(Transform(summation_formula[0][-1], question_mark), run_time=1.2)
        self.wait(2.5)

        poly_copy = polynomial.copy()

        points = VGroup(
            MathTex(r"g(0,0,0) = 0", font_size=36, color=POLY_COLOR),
            MathTex(r"g(0,0,1) = 0", font_size=36, color=POLY_COLOR),
            MathTex(r"\vdots",        font_size=36, color=POLY_COLOR),
            MathTex(r"g(1,1,1) = 3", font_size=36, color=POLY_COLOR),
        ).arrange(DOWN, buff=0.3)

        points.next_to(question_mark, LEFT, buff=0.4)
        self.play(FadeOut(summation_formula[0][:-1]),ReplacementTransform(poly_copy, points), run_time=1.2)
        self.wait(1.5)

        correct_answer = 12
        
        answer = MathTex(rf"{correct_answer}", font_size=36, color=POLY_COLOR)
        answer.scale(1.4)
        answer.next_to(question_mark, LEFT, buff=0.3)
        answer.shift(DOWN * 0.06)

        self.play(ReplacementTransform(points, answer), run_time=1.5)
        self.pause(4)
        self.play(FadeOut(*self.mobjects), run_time=1.5)

# Motivation that with larger number of variables and variable settings, the number of calculations explodes
class BiggerPolynomial(Scene):
    def construct(self):
        header = Text("What if there were more variables?", font_size=36, color=WHITE, weight=BOLD)
        self.play(Write(header))
        self.wait(1.5)
        self.play(header.animate.to_edge(UP))
        self.wait(0.5)
        big_poly = MathTex(
            r"\sum_{x_1\ldots\ x_{20}\,\in\,\{0,1\}}\!\! g(x_1,\,x_2,\,\ldots,\,x_{20})=\ ",
            r"T",
            font_size=42, color=POLY_COLOR
        )
        big_poly[1].set_color(ORANGE)
        big_poly[1].scale(1.2)
        self.play(Write(big_poly[0][:-1:]), run_time=2)
        self.wait(3.5)
        self.play(Write(big_poly[0][-1:]), Write(big_poly[1]), run_time=1.5)
        self.wait(4)

        explosion = MathTex(
            r"\text{Number of possible } (x_1,\ldots,x_{20}) = 2^{20} > 1\text{ million!}",
            font_size=28, color=BAD_COLOR
        )
        explosion.next_to(big_poly, DOWN, buff=0.4)

        self.play(Write(explosion), run_time=1.5)
        self.wait(2.5)

        general_poly = MathTex(
            r"\sum_{x_1\ldots x_n}\!\! g(x_1,\,x_2,\,\ldots,\,x_n)",
            font_size=42, color=POLY_COLOR
        )

        general_poly.move_to(big_poly[0])

        self.play(
            FadeOut(VGroup(header, explosion,big_poly)),
            run_time=0.5
        )
        self.wait(0.5)
        self.play(Write(general_poly), run_time=2)

        self.play(general_poly.animate.shift(DOWN * 0.3), run_time=1)

        self.wait(0.5)
        var_copy = general_poly[0][9:23].copy()  # x_1 ... x_n

        self.play(var_copy.animate.shift(UP * 1).shift(LEFT * 1.6), run_time=1)

        domain = MathTex(r"\in \{0,\ldots, k-1\}^n", font_size=36, color=WHITE)
        domain.next_to(var_copy, RIGHT, buff=0.3)
        self.play(Write(domain), run_time=1.2)
        self.wait(2.5)

        num_possibilities = MathTex(r"\text{Number of evaluations} = k^n", font_size=48, color=RED)
        num_possibilities.to_edge(UP, buff=1)
        self.play(Write(num_possibilities), run_time=2)
        self.wait(0.5)
        self.play(FadeOut(*self.mobjects), run_time=1)

class MotivationCheck(Scene):
    def construct(self):
        self.wait(5)

        header = Text("How can I efficiently prove to YOU that the sum is correct?", font_size=36, color=WHITE)
        header[6].set_color(VERIF_COLOR)
        header[25:28].set_color(PROVER_COLOR)
        self.play(Write(header), run_time=4.5)
        self.wait(7.5)

        self.play(header.animate.to_edge(UP, buff=0.8), run_time=1.5)

        self.wait(1)

        prover = header[6].copy()
        verifier = header[25:28].copy()

        self.play(
            prover.animate.scale(1.4).to_edge(LEFT, buff=1.5).shift(DOWN * 3),      
            verifier.animate.scale(1.4).to_edge(RIGHT, buff=1.5).shift(DOWN * 3),
            run_time=1.5
        )

        self.wait(4)

        # draw arrow from prover to verifier
        arrow_pv = CurvedArrow(
            start_point=prover.get_right(),
            end_point=verifier.get_left(),
            color=YELLOW,
            angle=-TAU/6
        )

        arrow_vp = CurvedArrow(
            start_point=verifier.get_left(),
            end_point=prover.get_right(),
            color=BLUE,
            angle=-TAU/6
        )

        label_pv = Text("Msg", font_size=24, color=YELLOW)
        label_pv.next_to(arrow_pv, UP, buff=0.15)

        label_vp = Text("Response", font_size=24, color=BLUE)
        label_vp.next_to(arrow_vp, DOWN, buff=0.15)

        self.play(Create(arrow_pv), FadeIn(label_pv), run_time=1.0)
        self.wait(1)
        self.play(Create(arrow_vp), FadeIn(label_vp), run_time=1.0)
        self.wait(2.5)

        self.play(
            FadeOut(arrow_pv),
            FadeOut(arrow_vp),
            FadeOut(label_pv),
            FadeOut(label_vp),
            FadeOut(prover),
            verifier.animate.move_to(ORIGIN).shift(UP * 0.3),
            run_time=1.2
        )

        self.wait(1.5)

        random = MathTex(r"r \overset{\$}{\longleftarrow} \{0,1\}^n", font_size=42, color=FIELD_COLOR)
        random.next_to(verifier, DOWN, buff=0.4)
        self.play(Write(random), run_time=1.5)
        self.wait(2.5)
        self.play(FadeOut(VGroup(verifier,random)),header.animate.move_to(ORIGIN).shift(DOWN * 0.2), run_time=1.5)
        self.wait(2)

        checkMark = MathTex(r"\checkmark", font_size=64, color=GREEN)
        checkMark.next_to(header, UP, buff=0.2)

        self.play(Write(checkMark), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(*self.mobjects), run_time=1.5)
        

        self.wait(5)

class FieldDefinition(Scene):
    def construct(self):
        self.wait(8)
        header = Text("Fields")
        header.to_edge(UP, buff=0.8)
        self.play(Write(header), run_time=1.5)

        self.wait(1.5)

        define_q = Tex("Consider some large prime number $q > T$", font_size=36, color=WHITE)
        define_q.next_to(header, DOWN, buff=0.5)
        define_q[0][-1].set_color(ORANGE)  # T
        define_q[0][-3].set_color(FIELD_COLOR)  # q

        self.play(Write(define_q), run_time=2.5)
        self.wait(2)

        field = MathTex(r"\mathbb{F}_q = \{0, 1, 2, \ldots, q-1\}", font_size=48, color=FIELD_COLOR)
        self.play(Write(field), run_time=1.5)
        self.wait(4.5)

        self.play(field.animate.shift(UP * 0.8), run_time=1.2)
        self.wait(3)

        fieldProperty = MathTex(
            r"\forall\, a, b \in \mathbb{F}_q:",
            font_size=48, color=WHITE
        )
        fieldProperty.next_to(field, DOWN, buff=0.8)
        fieldProperty[0][-3:-1:].set_color(FIELD_COLOR)  # F_q
        self.play(Write(fieldProperty), run_time=1.5)
        self.wait(1.5)

        addition = MathTex(r"(a + b) \mod\ q \in \mathbb{F}_q", font_size=42, color=WHITE)
        addition[0][-2::].set_color(FIELD_COLOR)  # mod q)
        multiplication = MathTex(r"(a \cdot b) \mod\ q \in \mathbb{F}_q", font_size=42, color=WHITE)
        multiplication[0][-2::].set_color(FIELD_COLOR)  # mod q)
        ops = VGroup(addition, multiplication).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ops.next_to(fieldProperty, DOWN, buff=0.3)
        self.play(Write(addition), run_time=1.5)
        self.wait(1)
        self.play(Write(multiplication), run_time=1.5)
        self.wait(12)
        self.play(FadeOut(*self.mobjects), run_time=1.5)
        self.wait(5)


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 6 — Schwartz-Zippel Lemma
# ══════════════════════════════════════════════════════════════════════════════

class SchwartzZippel(Scene):
    def construct(self):
        self.wait(5)
        header = Text("The Schwartz-Zippel Lemma", font_size=48, color=WHITE, weight=BOLD)
        self.play(Write(header))
        self.pause(1)
        self.play(header.animate.to_edge(UP))
        

        # ── Statement ──────────────────────────────────────────────────────
        stmt1 = MathTex(
            r"\text{If } f \neq g \text{ are polynomials over finite field } \mathbb{F} \text{ of maximum total degree} \leq d\text{,}",
            font_size=38
        )
        stmt2 = MathTex(
            r"\Pr_{r\leftarrow \mathbb{F}}\ \bigl[f(r) = g(r)\bigr] \;\leq\; \frac{d}{|\mathbb{F}|}",
            font_size=38, color=POLY_COLOR
        )
        VGroup(stmt1, stmt2).arrange(DOWN, buff=0.4)

        self.play(Write(stmt1), run_time=4.5)
        self.pause(1.5)

        self.play(Write(stmt2), run_time=2.5)
        self.wait(5.5)

        self.play(FadeOut(*self.mobjects), run_time=1.5)

        self.wait(2)

        f_poly = MathTex(r"f(X) =  X^2 - 6X + 10", font_size=36, color=PROVER_COLOR)
        g_poly = MathTex(r"g(X) = -X + 6", font_size=36, color=VERIF_COLOR)
        f_poly.to_edge(UL)
        f_poly.shift(DOWN * 0.2)
        g_poly.to_edge(UL)
        g_poly.shift(DOWN * 0.7)
        self.play(Write(f_poly), Write(g_poly), run_time=1.5)
        self.pause(2)

        graph = Axes(
            x_range=[0, 6, 1], y_range=[0, 6, 1], x_length=5, y_length=4, tips=False,
        )

        f_graph = graph.plot(lambda x: x ** 2 - 6 * x + 10, x_range=[3 - 5**0.5, 3 + 5**0.5], color=PROVER_COLOR, stroke_width=3)
        g_graph = graph.plot(lambda x: -x + 6, x_range=[0, 6], color=VERIF_COLOR, stroke_width=3)
        self.play(Create(graph),run_time=2.5)
        self.play(Create(f_graph), Create(g_graph), run_time=1)
        self.wait(1)

        # highlight intersection points
        intersections = [
            graph.coords_to_point(1, -1 + 6),   # (1, 5)
            graph.coords_to_point(4, -4 + 6),   # (4, 2)
        ]

        dots = VGroup(*[
            Dot(point, color=YELLOW, radius=0.1) for point in intersections
        ])

        self.play(Create(dots), run_time=1.5)
        self.wait(2)

        shift_val = 2
        self.play(graph.animate.shift(LEFT * shift_val), f_graph.animate.shift(LEFT * shift_val), g_graph.animate.shift(LEFT * shift_val), dots.animate.shift(LEFT * shift_val), run_time=1.2)

        graph_domain = MathTex(r"X \overset{\$}{\leftarrow} [0,1,2,3,4,5,6]", font_size=56, color=WHITE)
        graph_domain.next_to(graph, RIGHT, buff=0.5)
        self.play(Write(graph_domain), run_time=2.5)


        self.wait(2)


        vertical_line = Line(
            start=graph.coords_to_point(0,-0.5),
            end=graph.coords_to_point(0,6.5),
            color=YELLOW, stroke_width=4
        )

        self.play(Create(vertical_line), run_time=1.5)
        self.wait(1.5)

        new_line = Line(
            start = graph.coords_to_point(6, -0.5),
            end = graph.coords_to_point(6, 6.5),
            color=YELLOW, stroke_width=4
        )

        self.play(ReplacementTransform(vertical_line, new_line), Indicate(graph_domain[0][-2], color=YELLOW, scale_factor=1.2), run_time=2)
        self.wait(1)

        last_line = Line(
            start = graph.coords_to_point(1, -0.5),
            end = graph.coords_to_point(1, 6.5),
            color=YELLOW, stroke_width=4
        )

        self.play(ReplacementTransform(new_line, last_line), Indicate(graph_domain[0][6], color=YELLOW, scale_factor=1.2), run_time=2)
        self.wait(10)

        self.play(FadeOut(*self.mobjects), run_time=1.5)
        self.wait(4.7)



class SumCheckSetup(Scene):
    def construct(self):
        self.wait(5)
        protocol_header = Text("The Protocol", font_size=40, color=WHITE, weight=BOLD)
        self.play(Write(protocol_header), run_time=2.5)
        self.play(FadeOut(protocol_header), run_time=1.5)

        alice = Circle(radius=0.75, color=PROVER_COLOR, fill_opacity=0.2)
        alice_text = Text("Alice", font_size=22, color=PROVER_COLOR)
        alice_text.move_to(alice)

        bob = Circle(radius=0.75, color=VERIF_COLOR, fill_opacity=0.2)
        bob_text = Text("Bob", font_size=22, color=VERIF_COLOR)
        bob_text.move_to(bob)

        alice_group = VGroup(alice, alice_text).to_edge(LEFT, buff=2).shift(DOWN * 0.4)
        bob_group = VGroup(bob, bob_text).to_edge(RIGHT, buff=2).shift(DOWN * 0.4)

        self.play(FadeIn(alice_group), FadeIn(bob_group), run_time=2)
        self.wait(3)

        polynomial = MathTex(
            r"g(X_1\ldots\ X_n)",font_size=48
        )

        polynomial.to_edge(UP,buff=1)
        self.play(Write(polynomial), run_time=2)
        self.wait(1)

        domain =  polynomial[0][1:10].copy()
        self.play(domain.animate.shift(DOWN * 0.6).shift(LEFT * 1).scale(0.8), run_time=1.5)
        domain_text = MathTex(r"\in \{0,1\}^n", font_size=38, color=WHITE)
        domain_text.next_to(domain, RIGHT, buff=0.3)
        self.play(Write(domain_text), run_time=1.5)
        self.wait(3)

        # speech bubble above alice
        claim = MathTex(
            r"\sum_{X_1\ldots,X_n} g(X_1\ldots X_n) = T",
            font_size=24, color=WHITE
        )

        bubble = RoundedRectangle(
            corner_radius=0.2,
            width=claim.width + 0.6,
            height=claim.height + 0.5,
            color=PROVER_COLOR,
            fill_color=PROVER_COLOR,
            fill_opacity=0.15
        )
        bubble.next_to(alice_group, UP, buff=0.4)
        claim.move_to(bubble)

        # tail pointing down to alice
        tail = Triangle(
            color=PROVER_COLOR,
            fill_color=PROVER_COLOR,
            fill_opacity=0.15,
            stroke_width=0
        )
        tail.scale(0.12).next_to(bubble, DOWN, buff=-0.05)

        self.play(FadeIn(bubble), FadeIn(tail), Write(claim), run_time=2.5)
        self.wait(3)
        
        self.play(FadeOut(polynomial, domain, domain_text), run_time=1)
        example = MathTex(
            r'g(X_1,X_2,X_3) = 2X_1^3 + X_1 X_3 + X_2 X_3',
            font_size=48, color=POLY_COLOR
        )

        example.move_to(polynomial)
        self.play(Write(example), run_time=2)
        self.wait(3)

        example_claim = MathTex(r"\sum_{X_1\ldots,X_3} g(X_1\ldots X_3) = 12", font_size=24, color=WHITE)
        example_claim[0][-2::].set_color(ORANGE)  # H = 12

        example_claim.move_to(claim)
        self.play(ReplacementTransform(claim, example_claim), run_time=1.5)
        self.wait(2)

        alice_first_msg = Tex("Prime $q >> T$", font_size=28, color=PROVER_COLOR)
        alice_first_msg.move_to(alice_group)  # start at alice

        arrow = CurvedArrow(
            start_point=alice_group.get_right(),
            end_point=bob_group.get_left(),
            color=PROVER_COLOR,
            angle=-TAU/6
        )
        alice_first_msg.next_to(arrow, UP, buff=0.15)
        self.play(Create(arrow), run_time=0.8)

        self.play(
            Write(alice_first_msg),
            run_time=1.2
        )




        self.wait(4)
        


        # Second video
        self.play(alice_group.animate.move_to(ORIGIN).to_edge(UP, buff=0.5), *[FadeOut(mob) for mob in self.mobjects if mob != alice_group], run_time=1.5)
        self.wait(1.5)

        sum_x1 = MathTex(r"S_1(X_1) = \sum_{X_2\ldots X_n} g(X_1, X_2\ldots X_n)", font_size=48, color=POLY_COLOR)
        sum_x1.next_to(alice_group, DOWN, buff=0.6)
        self.play(Write(sum_x1), run_time=3)
        self.wait(6)

        self.play(sum_x1.animate.to_edge(UP,buff=0.8).to_edge(LEFT,buff=0.1).scale(0.6), run_time=1.5)
        example.next_to(alice_group,DOWN,buff=0.6)

        self.play(Write(example), run_time=1.5)
        self.pause(1)

        g_1_summation = MathTex(
            r"g(X_1,0,0) + g(X_1,0,1) + g(X_1,1,0) + g(X_1,1,1)",
            font_size=48, color=POLY_COLOR
        )

        g_1_summation.next_to(example, DOWN, buff=0.6)
        self.play(Write(g_1_summation), run_time=2.5)
        self.wait(1.5)

        g1_new = MathTex(
            r"S_1(X_1) = 8X_1^3 + 2X_1 + 1",
            font_size=48, color=POLY_COLOR
        )
        g1_new.next_to(g_1_summation, DOWN, buff=0.6)
        self.play(Write(g1_new), run_time=3)
        self.wait(2)

        # position bob off screen right at the same vertical position as alice
        bob_group.move_to(alice_group.get_center())
        bob_group.shift(RIGHT * 15)
        self.add(bob_group)

        # swipe all current objects left, bob slides in simultaneously
        self.play(
            *[mob.animate.shift(LEFT * 15) for mob in self.mobjects if mob != bob_group],
            bob_group.animate.shift(LEFT * 15),
            run_time=1.5
        )

        # clean up everything that slid off screen
        for mob in self.mobjects:
            if mob.get_center()[0] < -14:  # arbitrary threshold for "off screen left"
                self.remove(mob)
        self.add(bob_group)
        self.wait(1)
        
        bob_s1 = MathTex(r"S_1(X_1)", font_size=48, color=POLY_COLOR)
        bob_s1.next_to(bob_group, DOWN, buff=0.6)
        bob_s1.shift(LEFT * 14)
        self.play(bob_s1.animate.shift(RIGHT * 14), run_time=2)
        self.wait(1)

        sum_s1_bob = MathTex(r"\sum_{X_1 \in \{0,1\}}", font_size=36, color=POLY_COLOR)
        self.play(bob_s1.animate.shift(RIGHT * 0.4), run_time=1)
        sum_s1_bob.next_to(bob_s1, LEFT)
        self.play(Write(sum_s1_bob), run_time=2)
        self.wait(2.5)

        x1_s1_bob = MathTex(r"S_1(0) + S_1(1) \stackrel{?}{=} T", font_size=48, color=POLY_COLOR)
        x1_s1_bob.next_to(sum_s1_bob, DOWN, buff=0.4)
        x1_s1_bob.shift(RIGHT * 1)
        self.play(Write(x1_s1_bob), run_time=3)
        self.wait(3)

        s1_b1_transform = MathTex(r"\sum_{X_2\ldots X_n} g(X_1, X_2\ldots X_n)", font_size=36, color=POLY_COLOR)
        s1_b1_transform.move_to(bob_s1)
        self.play(ReplacementTransform(bob_s1, s1_b1_transform), sum_s1_bob.animate.next_to(s1_b1_transform, LEFT), run_time=3)
        self.wait(5)

        exampleS1 = MathTex(
            r"S_1(X_1) = 8X_1^3 + 2X_1 + 1",
            font_size=48, color=POLY_COLOR
        )
        exampleS1.next_to(bob_group, DOWN, buff=0.6)
        twelve = MathTex(r"12", font_size=48, color=ORANGE)
        twelve.move_to(x1_s1_bob[0][-1])  # position over T
        twelve.shift(RIGHT * 0.3).shift(DOWN * 0.03)
        self.play(FadeOut(s1_b1_transform, sum_s1_bob), run_time=1)
        self.play(Write(exampleS1), ReplacementTransform(x1_s1_bob[0][-1], twelve), run_time=2)
        self.pause(4)

        # replacement values
        val_0 = MathTex(r"1", font_size=48, color=POLY_COLOR)
        val_1 = MathTex(r"11", font_size=48, color=POLY_COLOR)

        # position them over S_1(0) and S_1(1)
        val_0.move_to(x1_s1_bob[0][0:5])   # adjust indices to cover S_1(0)
        val_1.move_to(x1_s1_bob[0][6:11])  # adjust indices to cover S_1(1)

        self.play(
            ReplacementTransform(x1_s1_bob[0][0:5], val_0),
            ReplacementTransform(x1_s1_bob[0][6:11], val_1),
            run_time=2
        )
        self.wait(3)

        random_r = MathTex(r"r \overset{\$}{\leftarrow} \mathbb{F}_q}", font_size=48, color=FIELD_COLOR)
        random_r.next_to(bob_group, DOWN, buff=0.4)

        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != bob_group], run_time=1.5)
        self.play(Write(random_r), run_time=2)
        example_r = MathTex(r"r = 2", font_size=48, color=FIELD_COLOR)
        example_r.next_to(random_r, DOWN, buff=0.4)
        self.play(Write(example_r), run_time=1.5)
        self.wait(3)

        alice_group.move_to(bob_group.get_center())
        alice_group.shift(LEFT * 15)
        self.add(alice_group)

        self.play(
            *[mob.animate.shift(RIGHT * 15) for mob in self.mobjects if mob != alice_group],
            alice_group.animate.shift(RIGHT * 15),
            run_time=1.5
        )
        self.clear()
        alice_group.move_to(ORIGIN).to_edge(UP, buff=0.5)
        self.add(alice_group)
        self.wait(1)
        self.wait(5)


class SumCheckScene2(Scene):
    def construct(self):
        # alice is already on screen from previous scene
        alice = Circle(radius=0.75, color=PROVER_COLOR, fill_opacity=0.2)
        alice_text = Text("Alice", font_size=22, color=PROVER_COLOR)
        alice_text.move_to(alice)
        alice_group = VGroup(alice, alice_text)
        alice_group.move_to(ORIGIN).to_edge(UP, buff=0.5)
        self.add(alice_group)  # no animation, just place her
        self.wait(5)
        # ── Alice receives r=2 ───────────────────────────────────────────
        r_received = MathTex(r"r_1 = 2", font_size=48, color=FIELD_COLOR)
        r_received.next_to(alice_group, DOWN, buff=0.6)
        r_received.shift(RIGHT * 15)
        self.play(r_received.animate.shift(LEFT * 15), run_time=1.5)
        self.wait(1.5)

        # ── Alice defines S_2 ────────────────────────────────────────────
        sum_x2 = MathTex(
            r"S_2(X_2) = \sum_{X_3 \ldots X_n} g(r_1, X_2, X_3 \ldots X_n)",
            font_size=40, color=POLY_COLOR
        )
        sum_x2.next_to(r_received, DOWN, buff=0.5)
        self.play(Write(sum_x2), run_time=3)
        self.wait(7.5)

        self.play(
            FadeOut(r_received),
            sum_x2.animate.to_edge(UP, buff=0.8).to_edge(LEFT, buff=0.1).scale(0.6),
            run_time=1.5
        )

        # ── show example polynomial ──────────────────────────────────────
        example = MathTex(
            r"g(X_1, X_2, X_3) = 2X_1^3 + X_1 X_3 + X_2 X_3",
            font_size=40, color=POLY_COLOR
        )
        example.next_to(alice_group, DOWN, buff=0.6)
        self.play(Write(example), run_time=2)
        self.wait(1.5)

        # ── substitute r=2 into X_1 ──────────────────────────────────────
        example_sub = MathTex(
            r"g(2, X_2, X_3) = 2(2)^3 + 2X_3 + X_2 X_3",
            font_size=40, color=POLY_COLOR
        )
        example_sub.move_to(example)
        self.play(ReplacementTransform(example, example_sub), run_time=1.5)
        self.wait(0.5)

        # ── expand summation over X_3 ∈ {0,1} ───────────────────────────
        g_2_summation = MathTex(
            r"g(2, X_2, 0) + g(2, X_2, 1)",
            font_size=40, color=POLY_COLOR
        )
        g_2_summation.next_to(example_sub, DOWN, buff=0.5)
        self.play(Write(g_2_summation), run_time=2)
        self.wait(1)

        g2_expanded = MathTex(
            r"= 16 + (18 + X_2)",
            font_size=40, color=POLY_COLOR
        )
        g2_expanded.next_to(g_2_summation, DOWN, buff=0.4)
        self.play(Write(g2_expanded), run_time=2)
        self.wait(1)

        g2_new = MathTex(
            r"S_2(X_2) = X_2 + 34",
            font_size=48, color=POLY_COLOR
        )
        g2_new.next_to(g2_expanded, DOWN, buff=0.5)
        self.play(Write(g2_new), run_time=2.5)
        self.wait(2)
        # ── swipe to Bob ─────────────────────────────────────────────────
        bob = Circle(radius=0.75, color=VERIF_COLOR, fill_opacity=0.2)
        bob_text = Text("Bob", font_size=22, color=VERIF_COLOR)
        bob_text.move_to(bob)
        bob_group = VGroup(bob, bob_text)
        bob_group.move_to(alice_group.get_center())
        bob_group.shift(RIGHT * 15)
        self.add(bob_group)

        self.play(
            *[mob.animate.shift(LEFT * 15) for mob in self.mobjects if mob != bob_group],
            bob_group.animate.shift(LEFT * 15),
            run_time=1.5
        )
        self.clear()
        bob_group.move_to(ORIGIN).to_edge(UP, buff=0.5)
        self.add(bob_group)
        self.wait(1.5)

        # ── Bob receives S_2 from Alice ──────────────────────────────────
        s2_received = MathTex(
            r"S_2(X_2) = X_2 + 34",
            font_size=48, color=POLY_COLOR
        )
        s2_received.next_to(bob_group, DOWN, buff=0.6)
        s2_received.shift(LEFT * 15)
        self.play(s2_received.animate.shift(RIGHT * 15), run_time=1.5)
        self.wait(2)

        # ── Bob expands the summation ────────────────────────────────────
        sum_s2_bob = MathTex(r"\sum_{X_2 \in \{0,1\}}", font_size=36, color=POLY_COLOR)
        self.play(s2_received.animate.shift(RIGHT * 0.4), run_time=1)
        sum_s2_bob.next_to(s2_received, LEFT)
        self.play(Write(sum_s2_bob), run_time=2)
        self.wait(2)

        # ── expand S_2(0) + S_2(1) =? S_1(r) ───────────────────────────
        x2_s2_bob = MathTex(
            r"S_2(0) + S_2(1) \stackrel{?}{=} S_1(r_1)",
            font_size=40, color=POLY_COLOR
        )
        x2_s2_bob.next_to(sum_s2_bob, DOWN, buff=0.5)
        x2_s2_bob.shift(RIGHT * 2)
        self.play(Write(x2_s2_bob), run_time=2.5)
        self.wait(7)

        # ── evaluate: S_2(0)=34, S_2(1)=35 ─────────────────────────────
        val_0 = MathTex(r"34", font_size=40, color=POLY_COLOR)
        val_1 = MathTex(r"35", font_size=40, color=POLY_COLOR)
        val_0.move_to(x2_s2_bob[0][0:5])
        val_1.move_to(x2_s2_bob[0][6:11])

        self.play(
            ReplacementTransform(x2_s2_bob[0][0:5], val_0),
            ReplacementTransform(x2_s2_bob[0][6:11], val_1),
            run_time=1.5
        )
        self.wait(2)

        # ── verify against S_1(r) = S_1(2) ──────────────────────────────
        # S_1(2) = 8(2)^3 + 2(2) + 1 = 64 + 4 + 1 = 69
        s1_r = MathTex(
            r"S_1(2) = 8(2)^3 + 2(2) + 1 = 69",
            font_size=36, color=FIELD_COLOR
        )
        s1_r.next_to(x2_s2_bob, DOWN, buff=0.5)
        self.play(Write(s1_r), run_time=2.5)
        self.wait(2)

        # 34 + 35 = 69 ✓
        check = MathTex(r"34 + 35 = 69 \checkmark", font_size=40, color=GOOD_COLOR)
        check.next_to(s1_r, DOWN, buff=0.4)
        self.play(Write(check), run_time=1.5)
        self.wait(3)

        # ── Bob picks new random r_2 ─────────────────────────────────────
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != bob_group],
            run_time=1.5
        )

        random_r2 = MathTex(
            r"r_2 \overset{\$}{\leftarrow} \mathbb{F}_q",
            font_size=48, color=FIELD_COLOR
        )
        random_r2.next_to(bob_group, DOWN, buff=0.4)
        self.play(Write(random_r2), run_time=2)

        example_r2 = MathTex(r"r_2 = 3", font_size=48, color=FIELD_COLOR)
        example_r2.next_to(random_r2, DOWN, buff=0.4)
        self.play(Write(example_r2), run_time=1.5)
        self.wait(3)

        # ── swipe back to both on screen ─────────────────────────────────
        alice = Circle(radius=0.75, color=PROVER_COLOR, fill_opacity=0.2)
        alice_text = Text("Alice", font_size=22, color=PROVER_COLOR)
        alice_text.move_to(alice)
        alice_group = VGroup(alice, alice_text)
        alice_group.to_edge(UP, buff=0.5).to_edge(LEFT, buff=2)
        alice_group.shift(LEFT * 15)  # start off screen left
        self.add(alice_group)

        self.play(
            bob_group.animate.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=2),
            alice_group.animate.shift(RIGHT * 15),
            *[FadeOut(mob) for mob in self.mobjects if mob not in [bob_group, alice_group]],
            run_time=1.5
        )
        self.wait(5)


class SumCheckRoundI(Scene):
    def construct(self):
        # ── continuing from scene 2 ──────────────────────────────────────
        alice = Circle(radius=0.75, color=PROVER_COLOR, fill_opacity=0.2)
        alice_text = Text("Alice", font_size=22, color=PROVER_COLOR)
        alice_text.move_to(alice)
        alice_group = VGroup(alice, alice_text).to_edge(UP, buff=0.5).to_edge(LEFT, buff=2)

        bob = Circle(radius=0.75, color=VERIF_COLOR, fill_opacity=0.2)
        bob_text = Text("Bob", font_size=22, color=VERIF_COLOR)
        bob_text.move_to(bob)
        bob_group = VGroup(bob, bob_text).to_edge(UP, buff=0.5).to_edge(RIGHT, buff=2)

        self.add(alice_group, bob_group)
        self.wait(1)

        # helper: arrow at y=0, x from sender to receiver
        def make_arrow(sender, receiver, color):
            start = np.array([sender.get_center()[0], 0, 0])
            end   = np.array([receiver.get_center()[0], 0, 0])
            return Arrow(start=start, end=end, color=color, buff=0)

        # ── Bob sends r_i to Alice ────────────────────────────────────────
        arrow_to_alice = make_arrow(bob_group, alice_group, VERIF_COLOR)
        r_label = MathTex(r"r_i", font_size=48, color=VERIF_COLOR)
        r_label.next_to(arrow_to_alice, UP, buff=0.15)
        self.play(Create(arrow_to_alice), Write(r_label), run_time=1.5)
        self.wait(2)

        # ── Alice computes S_{i+1}: Alice to center, Bob exits right ─────
        self.play(
            FadeOut(arrow_to_alice), FadeOut(r_label),
            run_time=0.5
        )
        self.play(
            alice_group.animate.move_to(UP * 3),
            bob_group.animate.shift(RIGHT * 15),
            run_time=1.2
        )

        s_full = MathTex(
            r"S_{i+1}(X_{i+1}) = \!\!\sum_{X_{i+2},\ldots,X_n \in \{0,1\}}\!\! g(r_1,\ldots,r_i, X_{i+1},\ldots,X_n)",
            font_size=48, color=POLY_COLOR
        )
        s_full.next_to(alice_group, DOWN, buff=2)
        self.play(Write(s_full), run_time=2.5)
        self.wait(12)

        # ── swipe back: both at top corners ──────────────────────────────
        bob_group.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=2)
        bob_group.shift(RIGHT * 15)
        self.play(
            alice_group.animate.to_edge(UP, buff=0.5).to_edge(LEFT, buff=2),
            bob_group.animate.shift(LEFT * 15),
            FadeOut(s_full),
            run_time=1.2
        )
        self.wait(1)

        # ── Alice sends S_{i+1} to Bob ────────────────────────────────────
        arrow_to_bob = make_arrow(alice_group, bob_group, PROVER_COLOR)
        s_label = MathTex(r"S_{i+1}(X_{i+1})", font_size=48, color=PROVER_COLOR)
        s_label.next_to(arrow_to_bob, UP, buff=0.15)
        self.play(Create(arrow_to_bob), Write(s_label), run_time=1.5)
        self.wait(1)

        # ── Bob checks: Bob to center, Alice exits left ───────────────────
        self.play(
            FadeOut(arrow_to_bob), FadeOut(s_label),
            run_time=0.5
        )
        self.play(
            bob_group.animate.move_to(UP * 3),
            alice_group.animate.shift(LEFT * 15),
            run_time=1.2
        )

        check = MathTex(
            r"S_{i+1}(0) + S_{i+1}(1) \stackrel{?}{=} S_i(r_i)",
            font_size=48, color=VERIF_COLOR
        )
        check.next_to(bob_group, DOWN, buff=0.5)
        self.play(Write(check), run_time=2.5)
        self.wait(6)

        # ── Bob samples r_{i+1} ──────────────────────────────────────────
        next_round = MathTex(
            r"r_{i+1} \overset{\$}{\leftarrow} \mathbb{F}_q",
            font_size=48, color=VERIF_COLOR
        )
        next_round.next_to(check, DOWN, buff=0.5)
        repeat = Text("Repeat for round i+1", font_size=26, color=WHITE)
        repeat.next_to(next_round, DOWN, buff=0.4)

        self.play(Write(next_round), run_time=1.5)
        self.wait(2)

        # ── swipe back: both at top corners ──────────────────────────────
        alice_group.to_edge(UP, buff=0.5).to_edge(LEFT, buff=2)
        alice_group.shift(LEFT * 15)
        self.play(
            bob_group.animate.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=2),
            alice_group.animate.shift(RIGHT * 15),
            FadeOut(check), FadeOut(next_round),
            run_time=1.2
        )
        self.wait(0.5)

        repeat = Tex("Repeat for rounds $i+1, i+2, ..., n$", font_size=32, color=WHITE)
        repeat.to_edge(UP, buff=0.5).move_to(UP * 3)  # top center between them
        self.play(Write(repeat), run_time=1.2)
        self.wait(0.5)

        # ── stacked arrows showing remaining rounds ───────────────────────
        start_y = alice_group.get_bottom()[1] - 0.5
        spacing = 1.0

        rounds = [
            (r"r_{i+1}", VERIF_COLOR, "bob_to_alice"),
            (r"S_{i+2}(X_{i+2})", PROVER_COLOR, "alice_to_bob"),
            (r"\vdots", WHITE, None),
            (r"r_{n-1}", VERIF_COLOR, "bob_to_alice"),
            (r"S_n(X_n)", PROVER_COLOR, "alice_to_bob"),
        ]

        extra_pad = 0  # accumulates extra padding after the dots

        for i, (label_tex, color, direction) in enumerate(rounds):
            y = start_y - i * spacing - extra_pad

            label = MathTex(label_tex, font_size=32, color=color)

            if direction is None:
                label.move_to(np.array([0, y, 0]))
                self.play(Write(label), run_time=0.5)
                extra_pad += 0.4  # extra breathing room after dots
            else:
                if direction == "bob_to_alice":
                    start = np.array([bob_group.get_center()[0], y, 0])
                    end   = np.array([alice_group.get_center()[0], y, 0])
                else:
                    start = np.array([alice_group.get_center()[0], y, 0])
                    end   = np.array([bob_group.get_center()[0], y, 0])

                arrow = Arrow(start=start, end=end, color=color, buff=0)
                label.next_to(arrow, UP, buff=0.1)
                self.play(Create(arrow), Write(label), run_time=0.8)

            self.wait(0.5)

        self.wait(2)

        # ── Bob shifts to center, everything else fades out ───────────────
        self.play(
            bob_group.animate.move_to(UP * 3),
            *[FadeOut(mob) for mob in self.mobjects if mob != bob_group],
            run_time=1.5
        )
        self.wait(5)

class SumCheckFinale(Scene):
    def construct(self):
        # ── Bob already in center from previous scene ─────────────────────
        bob = Circle(radius=0.75, color=VERIF_COLOR, fill_opacity=0.2)
        bob_text = Text("Bob", font_size=22, color=VERIF_COLOR)
        bob_text.move_to(bob)
        bob_group = VGroup(bob, bob_text)
        bob_group.move_to(UP * 3)
        self.add(bob_group)
        self.wait(5)

        # ── Bob checks S_n(0) + S_n(1) =? S_{n-1}(r_{n-1}) ─────────────
        check = MathTex(
            r"S_n(0) + S_n(1) \stackrel{?}{=} S_{n-1}(r_{n-1})",
            font_size=48, color=VERIF_COLOR
        )
        check.next_to(bob_group, DOWN, buff=0.5)
        self.play(Write(check), run_time=2.5)
        self.wait(4)

        checkmark = MathTex(r"\checkmark", font_size=48, color=GOOD_COLOR)
        checkmark.next_to(check, RIGHT, buff=0.3)
        self.play(Write(checkmark), run_time=0.8)
        self.wait(1)

        # ── clear and move to final check ────────────────────────────────
        self.play(FadeOut(check), FadeOut(checkmark), run_time=1.0)
        self.wait(0.5)

        # ── Bob selects final random r_n ──────────────────────────────────
        random_rn = MathTex(
            r"r_n \overset{\$}{\leftarrow} \mathbb{F}_q",
            font_size=48, color=FIELD_COLOR
        )
        random_rn.next_to(bob_group, DOWN, buff=0.5)
        self.play(Write(random_rn), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(random_rn), run_time=0.8)

        # ── final check: g(r_1,...,r_n) =? S_n(r_n) ─────────────────────
        final_check = MathTex(
            r"g(r_1, r_2, \ldots, r_n) \stackrel{?}{=} S_n(r_n)",
            font_size=48, color=VERIF_COLOR
        )
        final_check.next_to(bob_group, DOWN, buff=0.5)
        self.play(Write(final_check), run_time=2.5)
        self.wait(10)

        # ── if equal, sum is verified ─────────────────────────────────────
        verdict = MathTex(
            r"\sum_{x_1,\ldots,x_n \in \{0,1\}} g(x_1,\ldots,x_n) = T \quad \checkmark",
            font_size=48, color=GOOD_COLOR
        )
        verdict.next_to(final_check, DOWN, buff=0.5)
        self.play(Write(verdict), run_time=2.5)
        self.wait(5)


        # ── fade out equations, revert to example polynomial ─────────────
        self.play(
            FadeOut(final_check), FadeOut(verdict),
            run_time=1.0
        )
        self.wait(0.5)

        example = MathTex(
            r"g(X_1, X_2, X_3) = 2X_1^3 + X_1 X_3 + X_2 X_3",
            font_size=48, color=POLY_COLOR
        )
        example.next_to(bob_group, DOWN, buff=0.5)
        self.play(Write(example), run_time=2.5)
        self.wait(1)
        
        # ── show r values ─────────────────────────────────────────────────
        r_vals = MathTex(
            r"(r_1, r_2, r_3) = (2, 3, 4)",
            font_size=48, color=FIELD_COLOR
        )
        r_vals.next_to(example, DOWN, buff=0.5)
        self.play(Write(r_vals), run_time=1.5)
        self.wait(2)

        # S_3(X_3) = g(2, 3, X_3) = 2(2)^3 + 2*X_3 + 3*X_3 = 16 + 5X_3
        s_n = MathTex(
            r"S_3(X_3) = g(2, 3, X_3) = 16 + 5X_3",
            font_size=48, color=POLY_COLOR
        )
        s_n.next_to(r_vals, DOWN, buff=0.5)
        self.play(Write(s_n), run_time=2.5)
        self.wait(3)


        self.play(
            example.animate.scale(0.6).next_to(bob_group, LEFT, buff=0.5),
            s_n.animate.scale(0.6).next_to(bob_group, RIGHT, buff=0.5),
            r_vals.animate.scale(0.7).next_to(bob_group, DOWN, buff=0.3),
            run_time=1.5
        )
        self.wait(2)

        aligned = MathTex(
            r"g(r_1, r_2, r_3) &= S_3(r_3) \\",
            r"g(2, 3, 4) &= S_3(4) \\",
            r"2(2)^3 + 2(4) + 3(4) &= 16 + 5(4) \\",
            r"36 &= 36 \quad \checkmark",
            font_size=36,
        )
        aligned.next_to(r_vals, DOWN, buff=0.7).shift(LEFT * 0.7)

        for i, line in enumerate(aligned):
            color = GOOD_COLOR if i == 3 else POLY_COLOR
            line.set_color(color)
            self.play(Write(line), run_time=1.2)
            self.wait(0.8)

        self.wait(6)
        self.play(FadeOut(*self.mobjects), run_time=4.0)
        self.wait(4)

class SumCheckSoundness(Scene):
    def construct(self):
        # ── soundness title ───────────────────────────────────────────────
        self.wait(5)
        title = Text("Soundness", font_size=64, color=WHITE, weight=BOLD)
        self.play(Write(title), run_time=1.5)
        self.wait(8)
        self.play(FadeOut(title), run_time=1.0)

        # ── Alice claims false T* ─────────────────────────────────────────
        false_claim = MathTex(
            r"T^* \neq \sum_{x_1,\ldots,x_n} g(x_1,\ldots,x_n)",
            font_size=46, color=WHITE
        )
        self.play(Write(false_claim), run_time=2)
        self.wait(7)

        self.play(FadeOut(false_claim), run_time=1.0)

        # ── both on screen ────────────────────────────────────────────────
        alice = Circle(radius=0.75, color=PROVER_COLOR, fill_opacity=0.2)
        alice_text = Text("Alice", font_size=22, color=PROVER_COLOR)
        alice_text.move_to(alice)
        alice_group = VGroup(alice, alice_text).to_edge(UP, buff=0.5).to_edge(LEFT, buff=2)

        bob = Circle(radius=0.75, color=VERIF_COLOR, fill_opacity=0.2)
        bob_text = Text("Bob", font_size=22, color=VERIF_COLOR)
        bob_text.move_to(bob)
        bob_group = VGroup(bob, bob_text).to_edge(UP, buff=0.5).to_edge(RIGHT, buff=2)

        self.play(FadeIn(alice_group), FadeIn(bob_group), run_time=0.5)
        self.wait(0.5)

        # ── focus on Alice: Bob exits right ───────────────────────────────
        self.play(
            alice_group.animate.move_to(UP * 3),
            bob_group.animate.shift(RIGHT * 15),
            run_time=1.2
        )
        self.wait(0.5)

        # ── dishonest S_i^* ───────────────────────────────────────────────
        dishonest = MathTex(
            r"S_1^*(X_1) \neq \sum_{X_2,\ldots,X_n} g(X_1, X_2,\ldots,X_n)",
            font_size=48, color=WHITE
        )
        dishonest.next_to(alice_group, DOWN, buff=0.5)
        self.play(Write(dishonest), run_time=2.5)
        self.wait(3)

        # ── but Alice crafts it so the check still passes ─────────────────
        fake_check = MathTex(
            r"S_1^*(0) + S_1^*(1) = T^*",
            font_size=48, color=WHITE
        )
        fake_check.next_to(dishonest, DOWN, buff=0.5)
        self.play(Write(fake_check), run_time=2.5)
        self.wait(3)

        # ── swipe back: both at top corners ───────────────────────────────
        bob_group.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=2)
        bob_group.shift(RIGHT * 15)
        self.play(
            alice_group.animate.to_edge(UP, buff=0.5).to_edge(LEFT, buff=2),
            bob_group.animate.shift(LEFT * 15),
            FadeOut(dishonest), FadeOut(fake_check),
            run_time=1.5
        )
        self.wait(1)

        # ── Alice sends S_i^* to Bob ──────────────────────────────────────
        def make_arrow(sender, receiver, color):
            start = np.array([sender.get_center()[0], 0, 0])
            end   = np.array([receiver.get_center()[0], 0, 0])
            return Arrow(start=start, end=end, color=color, buff=0)

        arrow_to_bob = make_arrow(alice_group, bob_group, PROVER_COLOR)
        s_label = MathTex(r"S_1^*(X_1)", font_size=48, color=WHITE)
        s_label.next_to(arrow_to_bob, UP, buff=0.15)

        self.play(Create(arrow_to_bob), Write(s_label), run_time=1.5)
        self.wait(2)

        # ── focus on Bob: Alice exits left ────────────────────────────────
        self.play(
            FadeOut(arrow_to_bob), FadeOut(s_label),
            run_time=0.5
        )

        self.wait(0.5)

        self.play(
            bob_group.animate.move_to(UP * 3),
            alice_group.animate.shift(LEFT * 15),
            run_time=1
        )
        self.wait(2.5)

        # ── Bob computes g(r_1,...,r_n) directly ──────────────────────────
        g_eval = MathTex(
            r"g(r_1, r_2, \ldots, r_n)",
            font_size=46, color=VERIF_COLOR
        )
        g_eval.next_to(bob_group, DOWN, buff=0.5)
        self.play(Write(g_eval), run_time=2)
        self.wait(6)

        # ── Bob compares to S_n^*(r_n) ────────────────────────────────────
        final_check = MathTex(
            r"S_n^*(r_n) \stackrel{?}{=} g(r_1, r_2, \ldots, r_n)",
            font_size=46, color=VERIF_COLOR
        )
        final_check.next_to(g_eval, DOWN, buff=0.5)
        self.play(Write(final_check), run_time=2.5)
        self.wait(4)

        # ── they differ with high probability ────────────────────────────
        prob = MathTex(
            r"\Pr\left[S_n^*(r_n) = g(r_1,\ldots,r_n)\right] \leq\frac{d}{|\mathbb{F}|} \text{ (Schwartz-Zippel)}",
            font_size=48, color=WHITE
        )
        self.pause(5)
        prob.next_to(final_check, DOWN, buff=0.5)
        self.play(Write(prob), run_time=4)
        self.wait(7)

        # ── swipe back: both at top corners ──────────────────────────────
        alice_group.to_edge(UP, buff=0.5).to_edge(LEFT, buff=2)
        alice_group.shift(LEFT * 15)
        self.play(
            bob_group.animate.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=2),
            alice_group.animate.shift(RIGHT * 15),
            FadeOut(g_eval), FadeOut(final_check), FadeOut(prob),
            run_time=1.5
        )
        self.wait(0.5)
        roundI = MathTex(
            r"\text{Round } i", font_size=48, color=WHITE
        )
        roundI.to_edge(UP, buff=1)
        self.play(Write(roundI), run_time=1.5)
        self.wait(1)


        arrow_to_bob = make_arrow(alice_group, bob_group, PROVER_COLOR)
        s_label = MathTex(r"S_i^*(X_i)", font_size=48, color=WHITE)
        s_label.next_to(arrow_to_bob, UP, buff=0.15)

        self.play(Create(arrow_to_bob), Write(s_label), run_time=1)
        self.wait(1.5)

        self.play(FadeOut(arrow_to_bob), FadeOut(s_label), run_time=1)
        self.wait(0.5)
        # ── Bob sends r_i back to Alice ───────────────────────────────────
        arrow_to_alice = make_arrow(bob_group, alice_group, VERIF_COLOR)
        r_label = MathTex(r"r_i", font_size=48, color=VERIF_COLOR)
        r_label.next_to(arrow_to_alice, UP, buff=0.15)

        self.play(
            Create(arrow_to_alice), Write(r_label),
            run_time=1
        )
        self.wait(1)

        self.play(FadeOut(arrow_to_alice), FadeOut(r_label), run_time=1)

        # ── show the agreement condition ──────────────────────────────────
        agreement = MathTex(
            r"S_i^*(r_i) = S_i(r_i)",
            font_size=48, color=WHITE
        )
        agreement.move_to(ORIGIN)
        self.play(Write(agreement), run_time=1.5)
        self.wait(7)

        left_prob = MathTex(
            r"\Pr\left[",
            font_size=42, color=WHITE
        )

        right_prob = MathTex(
            r"\right] \leq \frac{d}{|\mathbb{F}|}",
            font_size=42, color=WHITE
        )

        self.play(agreement.animate.shift(UP * 0.5).shift(LEFT * 0.5).scale(0.8), run_time=1)
        left_prob.next_to(agreement, LEFT, buff=0.1)
        right_prob.next_to(agreement, RIGHT, buff=0.1)
        self.play(Write(left_prob), Write(right_prob), run_time=1.5)
        self.wait(3)

        # ── fade out everything except probability, shift to top ──────────
        prob_group = VGroup(left_prob, agreement, right_prob)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [left_prob, agreement, right_prob]],
            prob_group.animate.to_edge(UP, buff=0.5),
            run_time=1.5
        )
        self.wait(0.5)

        for_rounds = MathTex(
            r"\text{for rounds } 1, \ldots, n",
            font_size=42, color=WHITE
        )
        for_rounds.next_to(prob_group, DOWN, buff=0.2)
        self.play(Write(for_rounds), run_time=1.2)
        self.wait(1)

        soundness = MathTex(
            r"\text{If } T^* \neq \sum_{x_1,\ldots,x_n} g(x_1,\ldots,x_n)",
            r"\implies \Pr[\text{Alice convinces Bob}] \leq \frac{dn}{|\mathbb{F}|}",
            font_size=36, color=WHITE
        )

        self.play(Write(soundness), run_time=2.5)
        self.wait(6)

        prob = soundness[1][-6:].copy()
        self.add(prob)

        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != prob],
            prob.animate.scale(1.5).move_to(ORIGIN),
            run_time=1.5
        )
        self.wait(4)

        large_prime = MathTex(r"2^{1279}-1", font_size=48, color=FIELD_COLOR)
        large_prime.move_to(prob[-2:])

        self.play(ReplacementTransform(prob[-3:], large_prime), run_time=1.5)

        self.wait(4)
        self.play(FadeOut(*self.mobjects), run_time=3.0)

        self.wait(5)
        