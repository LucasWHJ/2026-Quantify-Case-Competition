"""Checks for accounting, order-sensitive attribution and contract boundaries."""
import unittest
import numpy as np
import pandas as pd
from src.analysis import financial_metrics, sequential_shares, model_diagnostics
from src.pilot import Pilot, covered_indemnity, common_vendor_stress


class AnalysisTests(unittest.TestCase):
    def test_company_ratio_is_amount_weighted(self):
        frame = pd.DataFrame([
            dict(line="A", year=2025, exposure=10, claim_count=2,
                 earned_premium_cad=100, incurred_losses_cad=50, operating_expenses_cad=20),
            dict(line="B", year=2025, exposure=20, claim_count=1,
                 earned_premium_cad=900, incurred_losses_cad=810, operating_expenses_cad=90)])
        metrics, annual = financial_metrics(frame)
        self.assertAlmostEqual(annual.combined_ratio.iloc[0], .97)
        self.assertAlmostEqual(metrics.underwriting_profit_cad.sum(), 30)
        np.testing.assert_allclose(metrics.claim_frequency * metrics.average_severity_cad, metrics.pure_premium_cad)

    def test_same_model_fit_different_sequential_allocations(self):
        rng = np.random.default_rng(7)
        rows = []
        for i in range(180):
            mechanism = "high" if i % 3 else "low"
            industry = mechanism if i % 7 else ("high" if mechanism == "low" else "low")
            oversight = "Yes" if i % 2 else "No"
            log_loss = 10 + 2 * (mechanism == "high") - .2 * (oversight == "Yes") + rng.normal(0, .15)
            rows.append(dict(failure_type=mechanism, industry=industry, human_oversight=oversight,
                             estimated_insured_loss_cad=np.exp(log_loss)))
        data = pd.DataFrame(rows)
        a = sequential_shares(data, ["industry", "failure_type", "human_oversight"])
        b = sequential_shares(data, ["failure_type", "industry", "human_oversight"])
        self.assertAlmostEqual(a.share_of_total_log_variance.sum(), 1)
        self.assertAlmostEqual(b.share_of_total_log_variance.sum(), 1)
        self.assertAlmostEqual(a.iloc[-1, -1], b.iloc[-1, -1])
        self.assertGreater(a.loc[a.term == "industry"].iloc[0, -1],
                           b.loc[b.term == "industry"].iloc[0, -1])
        model, _ = model_diagnostics(data)
        self.assertGreater(model["oversight_conditional_geometric_mean_ratio"], 0)


class PilotTests(unittest.TestCase):
    def test_break_even_and_target(self):
        result = Pilot().result()
        self.assertAlmostEqual(result["break_even_frequency"], .0275)
        self.assertAlmostEqual(result["target_margin_frequency"], .0225)
        self.assertAlmostEqual(Pilot(claim_frequency=.0275).result()["underwriting_profit_cad"], 0)

    def test_scenario_accounting(self):
        self.assertEqual([Pilot(claim_frequency=f).result()["combined_ratio"] for f in [.01, .02, .03]], [.65, .85, 1.05])

    def test_deductible_and_limit_boundaries(self):
        self.assertEqual(covered_indemnity(9_000, 10_000, 100_000), 0)
        self.assertEqual(covered_indemnity(10_000, 10_000, 100_000), 0)
        self.assertEqual(covered_indemnity(110_000, 10_000, 100_000), 100_000)
        self.assertEqual(covered_indemnity(1_000_000, 10_000, 100_000), 100_000)

    def test_concentration_budget(self):
        self.assertTrue(common_vendor_stress(10, 100_000, 1_000_000)["within_budget"])
        self.assertFalse(common_vendor_stress(11, 100_000, 1_000_000)["within_budget"])

    def test_invalid_inputs(self):
        for kwargs in [dict(policies=0), dict(policies=1.5), dict(variable_expense_ratio=1),
                       dict(mean_covered_cost=0), dict(claim_frequency=-.01), dict(fixed_cost=float("nan"))]:
            with self.assertRaises(ValueError):
                Pilot(**kwargs)


if __name__ == "__main__":
    unittest.main()
