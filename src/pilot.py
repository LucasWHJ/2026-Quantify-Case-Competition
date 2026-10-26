"""Illustrative annual underwriting economics, separate from case observations."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Pilot:
    policies: int = 100
    premium_per_policy: float = 5_000.0
    variable_expense_ratio: float = 0.25
    fixed_cost: float = 100_000.0
    claim_frequency: float = 0.02
    mean_covered_cost: float = 100_000.0
    target_margin: float = 0.10

    def __post_init__(self):
        if isinstance(self.policies, bool) or not isinstance(self.policies, int) or self.policies <= 0:
            raise ValueError("policies must be a positive integer")
        for name in ("premium_per_policy", "fixed_cost", "claim_frequency", "mean_covered_cost"):
            value = getattr(self, name)
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        if self.premium_per_policy <= 0 or self.mean_covered_cost <= 0:
            raise ValueError("premium and mean covered cost must be positive")
        if not 0 <= self.variable_expense_ratio < 1:
            raise ValueError("variable expense ratio must be in [0, 1)")
        if not 0 <= self.target_margin < 1:
            raise ValueError("target margin must be in [0, 1)")

    def result(self):
        premium = self.policies * self.premium_per_policy
        variable = premium * self.variable_expense_ratio
        claims = self.policies * self.claim_frequency * self.mean_covered_cost
        cost = variable + self.fixed_cost + claims
        denominator = self.policies * self.mean_covered_cost
        return {
            "policies": self.policies,
            "premium_per_policy_cad": self.premium_per_policy,
            "claim_frequency": self.claim_frequency,
            "mean_covered_cost_cad": self.mean_covered_cost,
            "earned_premium_cad": premium,
            "variable_expense_cad": variable,
            "fixed_cost_cad": self.fixed_cost,
            "expected_covered_cost_cad": claims,
            "underwriting_profit_cad": premium - cost,
            "combined_ratio": cost / premium,
            "break_even_frequency": (premium - variable - self.fixed_cost) / denominator,
            "target_margin_frequency": (premium * (1 - self.variable_expense_ratio - self.target_margin)
                                        - self.fixed_cost) / denominator,
        }


def covered_indemnity(ground_up_loss, deductible, limit):
    """Single-claim indemnity; excludes defence, aggregate exhaustion and reinsurance."""
    if any(not math.isfinite(v) or v < 0 for v in (ground_up_loss, deductible, limit)):
        raise ValueError("loss, deductible and limit must be finite and non-negative")
    return min(max(ground_up_loss - deductible, 0.0), limit)


def common_vendor_stress(affected_policies, average_covered_cost, available_risk_budget):
    """Deterministic gross scenario, not an event probability or capital model."""
    if not isinstance(affected_policies, int) or affected_policies < 0:
        raise ValueError("affected policies must be a non-negative integer")
    if any(not math.isfinite(v) or v < 0 for v in (average_covered_cost, available_risk_budget)):
        raise ValueError("cost and budget must be finite and non-negative")
    stress = affected_policies * average_covered_cost
    return {"gross_stress_cad": stress, "risk_budget_cad": available_risk_budget,
            "within_budget": stress <= available_risk_budget}
