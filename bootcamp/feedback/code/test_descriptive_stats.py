import unittest
from pathlib import Path
from unittest.mock import patch

import matplotlib.pyplot as plt
import pandas as pd

import descriptive_stats as report


class SummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = Path(__file__).resolve().parent.parent
        cls.df = pd.read_csv(base / "data" / "AI Bootcamp Baseline Survey_WIDE.csv")
        cls.var_labels, cls.value_labels = report.parse_do_file(
            base / "code" / "import_ai_bootcamp_pre_survey.do"
        )
        cls.questions, cls.choices = report.parse_xlsform(
            base / "documentation" / "AI_Bootcamp_Baseline_XLSForm_v2.xlsx"
        )
        cls.groups, _ = report.find_multiselect_groups(cls.df, cls.var_labels)

    def messages(self, df):
        return report.compute_key_messages(
            df, self.var_labels, self.groups, self.questions, self.choices
        )

    def test_combined_percentages_exclude_missing_answers(self):
        pct, count, n = report.pct_in(pd.Series([1, 2, 3, None]), [1, 2])
        self.assertAlmostEqual(pct, 200 / 3)
        self.assertEqual((count, n), (2, 3))
        self.assertEqual(report.pct_of(pd.Series([1, None]), 1), (100, 1, 1))

    def test_multiselect_excludes_unanswered_parent(self):
        df = pd.DataFrame({"parent": ["1", "2", None], "option": [1, 0, 1]})
        self.assertEqual(report.multiselect_pct(df, "parent", [("option", "1")], "1"), 50)
        with self.assertRaises(KeyError):
            report.multiselect_pct(df, "parent", [("option", "1")], "2")

    def test_current_data_summary_figures(self):
        messages = self.messages(self.df)
        self.assertEqual([len(messages[k]) for k in ["executive", "1", "2", "3", "4"]],
                         [3, 4, 4, 3, 3])
        self.assertIn("68% report at least one hour per day", messages["1"][0])
        self.assertIn("24% who have used a coding agent", messages["1"][1])
        self.assertIn("28% gave detailed disclosure, 38% mentioned AI", messages["1"][3])
        self.assertIn("66% say AI helps", messages["2"][1])
        self.assertIn("65% more output", messages["2"][1])
        self.assertIn("31% are unsure", messages["2"][2])
        self.assertIn("23% using automated tests", messages["2"][3])
        self.assertIn("10% are active users", messages["3"][1])
        self.assertIn("69% have heard", messages["3"][1])
        self.assertIn("41% selected working with raw data", messages["3"][2])
        self.assertIn("work quality (79%) and technical skills (79%)", messages["4"][1])
        self.assertIn("14% good/excellent", messages["4"][2])
        self.assertNotIn("most restrictive", " ".join(sum(messages.values(), [])))
        executive = " ".join(messages["executive"])
        self.assertNotIn("disclosure", executive)
        self.assertNotIn("Training demand", executive)
        self.assertIn("only 24% have tried a coding agent", executive)
        self.assertNotIn("reproducibility", executive)
        self.assertIn("65% report producing more output", executive)
        self.assertIn("66% higher-quality outputs", executive)
        self.assertIn("45% spending less time on analysis", executive)
        self.assertIn("not measured productivity gains", executive)

    def test_executive_and_module_figures_update_together(self):
        df = self.df.copy()
        child = next(col for col, code in self.groups["q1_3"] if code == "5")
        df.loc[df["q1_3"].notna(), child] = 0
        messages = self.messages(df)
        self.assertIn("0% who have used a coding agent", messages["1"][1])
        self.assertIn("0% have tried a coding agent", messages["executive"][1])

    def test_executive_summary_precedes_modules_and_escapes_text(self):
        html = report.build_html(
            self.df, [], {}, {}, self.var_labels, self.value_labels, "survey.csv",
            key_messages={"executive": ["Tools < workflows & skills"]},
        )
        self.assertIn("Tools &lt; workflows &amp; skills", html)
        self.assertLess(html.index('<section class="executive-summary"'),
                        html.index('<nav class="module-nav"'))
        self.assertIn("Percentages use non-missing answers", html)
        self.assertNotIn('class="subtitle"', html)
        self.assertIn("<h1>AI Adoption at the World Bank Group</h1>", html)
        self.assertIn(
            '<p class="report-subtitle">Evidence from the AI-Enabled Research Bootcamp Baseline Survey</p>',
            html,
        )
        self.assertNotIn("survey.csv", html)
        html_without_summary = report.build_html(
            self.df, [], {}, {}, self.var_labels, self.value_labels, "survey.csv"
        )
        self.assertNotIn('<section class="executive-summary"', html_without_summary)

    def test_only_exact_yes_no_questions_use_stacked_bars(self):
        with patch.object(report, "render_stacked_bar_chart", return_value="stacked") as stacked, \
                patch.object(report, "render_bar_chart", return_value="standard"):
            for col in ["q1_6", "q4_4"]:
                image, _ = report.chart_for_single_select(
                    self.df, col, self.var_labels, self.value_labels, self.questions, self.choices
                )
                self.assertEqual(image, "stacked")
                rows, categories, _ = stacked.call_args.args
                self.assertEqual(categories, ["Yes", "No"])
                self.assertAlmostEqual(sum(rows[0][1].values()), 1)
                self.assertEqual(rows[0][2], int(self.df[col].notna().sum()))
                self.assertTrue(stacked.call_args.kwargs["compact"])
            for col in ["q2_1", "q2_2", "q3_1"]:
                image, _ = report.chart_for_single_select(
                    self.df, col, self.var_labels, self.value_labels, self.questions, self.choices
                )
                self.assertEqual(image, "standard")

    def test_current_work_use_combines_both_no_categories(self):
        df = pd.DataFrame({"q1_1": [1, 1, 2, 3, None]})
        with patch.object(report, "render_stacked_bar_chart", return_value="stacked") as stacked:
            image, _ = report.chart_for_single_select(
                df, "q1_1", self.var_labels, self.value_labels, self.questions, self.choices
            )
        self.assertEqual(image, "stacked")
        self.assertEqual(stacked.call_args.args[0], [("", {"Yes": 0.5, "No": 0.5}, 4)])
        self.assertEqual(stacked.call_args.args[1], ["Yes", "No"])
        self.assertTrue(stacked.call_args.kwargs["compact"])

    def test_yes_no_chart_preserves_zero_count_category(self):
        df = pd.DataFrame({"binary": [1, 1, None]})
        with patch.object(report, "render_stacked_bar_chart", return_value="stacked") as stacked:
            report.chart_for_single_select(df, "binary", {}, {"binary": {"1": "Yes", "2": "No"}})
        self.assertEqual(stacked.call_args.args[0], [("", {"Yes": 1, "No": 0}, 2)])

    def test_compact_stacked_chart_geometry(self):
        with patch.object(report, "encode_chart", side_effect=lambda fig: fig):
            fig = report.render_stacked_bar_chart(
                [("", {"Yes": 0.65, "No": 0.35}, 20)], ["Yes", "No"], "Question",
                compact=True,
            )
        try:
            ax = fig.axes[0]
            self.assertEqual(tuple(fig.get_size_inches()), report.COMPACT_CHART_SIZE)
            self.assertEqual(fig.get_size_inches()[1], report.SINGLE_CHART_SIZE[1] / 2)
            self.assertEqual([bar.get_width() for bar in ax.patches], [65, 35])
            self.assertEqual([bar.get_x() for bar in ax.patches], [0, 65])
            self.assertEqual([bar.get_y() for bar in ax.patches], [-0.325, -0.325])
            self.assertEqual(ax.get_xlim(), (0, 100))
            self.assertEqual([t.get_text() for t in fig.legends[0].get_texts()], ["Yes", "No"])
            self.assertEqual([t.get_text() for t in ax.texts], ["65%", "35%"])
        finally:
            plt.close(fig)


if __name__ == "__main__":
    unittest.main()
