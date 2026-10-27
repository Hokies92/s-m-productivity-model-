"""Model inputs and options.

Defaults are the values in the original workbook's Data Entry sheet.
Every derived total (fully loaded salary, travel, overhead, marketing) is
computed from its components, as the workbook does.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Optional

WORKBOOK_ENGINE_SALARY = 87_750.0   # deliberate test value typed into the original's engine (canonical/FOUNDATION.md sections 3 and 4)
RAMP_RULES = ("workbook", "year_one", "steady_state")


@dataclass
class ModelInputs:
    # Structure
    territories: float = 100            # open territories (a workload container, not headcount)
    deal_size: float = 75_000           # average revenue per transaction

    # Salesperson cost
    base_salary: float = 95_000
    load_rate: float = 0.23             # benefits, payroll tax, etc. as % of base
    commission_rate: float = 0.08

    # Travel components (per trip) and trips per year
    airfare: float = 750
    ground_transport: float = 200
    meals_per_day: float = 100
    lodging_per_night: float = 250
    days_per_trip: float = 2
    entertainment_per_trip: float = 250
    trips_per_year: float = 25

    # Sales mechanics
    manageable_opportunities: float = 30    # cognitive load limit
    cycle_months: float = 6                 # resolution time
    ramp_months: float = 12                 # time for a new salesperson to reach full productivity
    close_rate: float = 0.25

    # Sales overhead components
    non_quota_manager_salaries: float = 2_750_000
    sales_engineers: float = 6_000_000
    sales_admin: float = 800_000
    training: float = 500_000
    incentives: float = 750_000

    # Marketing components
    marketing_personnel: float = 1_000_000
    website: float = 250_000
    events: float = 500_000
    advertising: float = 500_000
    direct_mail: float = 250_000
    telemarketing: float = 250_000
    branding_pr: float = 200_000
    collateral: float = 750_000

    # Non-sales P&L shape, % of revenue
    cogs_pct: float = 0.1322
    rnd_pct: float = 0.1019
    gna_pct: float = 0.154

    # Optional extension (not in the original workbook)
    leads_per_territory: Optional[float] = None

    # ---- derived totals -------------------------------------------------
    @property
    def fully_loaded_salary(self) -> float:
        return self.base_salary * (1 + self.load_rate)

    @property
    def travel(self) -> float:
        per_trip = (self.airfare + self.ground_transport
                    + self.meals_per_day * self.days_per_trip
                    + self.lodging_per_night * self.days_per_trip
                    + self.entertainment_per_trip)
        return per_trip * self.trips_per_year

    @property
    def sales_overhead(self) -> float:
        return (self.non_quota_manager_salaries + self.sales_engineers
                + self.sales_admin + self.training + self.incentives)

    @property
    def marketing(self) -> float:
        return (self.marketing_personnel + self.website + self.events
                + self.advertising + self.direct_mail + self.telemarketing
                + self.branding_pr + self.collateral)

    def validate(self) -> None:
        if self.cycle_months <= 0:
            raise ValueError("cycle_months must be > 0")
        if not 0 <= self.close_rate <= 1:
            raise ValueError("close_rate must be between 0 and 1")
        if self.territories < 0 or self.manageable_opportunities < 0:
            raise ValueError("territories and manageable_opportunities must be >= 0")
        if not 0 <= self.ramp_months <= 12:
            raise ValueError("ramp_months must be between 0 and 12 (model horizon is one year)")

    # ---- serialization --------------------------------------------------
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ModelInputs":
        known = {f.name for f in fields(cls)}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"Unknown input field(s): {', '.join(sorted(unknown))}")
        obj = cls(**data)
        obj.validate()
        return obj


@dataclass
class Adjustments:
    """Size of each lever's change. Positive = improvement (cycle is shortened)."""
    territories: float = 0.10
    close_rate: float = 0.10
    cycle_time: float = 0.10
    deal_size: float = 0.10

    @classmethod
    def uniform(cls, value: float) -> "Adjustments":
        return cls(value, value, value, value)


@dataclass
class ModelOptions:
    """Alternatives to the original's deliberate values (canonical/FOUNDATION.md sections 3 and 4).

    Defaults reproduce the original workbook exactly.
    """
    use_entered_salary: bool = False     # False = the 87,750 typed into the original's engine
    ramp_rule: str = "workbook"          # workbook | year_one | steady_state
    adjustments: Adjustments = field(default_factory=Adjustments)

    def __post_init__(self) -> None:
        if self.ramp_rule not in RAMP_RULES:
            raise ValueError(f"ramp_rule must be one of {RAMP_RULES}")

    @property
    def is_workbook_faithful(self) -> bool:
        return not self.use_entered_salary and self.ramp_rule == "workbook"
