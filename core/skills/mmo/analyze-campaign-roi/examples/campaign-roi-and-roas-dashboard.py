#!/usr/bin/env python3
"""Campaign ROI and Blended ROAS Analytics Dashboard (2026).

Calculates True ROI incorporating operational overhead, proxy costs,
account die-rate attrition, and 90-day LTV cohort retention projections.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class CampaignFinancials:
    ad_spend: float
    direct_revenue: float
    rebill_revenue: float
    tier2_override_rate: float
    milestone_bonus: float
    proxy_cost: float
    api_token_cost: float
    active_accounts: int
    account_die_rate: float
    account_replace_cost: float
    clawback_reserve_rate: float


class CampaignAnalyticsEngine:
    def evaluate(self, fin: CampaignFinancials) -> Dict[str, float]:
        # Revenue aggregation
        tier2_revenue = fin.direct_revenue * fin.tier2_override_rate
        gross_revenue = fin.direct_revenue + fin.rebill_revenue + tier2_revenue + fin.milestone_bonus

        # Operational costs
        replacement_costs = fin.active_accounts * fin.account_die_rate * fin.account_replace_cost
        clawback_escrow = gross_revenue * fin.clawback_reserve_rate

        total_operational_cost = (
            fin.ad_spend + fin.proxy_cost + fin.api_token_cost + replacement_costs + clawback_escrow
        )

        true_net_profit = gross_revenue - total_operational_cost
        true_roi = true_net_profit / total_operational_cost if total_operational_cost > 0 else 0.0

        blended_roas = gross_revenue / fin.ad_spend if fin.ad_spend > 0 else 0.0
        mer = gross_revenue / total_operational_cost if total_operational_cost > 0 else 0.0

        return {
            "gross_revenue": gross_revenue,
            "total_cost": total_operational_cost,
            "true_net_profit": true_net_profit,
            "true_roi": true_roi,
            "blended_roas": blended_roas,
            "mer": mer,
        }


if __name__ == "__main__":
    engine = CampaignAnalyticsEngine()
    sample_data = CampaignFinancials(
        ad_spend=10000.0,
        direct_revenue=22000.0,
        rebill_revenue=7500.0,
        tier2_override_rate=0.05,
        milestone_bonus=1500.0,
        proxy_cost=350.0,
        api_token_cost=120.0,
        active_accounts=20,
        account_die_rate=0.10,
        account_replace_cost=40.0,
        clawback_reserve_rate=0.03,
    )

    metrics = engine.evaluate(sample_data)
    print("Campaign Financial Analysis:")
    print(f"  Gross Revenue:    ${metrics['gross_revenue']:.2f}")
    print(f"  Total Cost:       ${metrics['total_cost']:.2f}")
    print(f"  True Net Profit:  ${metrics['true_net_profit']:.2f}")
    print(f"  True ROI:         {metrics['true_roi']:.2%}")
    print(f"  Blended ROAS:     {metrics['blended_roas']:.2f}x")
    print(f"  MER:              {metrics['mer']:.2f}x")
